from copy import deepcopy
# import numpy   
    
parameters_map = {
    'W':'W',
    'L':'L',
    'M':'M',
    'NF':'NF',
    'RO':'ROW',
    'CO':'COL'
    }
parameters_map_pin = {
    'RU':'RU',
    'RD':'RD'   }

class Device:
    def __init__(self,name,pins,parameters):
        self.name = name     
        self.init_pins = pins
        self.init_parameters_dict = parameters

   
class Pin(Device):
    def __init__(self, name, pins, parameters):
        super().__init__(name,pins,parameters)
        for key,value in pins.items():
            setattr(self,key,value)
        for key,value in parameters.items():
            if key in self.parameters_map():
                t = parameters_map[key]
                setattr(self,t,value)
             
    @staticmethod
    def pins():
         return  ['NET']      
    @staticmethod
    def parameters_map():
        return parameters_map_pin   

class Mos4(Device):
    """
    Abstract representation of a MOS transistor.
    """

    def __init__(self, name, pins, parameters,
                 allow_flip_source_drain = True
                 ):
        """
        params:
        left: Either source or drain net.
        right: Either source or drain net.
        """
        super().__init__(name,pins,parameters) 
        
        for key,value in pins.items():
            setattr(self,key,value)
        for key,value in parameters.items():
            if key in self.parameters_map():
                t = parameters_map[key]
                if t == 'W' or t == 'L':
                    # print(value,int(1e9*(value + 1e-15))) 
                    value = int(1e9*(value + 1e-15)) #to nm, add 1e-15 to solve case of 4.1999999999999995e-07->419
                setattr(self,t,value)
            
        if not('NF' in self.__dict__):
            self.NF = 1
  
        if not('M' in self.__dict__):
            self.M = 1
            
        for p in self.pins():
            net = self.__getattribute__(p)
            if is_ground_net(net):
                self.__setattr__(p,'VSS')         
            if is_supply_net(net):
                self.__setattr__(p,'VDD')       
        
        net = self.__getattribute__('B')
        if is_vnw_net(net):
            self.__setattr__('B','VNW')         
        if is_vpw_net(net):
            self.__setattr__('B','VPW')        
        
        
        self.left = None
        self.right = None
        self.pn_pair = None
        
        self.left_CT = []
        self.right_CT = []
        

        self.allow_flip_source_drain = allow_flip_source_drain

        # TODO
        self.threshold_voltage = None
    
    @staticmethod
    def pins():
        return  ['S','G','D','B']
    @staticmethod
    def parameters_map():
        return parameters_map     
    @property
    def pins_dict(self):  
        return  {t:self.__getattribute__(t) for t in self.pins()}
        
    # def copy(self):
    #     return  Mos4(self.t, 
    #                  self.s, 
    #                  self.g, 
    #                  self.d,
    #                  self.b,
    #                  self.w,
    #                  self.l,
    #                  number_fingers = self.nf,
    #                  name = self.name,
    #                  allow_flip_source_drain = self.allow_flip_source_drain
    #                  )

    def flipped(self, rt = False):
        """ Return the same transistor but with left/right terminals flipped.
        """
        if rt:
            new_d = self.copy()
            new_d.flipped()
            return new_d
        else:
        
            t = self.S
            self.S = self.D
            self.D = t
        

    def copy(self):
        
        return Mos4(self.name, self.init_pins, self.init_parameters_dict)

    def if_abutment(self,device, power=False):
        if power:
            pass
        else:
            if self.D != 'VDD' and self.D != 'VSS':
                if self.D in [device.D,device.S]:
                    return True
            if self.S != 'VDD' and self.S != 'VSS':
                if self.S in [device.D,device.S]:
                    return True            
            return False

    def scale(self,ratio, l):
        self.l = int(l)
        self.w = int(self.w/ratio - self.w/ratio%10)

    def get(self,pin_name):
        """ Return a tuple of all terminal names.
        :return:
        """
        return self.__getattribute__(pin_name)

    def get_SD(self,with_power=True):
        sd = [self.D,self.S]
        if with_power:
            return sd,[]
        else:
            if self.D == 'VDD':
                return [self.S],['D']
            elif self.S == 'VDD':
                return [self.D],['S']
            elif self.D == 'VSS':
                return [self.S],['D']
            elif self.S == 'VSS':
                return [self.D],['S']
            else:            
                return sd,[]

    # def __key(self):
    #     return self.name, self.channel_type, self.source_net, self.gate_net, self.drain_net, self.channel_width, self.threshold_voltage

    # def __hash__(self):
    #     return hash(self.__key())

    # def __eq__(x, y):
    #     return x.__key() == y.__key()

    def __repr__(self):
        return "({}, {}, {}):{}".format(self.S, self.G, self.D, self.name)


class PMos4(Mos4):
    """
    Abstract representation of a PMOS transistor.
    """

    def __init__(self, name, pins, parameters,
                 allow_flip_source_drain = True ):

        super().__init__(name, pins, parameters, allow_flip_source_drain) 
        self.T = 'P'

class NMos4(Mos4):
    """
    Abstract representation of a PMOS transistor.
    """

    def __init__(self, name, pins, parameters,
                 allow_flip_source_drain = True ):

        super().__init__(name, pins, parameters, allow_flip_source_drain) 
        self.T = 'N'








class Net:
    def __init__(self, name, terminal_list=[]):
        self.name = name
        self.terminal_list = terminal_list
    def add(self, terminal):  #terminal: (device,terminal)
        self.terminal_list.append(terminal)

    def __repr__(self):
        repr_ = ''
        for t in self.terminal_list:
            repr_ += t[0] +'->' + str(t[1]) + ' '
        return self.name + ':' + repr_



def is_ground_net(net: str) -> bool:
    """ Test if net is something like 'gnd' or 'vss'.
    """
    ground_nets = {0, '0', 'gnd', 'vss', 'vgnd'}
    return net.lower() in ground_nets

def is_supply_net(net: str) -> bool:
    """ Test if net is something like 'vcc' or 'vdd'.
    """
    supply_nets = {'vcc', 'vdd', 'vpwr'}
    return net.lower() in supply_nets

def is_vnw_net(net: str) -> bool:
    supply_nets = {'vcc', 'vdd', 'vpwr','vnw'}
    return net.lower() in supply_nets

def is_vpw_net(net: str) -> bool:
    ground_nets = {0, '0', 'gnd', 'vss', 'vgnd','vpw'}
    return net.lower() in ground_nets



# deprecated
# class Terminal:
#     def __init__(self, net, device = None, device_t = '', loc = (0,0)):
#         self.net = net
#         self.device = device
#         self.device_t = device_t
#         self.loc = loc
#         self.loc_canditates = []
        
#     def __repr__(self):
#         return 'net: %s, %s->%s '%(self.net,self.device,self.device_t)
        
#     def add(self, terminals):
#         pass


# #test
# t1 = list(netlist.each_circuit())                
# t2 = {}
# t3 = []
# for t in t1:
#     t2[t.name] = len(list(t.each_device()))
#     t3.append(t2[t.name])
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# d1 = pd.DataFrame(list(t2.items()),columns=['name','num'])
# d1 = d1.sort_values('num')
# plt.hist(t3, bins=30)
# plt.show()  


# d2 = d1.num.astype('category')
# num = []
# summ = 0
# for cat in d2.cat.categories:
#     t = d1[d1.num == cat]
#     # print(t.shape[0])
#     num.append(t.shape[0])
#     summ += t.shape[0]
#     print(summ)
