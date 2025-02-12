# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 20:34:48 2024

@author: leiyuan
"""
# from itertools import combinations,permutations
from src.schematic.deconstruction import Deconstruction
from src.schematic.placer import smt_place


class Placement:
    
    #TODO need consider all cells: both SL and CL
    def __init__(self, ckt,  ckts,  tech, log):        
        self.ckt  = ckt
        self.ckts = ckts
        self.tech = tech
        self.log  = log
        
        
        self.data = []
        self.gap = 6

    def place_sl(self,patterns):
        
        self.ckt_dc = Deconstruction(self.tech, self.ckt, self.ckts.pin_map, patterns, self.log) 
        self.ckt_dc.run()
        
        
        cross_data = []
        ports = {'P':[],'N':[]}
        
        if 'cross1' in self.ckt_dc.sub_ckts and 'backtrack1' in self.ckt_dc.sub_ckts:
            ports['P'].append(self.ckt_dc.sub_ckts['cross1'].place[0]['P'].S)
            ports['P'].append(self.ckt_dc.sub_ckts['cross1'].place[-1]['P'].D)
            ports['N'].append(self.ckt_dc.sub_ckts['cross1'].place[0]['N'].S)
            ports['N'].append(self.ckt_dc.sub_ckts['cross1'].place[-1]['N'].D)            
            
            
            # for i in range(self.gap):
            #     cross_data.append([None,None])
            # for col in self.ckt_dc.sub_ckts['cross1'].place:
            #     cross_data.append([col['P'],col['N']])
            # for i in range(self.gap):
            #     cross_data.append([None,None])
            
        
        if 'cross2' in self.ckt_dc.sub_ckts and 'backtrack2' in self.ckt_dc.sub_ckts:
            ports['P'].append(self.ckt_dc.sub_ckts['cross2'].place[0]['P'].S)
            ports['P'].append(self.ckt_dc.sub_ckts['cross2'].place[-1]['P'].D)
            ports['N'].append(self.ckt_dc.sub_ckts['cross2'].place[0]['N'].S)
            ports['N'].append(self.ckt_dc.sub_ckts['cross2'].place[-1]['N'].D)  
            
            # for i in range(self.gap):
            #     cross_data.append([None,None])
            # for col in self.ckt_dc.sub_ckts['cross2'].place:
            #     cross_data.append([col['P'],col['N']])
            # for i in range(self.gap):
            #     cross_data.append([None,None])
     
        if 'cross1' in self.ckt_dc.sub_ckts:
            p_devices = [t for t in self.ckt_dc.ckt.devices if t.T =='P']       
            n_devices = [t for t in self.ckt_dc.ckt.devices if t.T =='N']  
            
            print('abc',ports)
            
            sat,model = smt_place(p_devices, n_devices, ports)
            # self.model = model
            
            # if sat:
            #     for d in model.decls():
            #         if not('flip' in d.name()):
            #             device = self.ckt_dc.ckt.get_device(d.name())
            #             row = 0 if device.T == 'P' else 1
            #             col = model[d].as_long()
                
            #             cross_data[col][row] = device
            
    
            # self.data = cross_data
        
        
            # self.log.write('------------%s:%s %s-------------\n'%(self.tech,self.ckt.name,str(sat)))
            # self.log.write(str(self))
            # self.log.write('clk_n:%s, clk_p:%s, net_pm:%s, net_bm:%s\n'%(str(self.ckt_dc.clk_n),str(self.ckt_dc.clk_p),str(self.ckt_dc.net_pm),str(self.ckt_dc.net_bm)))
            # self.log.write(str(self.ckt_dc.rnsn_signal) + '\n')
            # line = '%d devices left: '%(len( self.ckt_dc.ckt.devices))
            # for d in self.ckt_dc.ckt.devices:
            #     line += str(d) + '  '        
            # self.log.write(line + '\n')
        


        
        return 0
    
    

         
    
    def place_cl(self):
        pass


    def load_from_pattern(self, pattern):
        # print(pattern_ckt,pattern_ckt.devices)
        for d in pattern.ckt.devices:
            p_d = pattern.pattern_ckt.get_device(pattern.device_map_r[d.name])
            col = p_d.COL + self.start 
            pn = d.T
            if self.data[col][pn]:
                # print(self.data,col,pn,device)
                raise ValueError('Two device with same type and col!')
            else:
                self.data[col][pn] = d     
            if self.end < col:
                self.end = col
                
    def find_devices(self, device):
        pass
        
    
    def __repr__(self):
        line_p = ''
        line_n = ''

        for p,n in self.data:
            if p == None and n == None:
                line_p += '   |'
                line_n += '   |'
            else:
                line_p += '%20s |'%(str(p))
                line_n += '%20s |'%(str(n))
   
        
        return line_p + '\n' + line_n + '\n'
        
    
    # @property
    # def chain(self):
    #     return self.data[self.start+1 : self.end+1]