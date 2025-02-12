# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""
import re
import collections
import logging

from circuit import Ckt
from pdk import PDK_Model

# import klayout.db as db


logger = logging.getLogger(__name__)


# netlist parser

unit_multipliers = {
    'T': 1e12,
    'G': 1e9,
    'X': 1e6,
    'MEG': 1e6,
    'K': 1e3,
    'M': 1e-3,
    'U': 1e-6,
    'N': 1e-9,
    'P': 1e-12,
    'F': 1e-15
}


def str2float(val):
    unit = next((x for x in unit_multipliers if val.endswith(x.upper()) or val.endswith(x.lower())), None)
    numstr = val if unit is None else val[:-1*len(unit)]
    return float(numstr) * unit_multipliers[unit] if unit is not None else float(numstr)


# Token specification
modifiers = '|'.join(unit_multipliers.keys()) # 'T|G|X|MEG|K|M|U|N|P|F'
numericval = fr'[+-]?(?:0|[1-9]\d*)(?:[.]\d+)?(?:E[+\-]?\d+)?(?:{modifiers})?' #fr means {} can be used
identifier = r'[^\s{}()=;*]+'
operator = r'\s*[*+-/%]\s*'
exprcontent = fr'(?:{numericval}|{identifier})(?:{operator}(?:{numericval}|{identifier}))*'
commentchars = r'(?:[;$]|//)'

token_re_map = {
    'ANNOTATION': fr'(^|\s)*(\*|{commentchars})+\s*\@:\s*[^\n\r]*',
    'NLCOMMENT': r'(^|[\n\r])+\*[^\n\r]*',
    'COMMENT': fr'(^|\s)*{commentchars}[^\n\r]*',
    'CONTINUE': r'(^|[\n\r])+\+',
    'CONTINUEBACKSLASH': r'\\\s*[\n\r]',
    'NEWL': r'[\s]*[\n\r]+',
    'EQUALS': r'\s*=\s*',
    'EXPR': fr"""(?P<quote>['"]){exprcontent}(?P=quote)|({{){exprcontent}(}})""",
    'NUMBER': numericval + fr'(?=\s|\Z|{commentchars})',
    'DECL': fr'\.{identifier}',
    'NAME': identifier,
    'WS': r'\s+'}
spice_pat = re.compile('|'.join(fr'(?P<{x}>{y})' for x, y in token_re_map.items()), flags=re.IGNORECASE)

# constraint_dict = {x: getattr(constraint, x) for x in dir(constraint) if not x.startswith('_')}

# Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])


#if some device cannot find in pdk lib, print and logger warning, pass that ckt
class SpiceParser:

    _context = []
    #mode 1: 
    #mode 2:
    def __init__(self, pdk_lib = {}, mode='netlist'):
        self.mode = mode.lower()
        if self.mode == 'netlist':
            self.pdk_lib = pdk_lib
        else:
            self.pdk_lib = {}
        assert self.mode in ('netlist', 'model')

        self.data = {}
        # self.library = Library(loadbuiltins=True) if library is None else library
        # self.circuit = Circuit()
        # self._scope = [self.circuit]

    @staticmethod
    def _generate_tokens(text):
        scanner = spice_pat.scanner(text)
        for m in iter(scanner.match, None):

            tok = Token(m.lastgroup, m.group())
            # print(tok)
            if tok.type in ['EXPR', 'NUMBER', 'DECL', 'NAME', 'NEWL', 'EQUALS', 'ANNOTATION']:
                yield tok

    def parse(self, text):
        cache = []
        self._constraints = None
        for tok in self._generate_tokens(text):
            # print(tok)
            if tok.type == 'NEWL':
                self._dispatch(cache)
                cache.clear()
            # TODO for analog constraints
            # elif tok.type == 'ANNOTATION':
            #     self._dispatch(cache)
            #     cache.clear()
            #     self._queue_constraint(tok.value)
            else:
                cache.append(tok)
        self._dispatch(cache)

    def _dispatch(self, cache):
        if len(cache) == 0:
            return
        token = cache.pop(0)
        args, kwargs = self._decompose(cache)
        if token.type == 'DECL':
            self._process_declaration(token.value.upper(), args, kwargs)
        elif token.type == 'NAME':
            # print('NAME', args, kwargs  )
            self._process_instance(token.value.upper(), args, kwargs)
        else:
            assert False

    #TODO for ananlog constaints
    # def _queue_constraint(self, annotation):
    #     constraint = annotation.split('@:')[1].strip()
    #     assert self._constraints is not None, \
    #         f'Constraint {constraint} can only be defined within a .SUBCKT \nCurrent scope:{self._scope[-1]}'
    #     self._constraints.append(constraint)

    @staticmethod
    def _decompose(cache):
        for x in cache:
            if not(x.type in ('NAME', 'NUMBER', 'EXPR', 'EQUALS')):
                print(x)
        assert all(x.type in ('NAME', 'NUMBER', 'EXPR', 'EQUALS') for x in cache), cache
        assignments = {i for i, x in enumerate(cache) if x.type == 'EQUALS'}
        assert all(cache[i-1].type == 'NAME' for i in assignments)
        args = [SpiceParser._cast(x.value.upper(), x.type) for i, x in enumerate(cache) if len(assignments.intersection({i-1, i, i+1})) == 0]
        kwargs = {cache[i-1].value.upper(): SpiceParser._cast(cache[i+1].value.upper(), cache[i+1].type) for i in assignments}
        
        args = [str(t) for t in args]
        
        return args, kwargs

    @staticmethod
    def _cast(val, ty='NUMBER'):
        if ty == 'EXPR':
            return val[1:-1]
        elif ty == 'NAME':
            return val
        # Attempt to cast number to float
        try:
            val = str2float(val)
        except ValueError:
            return val
        # Cast to int if possible
        return int(val) if val.is_integer() else val
    
    def _process_declaration(self, decl, args, kwargs):
        if decl == '.SUBCKT':
            # self._constraints = []
            name = args.pop(0)
            assert not(name in self.data), f"User is attempting to redeclare subcircuit {name}"
            subckt = Ckt(name=name)
            subckt.add_pins(args)
            # print('x',len(subckt.devices))
            
        
            self.data[name] = subckt
            self.temp_ckt= subckt
        
            # print('xx',len(self.temp_ckt.devices))
        elif decl == '.ENDS':
            # self._process_constraints()
            self.temp_ckt = None
        
        elif decl == '.PARAM':
            #TODO
            raise ValueError('.PARAM is not supported now in this version!')
            # assert len(args) == 0, f"unsupported arguments {args}, probably missing default values"
            # self._scope[-1].parameters.update({
            #     k.upper(): str(v).upper() for k, v in kwargs.items()
            # })
        
        #use a model file here to import model or create it by netlist?
        elif decl == '.MODEL':
            assert len(args) == 2, args
            # print(args)
            name, base = args[0], args[1]
            assert not(name in self.pdk_lib), f"User is attempting to redeclare {name}"
            self.pdk_lib[name] = PDK_Model(base, parameters=kwargs)


    def _process_instance(self, name, args, kwargs):
        
        #TODO for analog circuits with passive devices
        # defaults = {'C': 'CAP', 'R': 'RES', 'L': 'IND'}
        # if any(name.startswith(x) for x in ('C', 'R', 'L')):
        #     model = defaults[name[0]]
        #     if not kwargs:
        #         kwargs['VALUE'] = args.pop()
        #     else:  # to allow cap/res parameters
        #         model = args.pop()
        # else:
        #     model = args.pop()
        
        #make this part strict
        model_name = args.pop() #last of args, 
        # print(args)
        assert model_name in self.pdk_lib, 'model %s not find in pdk!'%(model_name)
        
        model = self.pdk_lib[model_name]
        # print(args)
        assert len(args) == len(model.model.pins()), \
            f"Model {model.name} has {len(model.pins)} pins {model.pins}. " \
            + f"{len(args)} nets {args} were passed when instantiating {name}."
        pins = {pin: net for pin, net in zip(model.model.pins(), args)}

        # try:
        # print(pins)
        self.temp_ckt.add_device(model.model(name=name, pins=pins, parameters=kwargs))
        # except ValueError:
        #     assert False, f"could not identify device parameters {name} {kwargs} \
        #         allowed parameters of model {model.name} are {model.parameters}"

    #TODO for analog constraints
    # def _process_constraints(self):
    #     with set_context(self._scope[-1].constraints):
    #         for const in self._constraints:
    #             self._scope[-1].constraints.append(eval(const, {}, constraint_dict))
    #     self._constraints = None



# deprecated
#klayout netlist loaders
'''
def load_netlist_kl(path):
   netlist = db.Netlist()
   netlist.case_sensitive = True #?
   spice_reader = db.NetlistSpiceReader(DeviceReader_kl())
   netlist.read(path, spice_reader)
   return netlist

#try import align netlist reader
def load_circuit_kl(netlist, circuit_name): 
   """ Load a transistor level circuit from a spice netlist.

   :netlist

   :return: Returns
   :raise: Raises an exception if the circuit is not found.
   """
      
   circuit = netlist.circuit_by_name(circuit_name)
   if circuit is None:
       raise Exception(f"Circuit not found: '{circuit_name}'")

   pins = [p.name() for p in circuit.each_pin()]
    
   # print(pins)
   # device = circuit.device_by_name(el+name)
       
       # d_type = device.device_class().name
       # if ('n' in d_type) or ('N' in d_type):
       #     device.set_parameter('Type', 0)
       # elif('p' in d_type) or ('P' in d_type):
       #     device.set_parameter('Type', 1)
       # else:
       #     raise ValueError('%s not known'%(d_type))
      
   mos4 = db.DeviceClassMOS4Transistor()
   id_gate_4 = mos4.terminal_id('G')#1
   id_source_4 = mos4.terminal_id('S')#0
   id_drain_4 = mos4.terminal_id('D')#2

   devices = []
   nets = []

   for d in circuit.each_device():
       if isinstance(d.device_class(), db.DeviceClassMOS3Transistor) \
           or isinstance(d.device_class(), db.DeviceClassMOS4Transistor):
               devices.append(
                   Transistor( get_device_type_kl(d),
                               d.net_for_terminal(id_source_4).name,
                               d.net_for_terminal(id_gate_4).name,
                               d.net_for_terminal(id_drain_4).name,
                               channel_width=int(d.parameter('W') + 0.5),  # Convert into micrometers.?not good here, lei
                               channel_length=int(d.parameter('L') + 0.5),  # Convert into micrometers.
                               name=d.name
                               ) )  
   for n in circuit.each_net():
       n_t = [[t.device().name, t.terminal_id()]for t in n.each_terminal()]
       nets.append(Net(n.name,n_t))
       
   return devices, pins, nets


class DeviceReader_kl(db.NetlistSpiceReaderDelegate):
    """
    self-defined device reader

    """

    def element(self, circuit, el, name, model, value, nets, params):
        """
        Signature: [virtual] bool element (Circuit ptr circuit, string element, string name, string model,
        double value, Net ptr[] nets, map<string,variant> parameters)
        Description: Makes a device from an element line
        e.x.
        <klayout.dbcore.Circuit object at 0x000002140A3E2A50> 
        M 20 MP15 0.0 [XR03DM:N_3, XR03DM:A, XR03DM:VDD, XR03DM:VDD] 
        {'AD': 0.0, 'AS': 0.0, 'L': 1.3e-07, 'M': 1.0, 'W': 4e-07}
        """
        # print('aaa',circuit,el,name,model,value,nets,params)
        new_params = {}
        for k in params:
            if k == 'w' or k == 'W':
                new_params['W'] = params[k]*1e3#super element will convert W/L from SI to um, but here want convert to nm
            elif k == 'l' or k == 'L':
                new_params['L'] = params[k]*1e3
            else:
                new_params[k] = params[k]
    
        super().element(circuit, el, el+name, model, value, nets, new_params)

        # device.set_parameter('W', params.get('W', 0) * 1e6)
        # device.set_parameter('L', params.get('L', 0) * 1e6)

        return True
    
def get_device_type_kl(device):
    # device = circuit.device_by_name(el+name)
        
    d_type = device.device_class().name
    if ('n' in d_type) or ('N' in d_type):
        return 'N'
    elif('p' in d_type) or ('P' in d_type):
        return 'P'
    else:
        raise ValueError('%s not known'%(d_type))
''' 

        


# def get_subcircuit_ports(file: str, subckt_name: str) -> List[str]:
#     """ Find port names of a subcircuit.
#     :param file: Path to the spice file containing the subcircuit.
#     :param subckt_name: Name of the subcircuit.
#     :return: List of node names.
#     """

#     _, sc = load_subcircuit(file, subckt_name)

#     pins = [p.name() for p in sc.each_pin()]

#     return pins



# def extract_transistors(circuit: db.Circuit, force_lowercase: bool = False) -> Tuple[List[Transistor], Set[str]]:
#     """ Load a transistor level circuit from a circuit.

#     :param path: The path to the netlist.
#     :param force_lowercase: Convert all net names to lower case letters.

#     Returns
#     -------
#     Returns a list of `Transistor`s and a list of the pin names including power pins.
#     (List[Transistors], pin_names)
#     """

#     f = lambda s: s
#     if force_lowercase:
#         f = lambda s: s.lower()

#     pins = [f(p.name()) for p in circuit.each_pin()]

#     def get_channel_type(s: str):
#         """Determine the channel type of transistor from the model name.
#         """
#         if s.lower().startswith('n'):
#             return ChannelType.NMOS
#         return ChannelType.PMOS

#     mos4 = db.DeviceClassMOS4Transistor()
#     id_gate_4 = mos4.terminal_id('G')
#     id_source_4 = mos4.terminal_id('S')
#     id_drain_4 = mos4.terminal_id('D')

#     transistors_klayout = []

#     for d in circuit.each_device():
#         if isinstance(d.device_class(), db.DeviceClassMOS3Transistor) \
#             or isinstance(d.device_class(), db.DeviceClassMOS4Transistor):
#                 transistors_klayout.append(
#                     Transistor(get_channel_type(d.device_class().name),
#                                f(d.net_for_terminal(id_source_4).name),
#                                f(d.net_for_terminal(id_gate_4).name),
#                                f(d.net_for_terminal(id_drain_4).name),
#                                channel_width=d.parameter('W') * 1e-6,  # Convert into micrometers.?not good here, lei
#                                channel_length=d.parameter('L') * 1e-6,  # Convert into micrometers.
#                                name=d.name
#                                ) )  



#     return transistors_klayout, set(pins)


# def _transistors2graph(transistors: Iterable[Transistor]) -> nx.MultiGraph:
#     """ Create a graph representing the transistor network.
#         Each edge corresponds to a transistor, each node to an electrical potential.
#     """
#     G = nx.MultiGraph()
#     for t in transistors:
#         G.add_edge(t.left, t.right, t)
#     assert nx.is_connected(G)
#     return G


# def _is_output_net(net_name, power_nets: Iterable, transistor_graph: nx.MultiGraph) -> bool:
#     """
#     Determine if the net is a driven output net which is the case if there is a path from the net
#     to a power rail.
#     :param net_name: The net to be checked.
#     :param power_nets: List of available power nets ["vdd", "gnd", ...].
#     :param transistor_graph:
#     :return: True, iff `net_name` is a OUTPUT net. False, iff it is a INOUT net.
#     """

#     return any((
#         nx.has_path(transistor_graph, net_name, pn)
#         for pn in power_nets
#     ))

