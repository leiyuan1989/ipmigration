# -*- coding: utf-8 -*-
"""
Created on Thu May 23 15:41:51 2024

@author: leiyuan
"""
import pandas as pd

class Ckt:
    def __init__(self, name, devices = None, pins= None):
        self.name = name 

        self.pins = []
        if pins:
            self.add_pins(pins)
        else:
            self.pins = []
        if devices:
            self.devices = devices               
        else:
            self.devices = []

        #TODO, think if need a pos or neg parameter 

        self.nets = {}
        
        self.pin_map = {}   #netlist to ascell
        self.pin_map_r = {} #ascell to netlist
        self.io_map = {}    #netlist to ascell
        self.io_map_r = {}  #ascell to netlist       
        self.ipins = {}
        self.ipins_r = {}        
        self.opins = {}
        self.opins_r = {}      
            
        self.ckt_type = 'undefined'
        self.clk_net = 'undefined'
        self.vdd_net = 'undefined'
        self.vss_net = 'undefined'
        self.vnw_net = 'undefined' #vdd
        self.vpw_net = 'undefined' #vss
        
        
    def add_device(self,device):
        self.devices.append(device)
        #refresh net or process together?
    
    def get_device(self,device_name):
        t1 = [t for t in self.devices if t.name == device_name]
        if len(t1) == 1:
            return t1[0]
        else:
            raise ValueError('Not found or found more than 1')
           
    def add_pins(self,pins):
        for p in pins:
            if is_ground_net(p):
                self.pins.append('VSS')        
            elif is_supply_net(p):
                self.pins.append('VDD')
            else:
                self.pins.append(p)
        #refresh net or process together?        
    
    def set_type(self, ckt_type):
        self.ckt_type = ckt_type
            
    def set_pin_map(self, pins_in, pins_out, pins_power,pins_clk):
        clock_nets = []
        for pin in self.pins:
            if pin in pins_in:
                self.pin_map[pin] = pins_in[pin] 
                self.io_map[pin] = pins_in[pin] 
                self.ipins[pin] = pins_in[pin] 
            elif pin in pins_out:
                self.pin_map[pin] = pins_out[pin] 
                self.io_map[pin] = pins_out[pin]    
                self.opins[pin] = pins_out[pin] 
            elif pin in pins_clk:
                self.pin_map[pin] = pins_clk[pin] 
                clock_nets.append(pin)
                # self.io_map[pin] = pins_clk[pin] 
            elif pin in pins_power:
                self.pin_map[pin] = pins_power[pin] 
                # self.io_map[pin] = pins_power[pin]             
            else:
                print(self.ckt_type,self.pins)
                raise ValueError(pin,pins_out)
        
        if len(clock_nets) == 1:    
            self.clk_net = clock_nets[0]
        elif len(clock_nets) == 0:  
            pass
        else:
            raise ValueError
        
        self.pin_map_r = self.inv_map(self.pin_map)
        self.io_map_r  = self.inv_map(self.io_map)    
        self.ipins_r = self.inv_map(self.ipins)
        self.opins_r = self.inv_map(self.opins)           
        
        self.vdd_net = self.pin_map_r['VDD']
        self.vss_net = self.pin_map_r['VSS']
        if 'VNW' in self.pin_map_r:
            self.vnw_net = self.pin_map_r['VNW']
        else:
            self.vnw_net = self.pin_map_r['VDD']
        if 'VPW' in self.pin_map_r:
            self.vpw_net = self.pin_map_r['VPW']
        else:
            self.vpw_net = self.pin_map_r['VSS']        
        
    
    @staticmethod
    def inv_map(maps):
        return {v: k for k, v in maps.items()}
    
    def __repr__(self):
        return "(%s, %d devices)"%(self.name, len(self.devices))
    
    def __len__(self):
        return len(self.devices)
    
    
    
    
    
    
    #move the following to cell    
    
    def find_device(self,device_name):
        t1 = [t for t in self.devices if t.name == device_name]
        if len(t1) == 1:
            return True
        elif len(t1) == 0:
            return False
        else:
            raise ValueError('Not found or found more than 1')     

    def extract_nets(self):
        #get nets, exclude B
        self.nets_cdl = {}
        for d in self.devices:
            for p, net in d.pins_dict.items():
                if p != 'B':
                    if net in self.nets_cdl:
                        self.nets_cdl[net].append((d,p))
                    else:
                        self.nets_cdl[net] = [(d,p)]

        nets_io_name = get_io_pins(self.pins)
        self.nets_cdl_io = {}
        self.nets_abutment = {}
        for name,net in self.nets_cdl.items():
            if name in nets_io_name:
                self.nets_cdl_io[name] = net
            if len(net) == 2:

                t1 = net[0][1]
                t2 = net[1][1]
                if type(net[0][0]) == type(net[1][0]):
                    if ((t1 == 'D') and (t2 == 'S')) or ((t2 == 'D') and (t1 == 'S')):
                        self.nets_abutment[name] = net         
 
        
    
    # def extract_adjacent(self):
    #     self.extract_nets()
    #     self.device_adjacent = {}
    #     for device in self.devices:
    #         self.device_adjacent[device.name] = {'G':device.G}
    #         if device.S != 'VDD' and device.S != 'VSS':
    #             self.device_adjacent[device.name]['S'] = []
    #             for dev,pin in self.nets_cdl[device.S]:
    #                 if dev.name != device.name:
    #                     self.device_adjacent[device.name]['S'].append(dev)
    #         else:
    #             self.device_adjacent[device.name]['S'] = device.S
            
    #         if device.D != 'VDD' and device.D != 'VSS':
    #             self.device_adjacent[device.name]['D'] = []
    #             for dev,pin in self.nets_cdl[device.D]:
    #                 if dev.name != device.name:
    #                     self.device_adjacent[device.name]['D'].append(dev)
    #         else:
    #             self.device_adjacent[device.name]['D'] = device.D         
            
            
            
 
    def preprocess(self,top_db_layout,db_layers):
        self.extract_nets()
        
        self.db_layout = top_db_layout.create_cell(self.name)
        self.db_shapes = {}
        for name in db_layers:
            self.db_shapes[name] = self.db_layout.shapes(db_layers[name]) 
        
        
    def sub_ckt(self, devices, remove=False):
        
        for device in devices:
            if not(device in self.devices):
                raise ValueError('sub devices not in ckt devices!')
        if remove:
            sub_devices = [t for t in self.devices if not(t in devices)]
        else:
            sub_devices = devices

        
        ckt = Ckt(self.name, devices = sub_devices, pins= self.pins)
        ckt.extract_nets()
        remove_pins = []
        for pin in ckt.pins:
            if not(pin in ckt.nets_cdl):
                remove_pins.append(pin)
        for pin in remove_pins:
            ckt.pins.remove(pin)
        ckt.extract_nets()
        return ckt

       
        # print(self.nets_abutment)
     
    #TODO add process here, only alert not equal w ones    
    def inspect_parallel(self):
        parallel_list = []
        for d1 in self.devices:
            for d2 in self.devices:
                if d1.name != d2.name:
                    # if d1.T ==d2.T and d1.W == d2.W and d1.L == d2.L and d1.G == d2.G: 
                    #TODO not condider different W
                    if d1.T ==d2.T and d1.L == d2.L and d1.G == d2.G:   
                        if (d1.S == d2.S and d1.D == d2.D) or (d1.S == d2.D and d1.D == d2.S):
                            find_parallel = False
                            for parallel in parallel_list:
                                if (d1 in parallel) and not(d2 in parallel):
                                    parallel.append(d2)
                                    find_parallel = True
                                elif (d2 in parallel) and not(d1 in parallel):
                                    parallel.append(d1)
                                    find_parallel = True
                                elif (d1 in parallel) and (d2 in parallel):
                                    find_parallel = True
                            if not(find_parallel):
                                parallel_list.append([d1,d2])

        if len(parallel_list) >0:
            print(parallel_list)
            raise ValueError('CKT: %s has parallel devices'%(self.name))

        
 


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

def is_power_net(net: str) -> bool:
    return is_ground_net(net) or is_supply_net(net)


def get_io_pins(pin_names):
    """ Get all pin names that don't look like power pins.
    """
    return [p for p in pin_names if not is_ground_net(p) and not is_supply_net(p)]


def get_cell_inputs(transistors):
    """Given the transistors of a cell find the nets connected only to transistor gates.
    Will not work for transmission gates.
    """

    transistors = [t for t in transistors if t is not None]

    gate_nets = set(t.gate_net for t in transistors)
    source_and_drain_nets = set(t.source_net for t in transistors) | set(t.drain_net for t in transistors)

    # Input nets are only connected to transistor gates.
    input_nets = gate_nets - source_and_drain_nets

    return input_nets
        
