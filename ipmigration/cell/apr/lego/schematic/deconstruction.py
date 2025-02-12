# -*- coding: utf-8 -*-

from src.lego.graph import StructGraph 
from src.lego.struct import Struct

class CktDeconstruction:
    def __init__(self, tech_name, ckt, pin_map, structs_db, log, debug=False):
        self.tech_name = tech_name 
        self.ckt = ckt
        self.pin_map = pin_map
        self.classify_ckt() 
        self.structs = structs_db
        self.log = log
        self.debug = debug
        self.struct_array = {'match':[],'devices':[],'struct':[],'struct_t':[]}
    
    def __repr__(self):
        return str(self.struct_array['struct_t']) + ' ' + str(self.struct_array['struct'])
        
 
   
    def ckt_pin_map(self):
        net_map = {} # target to lego
        for p in self.ckt.pins:
            net_map[p] = self.pin_map[p]
        net_map_r = {v: k for k, v in  net_map.items()} #lego to target 
        return net_map,net_map_r
    
    @staticmethod
    def _add_net(net_map, net_map_r, nets):
        for a,b in nets.items():
            net_map[a] = b
            net_map_r[b] = a

    def match(self,devices_graph,struct_graph,pin_match):#p1:p2.p1 is pin in struct, p2 is pin in columns of pin align 
        matches = devices_graph.find_subgraph_matches(struct_graph)
        searched = []
        for match in matches:
            if len(pin_match) == 0:
                cond = True
            else:
                cond = False
            for p1,p2 in pin_match.items():
                pin1 = match[p1]
                pin2 = self.net_map_r[p2]
                if (pin1 == pin2):
                    cond = True
                else:
                    cond = False
                    break
            if cond:
                searched.append(match)       
        return searched
      
        
      
        
    def add_struct(self, struct_t, match_dict):
        for k,v in match_dict.items():
            self.struct_array[k].append(v)
        self.struct_array['struct_t'].append(struct_t)    


        
    def run(self):
        self.net_map,self.net_map_r = self.ckt_pin_map() 
        self.devices = self.ckt.devices.copy()   
             
        #1 CLK
        search_result,match_dict  = self.process_clk()
        if not(search_result):
            self.log.append('CLK search failed: %s %s '%(self.tech_name,self.ckt.name))    
            return False
        self.add_struct('CLK',match_dict)
        self.structs.remove_match(self.devices, match_dict['devices'])
        
        
        #2 OUT
        search_result,match_dict  = self.process_out()
        if not(search_result):
            self.log.append('OUT search failed: %s %s '%(self.tech_name,self.ckt.name))
            return False
        self.add_struct('OUT',match_dict)
        self.structs.remove_match(self.devices, match_dict['devices'])        
        # print(self.struct_array['match'])
        #3 
        # print('abc',self.devices)
        
        #3 INPUT
        #TODO process en mul se si syn reset...
        search_result,match_dict = self.process_input()
        if not(search_result):
            self.log.append('INPUT search failed: %s %s '%(self.tech_name,self.ckt.name))
            return False
        self.add_struct('INPUT',match_dict)
        self.structs.remove_match(self.devices, match_dict['devices'])   
    
        
        #4 Left Part
        search_result,match_dict  = self.structs.assemble(self.ckt,self.devices,self.log)
        # if self.ckt_type['type'] != 'SD':
        #     print('abc',self.ckt_type['type'] )
        #     raise ValueError
        if not(search_result):
            # substructs_find = self.structs.find_substruct_matches(self.devices)
            # print('Search failed, found searched:',self.ckt.name, substructs_find, 'input_type',self.input_type,self)
            # print('Left: %d devices. '%(len(self.devices)) ,self.devices)
            # print(match_dict['match'])
            self.log.append('STRUCT search failed: %s %s '%(self.tech_name,self.ckt.name))
            return False
        
        self.add_struct('STRUCT',match_dict)
        self.structs.remove_match(self.devices, match_dict['devices'])     

        # print('found searched:',self.ckt.name, self)
        #all passed
        self.deconstruction = {'STRUCT':[]}
        
        for i in range(len(self.struct_array['match'])):
            struct_type = self.struct_array['struct_t'][i]
            if struct_type != 'STRUCT':
                struct_ckt  = self.struct_array['struct'][i]
                devices     = self.struct_array['devices'][i]
                match_table = self.struct_array['match'][i]

                
                self.deconstruction[struct_type] = Struct(struct_type, struct_ckt[0], devices[0], match_table[0])
            else:
                struct_ckt  = self.struct_array['struct'][i]
                devices     = self.struct_array['devices'][i]
                match_table = self.struct_array['match'][i]
                for j in range(len(struct_ckt)):
                    self.deconstruction[struct_type].append(Struct(struct_type, struct_ckt[j], devices[j], match_table[j]))
        
        #
        
        #sort array
        struct_clk     = self.deconstruction['CLK']
        struct_out     = self.deconstruction['OUT']
        struct_input   = self.deconstruction['INPUT']
        
        self.net_cn = struct_clk.net_mapping['CN']
        self.net_c  = struct_clk.net_mapping['C']
        
        self.struct_out_in = [struct_out.net_mapping['IN1']]
        if 'IN2' in struct_out.net_mapping:
            self.struct_out_in.append(struct_out.net_mapping['IN2'])
        
        
        
        # self.dff1_input = [struct_input.net_mapping['OUT1']]
        # if 'OUT2' in struct_input.net_mapping:
        #     self.dff1_input.append(struct_input.net_mapping['OUT2'])
            
        count = 0
        struct_queue = []
        input_pin = struct_input.net_mapping['OUT1']
        while(1):
            for struct in self.deconstruction['STRUCT']:   
                if struct.net_mapping['IN1'] == input_pin:
                    struct_queue.append(struct)
                    input_pin = struct.net_mapping['OUT1']
                elif 'IN2' in struct.net_mapping:
                    if struct.net_mapping['IN2'] == input_pin:    
                            struct_queue.append(struct)
                            input_pin = struct.net_mapping['OUT1']                
                    
            count+=1
            if len(struct_queue) == len(self.deconstruction['STRUCT']):
                break
            if count > 10:
                print(self.struct_array)
                print(self.ckt.name,struct_queue, len(struct_queue), len(self.deconstruction['STRUCT']))
                raise ValueError
        # print(self.ckt.name, ' ;clk: ',struct_clk, ' ;out: ',struct_out, ' ;input: ',struct_input,  ' ;struct: ' ,struct_queue)
        self.struct_clk = struct_clk
        self.struct_out = struct_out
        self.struct_input = struct_input
        self.struct_queue = struct_queue
        
        return search_result
        



    def process_clk(self):

        clk1_ckt =  self.structs.clk_dict['CLK1']
        clk1_graph = StructGraph(clk1_ckt.devices)
        
        clk2_ckt =  self.structs.clk_dict['CLK2']
        clk2_graph = StructGraph(clk2_ckt.devices)
        
        devices_graph = StructGraph(self.devices)
        devices_dict = {t.name:t for t in self.devices} 
        # 

        search1 = self.match(devices_graph,clk2_graph,{'CK':self.clk_pin})
        if len(search1) == 1:
            devices = self.structs.graph_to_devices(search1[0],devices_dict)
            return True, {'match':[search1[0]], 'devices':[devices], 'struct': [clk2_ckt]  }
        else:
            search2 = self.match(devices_graph,clk1_graph,{'CK':self.clk_pin})    
            if len(search2) == 1:
                devices = self.structs.graph_to_devices(search2[0],devices_dict)
                return True, {'match':[search2[0]], 'devices':[devices], 'struct': [clk1_ckt]  }        
            else: 
                return False, {}

        self.net_cn = ''
        self.net_c = ''


    def process_out(self):
        #TODO add 3 inv structure
        
        #set or reset Q
        q_list = ['OUT_SR1','OUT_NOR2','OUT_NAND2','OUT_INV']
        q_ckts = [self.structs.output_dict[t] for t in q_list]
        
        
        # inv_graph = StructGraph(inv_ckt.devices)

        cg_list = ['OUT_NOR2','OUT_AND2','OUT_OR2','OUT_NAND2']
        cg_ckts = [self.structs.output_dict[t] for t in cg_list]
        
        devices_graph = StructGraph(self.devices)
        devices_dict = {t.name:t for t in self.devices}  

        search = []
        search_struct = []
        if self.ckt_type['type'] == 'CG':
            for cg_ckt in cg_ckts:
                cg_ckt_graph = StructGraph(cg_ckt.devices)
                match = self.match(devices_graph,cg_ckt_graph,{'OUT1':'ECK'})
                if len(match) == 1:
                    search.append(match[0])
                    search_struct.append(cg_ckt)
                    break
            # print(search_K_struct,self.ckt,self.tech_name)
        else:
            # Q,QN; Q; QN

            if 'Q' in self.net_map_r and 'QN' in self.net_map_r:
                q_list = ['OUT_2INV']
                q_ckts = [self.structs.output_dict[t] for t in q_list]
                for q_ckt in q_ckts:
                    q_ckt_graph = StructGraph(q_ckt.devices)
                    match = self.match(devices_graph,q_ckt_graph,{'OUT1':'Q','OUT2':'QN'})
                    if len(match) == 1:
                        search.append(match[0])
                        search_struct.append(q_ckt)
                        break
        
            elif 'QN' in self.net_map_r and not('Q' in self.net_map_r):
                for q_ckt in q_ckts:
                    q_ckt_graph = StructGraph(q_ckt.devices)
                    match = self.match(devices_graph,q_ckt_graph,{'OUT1':'QN'})
                    if len(match) == 1:
                        search.append(match[0])
                        search_struct.append(q_ckt)
                        break              
            elif 'Q' in self.net_map_r and not('QN' in self.net_map_r):
                for q_ckt in q_ckts:
                    q_ckt_graph = StructGraph(q_ckt.devices)
                    match = self.match(devices_graph,q_ckt_graph,{'OUT1':'Q'})
                    if len(match) == 1:
                        search.append(match[0])
                        search_struct.append(q_ckt)
                        break          
        
        
        
        if len(search) == 1:
            devices = self.structs.graph_to_devices(search[0],devices_dict)
            return True, {'match':[search[0]], 'devices':[devices], 'struct': [search_struct[0]] }    
        
        else:
            return False, {}
        
    def process_input(self):
        
        devices_graph = StructGraph(self.devices)
        devices_dict = {t.name:t for t in self.devices}  
        search = []
        search_struct = []
        
        if self.input_type == 0:
            input_list = ['INPUT_D0','INPUT_D1','INPUT_D2',
                           'INPUT_D3','INPUT_D4',
                          'INPUT_DR1','INPUT_DR1_2','INPUT_DR2','INPUT_DR3',
                          'INPUT_DS1','INPUT_DS2','INPUT_DS3','INPUT_DSR1']
            searched = False
            for inputs in self.structs.input_dict:
                if  inputs in input_list:
                    inputs_ckt = self.structs.input_dict[inputs]
                    inputs_ckt_graph = StructGraph(inputs_ckt.devices)
                    match = self.match(devices_graph,inputs_ckt_graph,{'D':'D'})
                    if len(match) >= 1:
                        searched = True
                        search.append(match[0])
                        search_struct.append(inputs_ckt)
                        break
                
            if not(searched):
                print('Type 0 input search failed: %s %s '%(self.tech_name,self.ckt.name))

                
        elif self.input_type == 1:
            #D SE SI
            input_list = ['INPUT_SD1','INPUT_SD2','INPUT_SD3','INPUT_SD4',
                          'INPUT_SD5','INPUT_SD6','INPUT_SD7','INPUT_SD8',
                          'INPUT_SDR1','INPUT_SDR2']
            searched = False
            for inputs in input_list:
                inputs_ckt = self.structs.input_dict[inputs]
                inputs_ckt_graph = StructGraph(inputs_ckt.devices)
                match = self.match(devices_graph,inputs_ckt_graph,{'D':'D','SE':'SE','SI':'SI'})
                if len(match) >= 1:
                    searched = True
                    search.append(match[0])
                    search_struct.append(inputs_ckt)
                    break
            if not(searched):
                print('Type 1 input search failed: %s %s '%(self.tech_name,self.ckt.name))
            else:
                pass
                # print('#Type 1 input search succeed: %s %s '%(self.tech_name,self.ckt.name),search_struct)
            
        elif self.input_type == 2:
            input_list = ['INPUT_ED1','INPUT_ED2','INPUT_ED3','INPUT_ED4',
                          'INPUT_EDR1','INPUT_EDR2','INPUT_EDR3','INPUT_EDR4']
            searched = False
            for inputs in input_list:
                inputs_ckt = self.structs.input_dict[inputs]
                inputs_ckt_graph = StructGraph(inputs_ckt.devices)
                match = self.match(devices_graph,inputs_ckt_graph,{'D':'D','E':'E'})
                if len(match) >= 1:
                    searched = True
                    search.append(match[0])
                    search_struct.append(inputs_ckt)
                    break
            if not(searched):
                print('Type 2 input search failed: %s %s '%(self.tech_name,self.ckt.name))

                
        elif self.input_type == 3:#not found
            input_list = ['INPUT_SDE1','INPUT_SDE2','INPUT_SDE3',
                          'INPUT_SDER1','INPUT_SDER2',
                          'INPUT_SDERS1']
            searched = False
            for inputs in input_list:
                inputs_ckt = self.structs.input_dict[inputs]
                inputs_ckt_graph = StructGraph(inputs_ckt.devices)
                match = self.match(devices_graph,inputs_ckt_graph,{'D':'D','E':'E','SE':'SE','SI':'SI'})
                if len(match) >= 1:
                    searched = True
                    search.append(match[0])
                    search_struct.append(inputs_ckt)
                    break
            if not(searched):
                print('Type 3 input search failed: %s %s '%(self.tech_name,self.ckt.name))
    
        elif self.input_type == 4:
            #['ECK','E'] 
            input_list = ['INPUT_D0','INPUT_D1','INPUT_D2',
                           'INPUT_D3','INPUT_D4','INPUT_DS2']
            searched = False
            for inputs in self.structs.input_dict:
                if  inputs in input_list:
                    inputs_ckt = self.structs.input_dict[inputs]
                    inputs_ckt_graph = StructGraph(inputs_ckt.devices)
                    match = self.match(devices_graph,inputs_ckt_graph,{'D':'E'})
                    if len(match) >= 1:
                        searched = True
                        search.append(match[0])
                        search_struct.append(inputs_ckt)
                        break
            if not(searched):
                print('Type 4 input search failed: %s %s '%(self.tech_name,self.ckt.name))

        elif self.input_type == 5:
            #D0,D1
            input_list = ['NAND2']
            searched = False
            for inputs in input_list:
                inputs_ckt = self.structs.input_dict[inputs]
                inputs_ckt_graph = StructGraph(inputs_ckt.devices)
                match = self.match(devices_graph,inputs_ckt_graph,{'A':'D0','B':'D1'})
                if len(match) >= 1:
                    searched = True
                    search.append(match[0])
                    search_struct.append(inputs_ckt)
                    break
            if not(searched):
                print('Type 5 input search failed: %s %s '%(self.tech_name,self.ckt.name))
         
        elif self.input_type == 6:
            #D0 D1 S0
            input_list = ['INPUT_MDR1']
            searched = False
            for inputs in input_list:
                inputs_ckt = self.structs.input_dict[inputs]
                inputs_ckt_graph = StructGraph(inputs_ckt.devices)
                match = self.match(devices_graph,inputs_ckt_graph,{})
                if len(match) >= 1:
                    searched = True
                    search.append(match[0])
                    search_struct.append(inputs_ckt)
                    break
            if not(searched):
                print('Type 6 input search failed: %s %s '%(self.tech_name,self.ckt.name))
        elif self.input_type == 7:
            pass
            # print('type', self.input_type)  
        elif self.input_type == 8:
            pass
            # print('type', self.input_type)  
        else:
            print('error!')  
        
        if len(search) == 1:
            devices = self.structs.graph_to_devices(search[0],devices_dict)
            return True, {'match':[search[0]], 'devices':[devices], 'struct': [search_struct[0]] }    
        
        else:
            return False, {}
    
    
    
    def classify_ckt(self):
        
        '''
        Try to delete this part as much as possible
        '''
        
        mapped_pins = []
        for p in self.ckt.pins:
            if not(p in self.pin_map):
                raise ValueError('Pin not found in pin map',self.tech_name,self.ckt.name,p,self.pin_map)
            else:
                p1 = self.pin_map[p]
                if p1 != 'VDD' and p1 != 'VSS':
                    mapped_pins.append(p1)        
        self.mapped_pins = mapped_pins
        self.ckt_type = {}

        
        
        
        
        
        c1 = 'Q'   in mapped_pins
        c2 = 'QN'  in mapped_pins
        c3 = 'D'   in mapped_pins
        c4 = 'CK'  in mapped_pins
        c5 = 'CKN' in mapped_pins
        c6 = 'ECK' in mapped_pins
        c7 = 'G'   in mapped_pins
        c8 = 'GN'  in mapped_pins
        c9 = 'SE'  in mapped_pins
        c10 = 'SI' in mapped_pins
        c11 = 'SN' in mapped_pins
        c12 = 'RN' in mapped_pins    
        c13 = 'E' in mapped_pins
        c14 = 'EN' in mapped_pins
        c15 = 'FC' in mapped_pins
        c16 = 'BC' in mapped_pins
        c17 = 'D0' in mapped_pins    
        c18 = 'D1' in mapped_pins  
        c19 = 'S0' in mapped_pins  
        
        # self.input_pins = {'D':c3, 'ECK':c4, '' }
        if c3 and not(c13) and not(c9) and not(c10):
            #single D
            self.input_type = 0
            self.input_pins=['D']
        elif  c3 and c9 and c10 and not(c13):
            #D SE SI
            self.input_type = 1
            self.input_pins=['D','SE','SI']
        elif c3 and c13 and not(c9) and not(c10):
            #D E 
            self.input_type = 2
            self.input_pins=['D','E']     
        elif  c3 and c9 and c10 and c13:
            #D E SE SI
            self.input_type = 3#
            self.input_pins=['D','E','SE','SI'] 
            
        
        
        elif c6 and c13:
            #ECK
            self.input_type = 4
            self.input_pins=['ECK','E']   
        elif c17 and c18 and not(c19)  and not(c9) and not(c10) :
            #D0,D1
            self.input_type = 5
            self.input_pins=['D0','D1'] 
        elif c17 and c18 and c19  and not(c9) and not(c10):
            self.input_type = 6
            self.input_pins=['D0','D1','S0'] 
        elif c17 and c18 and not(c19) and c9 and  c10:
            self.input_type = 7
            self.input_pins=['D0','D1','SE','SI'] 
        elif c17 and c18 and c19 and  c9 and c10:
            self.input_type = 8
            self.input_pins=['D0','D1','S0','SE','SI'] 
        else:
            print(self.mapped_pins) 
            raise ValueError()
        
        # print(t1) 
        
        
        #1 this may be weak
        if (c7 or c8) and not(c4 or c5):
            self.ckt_type['type'] = 'LA' #Latch
        elif (c4 or c5) and c6 and not(c3):
            self.ckt_type['type'] = 'CG' #clock gate
        elif (c9 or c10) and (c4 or c5):
            self.ckt_type['type'] = 'SD' #Scan DFF
        elif not(c7 or c8) and (c4 or c5):
            self.ckt_type['type'] = 'DF' #DFF
        else:
            print(mapped_pins)
            raise ValueError('LA DF SD CLK error')
        
        # clk
        if  self.ckt_type['type']  == 'LA':
            if c7:
                self.ckt_type['clk'] = 'H'
                self.clk_positive = True
                self.clk_pin = 'G'
            elif c8:
                self.ckt_type['clk'] = 'L'
                self.clk_positive = False
                self.clk_pin = 'GN'
            else:
                raise  ValueError('No G GN in LA error') 
        else:
            if c4:
                self.ckt_type['clk'] = 'R'
                self.clk_positive = True
                self.clk_pin = 'CK'
            elif c5:
                self.ckt_type['clk'] = 'F'
                self.clk_positive = False
                self.clk_pin = 'CKN'
            else:
                raise  ValueError('No G GN in LA error') 
        
        #out
        if c1 and c2:
            self.ckt_type['out'] = 'B'
        elif c1 and not(c2):
            self.ckt_type['out'] = 'Q'
        elif c2 and not(c1):
            self.ckt_type['out'] = 'N'
        else:
            if c6:
                self.ckt_type['out'] = 'K'
            else:
                print(mapped_pins)
                raise ValueError('Q, QN ECK error!')
  
        #SN RN
        if c11 and c12:
            self.ckt_type['set'] = ['RN','SN']
        elif c11 and not(c12):
            self.ckt_type['set'] = ['SN']
        elif c12 and not(c11):
            self.ckt_type['set'] = ['RN']
        elif not(c11) and not(c11):
            self.ckt_type['set'] = []
        else:
            raise  ValueError('B P C N error')
    
  
    
        # #5 enable
        # if c13 and not(c14):
        #     ee = 'E'
        # elif c14 and not(c13):
        #     ee = 'EN'
        # else:
        #     assert not(c13) and not(c14)
        #     ee = ''
        # #6 front control/ back control
        # if c15 and not(c16):
        #     ff = 'FC'
        # elif c16 and not(c15):
        #     ff = 'BC'
        # else:
        #     assert not(c15) and not(c16)
        #     ff = ''    
        # #7 multi-input
        # if c17 and c18 and c19:
        #     gg = 'MS'
        # elif c17 and c18 and not(c19):
        #     gg = 'M'
        # else:
        #     assert not(c17) and not(c18) and not(c19)
        #     gg = ''       
        
        # ckt_name = aa+bb+cc+dd
        
        # if ee != '':
        #     ckt_name = ckt_name + ee
        # if ff != '':
        #     ckt_name = ckt_name + ff
        # if gg != '':
        #     ckt_name = ckt_name + gg
        # self.ckt_type_name = ckt_name
        # self.ckt_type = {'type':aa, 'set':bb, 'clk':cc, 'out':dd, 'en':ee, 'ctrl':ff, 'mi':gg}
        

        
        # # inv_graph = StructGraph(inv_ckt.devices)

        # cg_list = ['NOR2','AND2','OR2','NAND2']
        # cg_ckts = [self.structs[t] for t in cg_list]
        
        # devices_graph = StructGraph(self.devices)
        # devices_dict = {t.name:t for t in self.devices}  
        
        # out_net = self.ckt_type['out']

        # search = []
        # search_struct = []
        # if out_net == 'K':
        #     for cg_ckt in cg_ckts:
        #         cg_ckt_graph = StructGraph(cg_ckt.devices)
        #         match = self.match(devices_graph,cg_ckt_graph,{'OUT':'ECK'})
        #         if len(match) == 1:
        #             search.append(match[0])
        #             search_struct.append(cg_ckt)
        #             break
        #     # print(search_K_struct,self.ckt,self.tech_name)
        # else:
        #     # Q,QN; Q; QN
        #     if 'Q' in self.net_map_r:
        #         for q_ckt in q_ckts:
        #             q_ckt_graph = StructGraph(q_ckt.devices)
        #             match = self.match(devices_graph,q_ckt_graph,{'OUT':'Q'})
        #             if len(match) == 1:
        #                 search.append(match[0])
        #                 search_struct.append(q_ckt)
        #                 break
        
        #     if 'QN' in self.net_map_r:
        #         for q_ckt in q_ckts:
        #             q_ckt_graph = StructGraph(q_ckt.devices)
        #             match = self.match(devices_graph,q_ckt_graph,{'OUT':'QN'})
        #             if len(match) == 1:
        #                 search.append(match[0])
        #                 search_struct.append(q_ckt)
        #                 break              
        
        # if len(search) == 1:
        #     devices = self.structs.graph_to_devices(search[0],devices_dict)
        #     return True, {'match':[search], 'devices':[devices], 'struct': [search_struct[0]] }    
        # elif len(search) == 2:
        #      devices1 = self.structs.graph_to_devices(search[0],devices_dict)
        #      devices2 = self.structs.graph_to_devices(search[1],devices_dict)
        #      return True, {'match':[search[0],search[1]], 'devices':[devices1, devices2], 'struct': [search_struct[0], search_struct[0]]}          
        # else:
        #     return False, {}
        




    # def process_latch(self):
    #     latch_list = ['LATCH1','LATCH1_SR','LATCH2_SR', 
    #                   'LATCH1_R','LATCH2_R','LATCH3_R',
    #                   'LATCH1_S']
        
    #     #must be exclusive
        
    #     struct_ckts = [self.structs[t] for t in latch_list]
    #     devices_graph = StructGraph(self.devices)
    #     devices_dict = {t.name:t for t in self.devices}  
        
    #     searched = []
    #     searched_struct= []
    #     for struct in struct_ckts:
    #         struct_graph = StructGraph(struct.devices)
    #         match = self.match(devices_graph,struct_graph,{})
    #         # xxxxx maybe left a inv here try give some margin
    #         if len(match) == 1:
    #             if len(match[0]) == len(devices_graph.nodes):
    #                 searched.append(match[0])
    #                 searched_struct.append(struct)
    #                 break
    #     if len(searched) == 1:
    #         devices = [[devices_dict[t] for t in searched[0].values() if t in devices_dict]]
    #         return True, {'match':searched, 'devices':devices, 'struct': searched_struct[0] }

    #     # pin_in = net_map['D']
    #     # pin_cn = net_map['CN']
    #     # pin_c  = net_map['C']
        
    
    #     return False,{}
 
    
    # def process_dff(self):
    #     latch_list = ['LATCH1','LATCH1_SR','LATCH2_SR', 
    #                   'LATCH1_R','LATCH2_R','LATCH3_R',
    #                   'LATCH1_S',
    #                   'DFF1']
        
    #     #must be exclusive
        
    #     struct_ckts = [self.structs[t] for t in latch_list]
    #     devices_graph = StructGraph(self.devices)
    #     devices_dict = {t.name:t for t in self.devices}  
        
    #     searched = []
    #     searched_struct= []
    #     for struct in struct_ckts:
    #         struct_graph = StructGraph(struct.devices)
    #         match = self.match(devices_graph,struct_graph,{})
    #         if len(match) == 1:
    #             if len(match[0]) == len(devices_graph.nodes):
    #                 searched.append(match[0])
    #                 searched_struct.append(struct)       
    #                 break
    #         # print(match,'abc',struct,self.ckt,self.tech_name)
    #         # if len(match) > 0:
    #         #     searched.append(match)
    #         #     searched_struct.append(struct)
    #     if len(searched) >0:
    #         devices = [[devices_dict[t] for t in searched[0].values() if t in devices_dict]]
    #         return True, {'match':searched, 'devices':devices, 'struct': searched_struct[0] }
    #     else:
    #         # print('test2', searched_struct,self.ckt,self.tech_name)
    #         # devices = [[devices_dict[t] for t in searched[0].values() if t in devices_dict]]
    #         # return True, {'match':searched, 'devices':devices, 'struct': searched_struct[0] }

    #         return False,{}
    # def process_sdff(self):
    #     return False,{}
   
    
    
    

# 








# class BaseStruct:
#     def __init__(self,ckt,devices,ckt_type, net_map, net_map_r):
#         self.ckt = ckt
#         self.devices = devices
#         self.ckt_type = ckt_type
#         self.struct_devices = []
#         self.net_map = net_map
#         self.net_map_r = net_map_r
        
#         self.devices_p = [t for t in devices if t.T == 'P']
#         self.devices_n = [t for t in devices if t.T == 'N']
     
    
#     def remove(self):
#         for d in self.struct_devices:
#             self.devices.remove(d)
#         if len(self.devices) == 0:
#             return True
#         else:
#             return False

# #1 clock structure    
# class CLK_Struct(BaseStruct):
#     def __init__(self,ckt, devices, ckt_type,  net_map, net_map_r):
#         super().__init__(ckt, devices, ckt_type,  net_map, net_map_r)
#         clk_net = ckt_type['clk']
#         if clk_net == 'H':
#             clk_pin = 'G'
#             positive = True
#         elif clk_net == 'L':
#             clk_pin = 'GN'    
#             positive = False
#         elif clk_net == 'R':
#             clk_pin = 'CK'
#             positive = True
#         elif clk_net == 'F':
#             clk_pin = 'CKN'
#             positive = False
#         else:
#             print(devices,ckt_type)
#             raise ValueError
        
#         self.positive = positive
#         self.clk_pin = clk_pin



#     def search(self):
        
#         #TODO use graph?
#         pin_name = self.net_map_r[self.clk_pin]
#         (pmos1,nmos1),inv1_out = search_inv(self.devices_p, self.devices_n, pin_name,pin_type = 'G')
#         (pmos2,nmos2),inv2_out = search_inv(self.devices_p, self.devices_n, inv1_out,pin_type = 'G')
#         # print('abc',inv1_out,inv2_out)
    
#         if len(pmos1) == 0 or len(nmos1) == 0:
#             return False, [[],[]]
#         else:
#             if len(pmos1) != 1 or len(nmos1) != 1:
#                 #TODO log it
#                 # print('1st clk not found', ckt,pmos1,nmos1)
#                 return False, [[],[]]
           
#         if len(pmos2) == 0 or len(nmos2) == 0:
#             return False, [[],[]]
#         else:
#             if len(pmos2) != 1 or len(nmos2) != 1:
#                 #TODO log it
#                 # print('2nd clk not found', ckt,pmos1,nmos1)
#                 return False, [[],[]]      
           
            
#         self.pmos1 = pmos1[0]
#         self.nmos1 = nmos1[0]
#         self.pmos2 = pmos2[0]
#         self.nmos2 = nmos2[0]       
        
#         self.struct_devices = [self.pmos1, self.nmos1, self.pmos2, self.nmos2]        
        
#         #if has pull struct (p->vdd ck net1; p->net1 c cn; n->cn ck vss)
#         pull_struct = []

#         for device_p in self.devices_p:
#             if device_p.G == pin_name:
#                 p_d_net,p_power = device_p.get_SD(with_power=False)
#                 if len(p_power) == 1:
#                     if device_p.get(p_power[0]) == 'VDD':
#                         for device_n in self.devices_n:
#                             if device_n.G == pin_name:
#                                 n_d_net,n_power = device_n.get_SD(with_power=False)
#                                 if len(n_power) == 1:  
#                                     if device_n.get(n_power[0]) == 'VSS':
#                                         for device_p2 in self.devices_p:
#                                             p2_sd_nets,n_power = device_p2.get_SD(with_power=False) 
#                                             if (len(p2_sd_nets) == 2) and (p_d_net[0] in p2_sd_nets) and (n_d_net[0] in p2_sd_nets):                        
#                                                 pull_struct = [device_p,device_p2,device_n]
#                                                 pull_out = n_d_net[0]
                                        
#         if len(pull_struct) == 0:
#             if self.positive:
#                 self.net_cn = inv1_out
#                 self.net_c = inv2_out
#             else:
#                 self.net_cn = inv2_out
#                 self.net_c = inv1_out               
#             return True,[[self.pmos1,self.nmos1],[self.pmos2,self.nmos2]]
#         else:
#             if self.positive:
#                 self.net_cn = pull_out
#                 self.net_c = inv2_out
#             else:
#                 self.net_cn = inv2_out
#                 self.net_c = pull_out             
#             self.struct_devices =  self.struct_devices + pull_struct
#             return True,[[self.pmos1,self.nmos1],[self.pmos2,self.nmos2],pull_struct]


# #2 out structure
# class OUT_Struct(BaseStruct):
#     def __init__(self, ckt, devices, ckt_type, net_map, net_map_r):
#         super().__init__(ckt, devices, ckt_type, net_map, net_map_r)
        
#         out_net = ckt_type['out']
#         if out_net == 'B':
#             out_pins = ['Q','QN']
#         elif out_net == 'Q':
#             out_pins = ['Q']    
#         elif out_net == 'N':
#             out_pins = ['QN']
#         elif out_net == 'K':
#             out_pins = ['ECK']
#         else:
#             print(devices,ckt_type)
#             raise ValueError
        
#         self.out_pins = out_pins

#     def search(self):
#         out_pins = [] #mapped pin
#         out_pins = [self.net_map_r[t] for t in self.out_pins]
    
#         pmos1 = []
#         nmos1 = []
#         pmos2 = []
#         nmos2 = []
        
#         if len(out_pins) == 1:
#             if out_pins[0] == 'K':
#                 print('ECK Found!')
#             else:
#                 (pmos1,nmos1),inv1_out = search_inv(self.devices_p, self.devices_n, out_pins[0],pin_type = 'SD')
#         elif len(out_pins) == 2:
#             (pmos1,nmos1),inv1_out = search_inv(self.devices_p, self.devices_n,  out_pins[0], pin_type = 'SD')
#             (pmos2,nmos2),inv2_out = search_inv(self.devices_p, self.devices_n,  out_pins[1], pin_type = 'SD')
#         else:
#             raise ValueError
    
#         if len(pmos1) == 0 or len(nmos1) == 0:
#             return False, [[],[]]
#         else:
#             if len(pmos1) != 1 or len(nmos1) != 1:
#                 #TODO log it
#                 # print('1st clk not found', ckt,pmos1,nmos1)
#                 return False, [[],[]]
        
#         if len(out_pins) == 2: 
#             if len(pmos2) == 0 or len(nmos2) == 0:
#                 return False, [[],[]]
#             else:
#                 if len(pmos2) != 1 or len(nmos2) != 1:
#                     #TODO log it
#                     # print('2nd clk not found', ckt,pmos1,nmos1)
#                     return False, [[],[]]      
           
#         if len(out_pins) == 1:
#             self.struct_devices = [pmos1[0], nmos1[0]]    
#             return True, [[pmos1[0],nmos1[0]]] 
            
#         elif len(out_pins) == 2:        
#             self.struct_devices = [pmos1[0], nmos1[0], pmos2[0], nmos2[0]]        
#             return True, [[pmos1[0], nmos1[0]],[pmos2[0], nmos2[0]]]

#         # if len(pull_struct) == 0:
#         # return True,[[self.pmos1,self.nmos1],[self.pmos2,self.nmos2]]



# # #3 and2        
# # class And2_Struct(BaseStruct):
# #     '''

# #     '''
    
    
# #     def __init__(self,ckt, devices, net_map, ckt_type):
# #         super().__init__(ckt,devices,net_map,ckt_type)


# #4 cross        
# class Latch1_Struct(BaseStruct):    
#     def __init__(self, ckt, devices, ckt_type, net_map, net_map_r, 
#                   struct_ckt, pin_in, pin_cn, pin_c):
#         super().__init__(ckt, devices, ckt_type, net_map, net_map_r)

#         self.pin_in =  pin_in
#         self.pin_cn = pin_cn
#         self.pin_c = pin_c
        
#         self.struct_ckt = struct_ckt
#         self.devices_graph = StructGraph(devices)
#         self.struct_graph = StructGraph(struct_ckt.devices)

#     def search(self):
#         matches = self.devices_graph.find_subgraph_matches(self.struct_graph)
#         for match in matches:
#             sub_pin_in = match['D']
#             sub_pin_cn = match['CN']
#             sub_pin_c = match['C']
#             if sub_pin_in == self.pin_in and sub_pin_cn == self.pin_cn and sub_pin_c == self.pin_c:
#                 return True
#         return False


