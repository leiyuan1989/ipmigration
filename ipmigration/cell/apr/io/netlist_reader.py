# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""
import re
import collections
import logging

from ipmigration.cell.apr.cir.circuit  import Ckt
from ipmigration.cell.apr.cir.base  import PDK_Model

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




