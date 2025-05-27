# -*- coding: utf-8 -*-
import os
import time
import logging

import networkx as nx
from ipmigration.cell.apr.cir.graph import MosGraph
from ipmigration.cell.apr.cir.patterns import Pattern

logger = logging.getLogger(__name__)

DEBUG=False

class DeCKT:
    def __init__(self, ckt, patterns, tech_name, output_dir):
        self.init_ckt = ckt
        self.ckt = ckt.copy()
        self.patterns = patterns
        self.sub_ckts = {}
        self.tech_name = tech_name
        self.output_dir = output_dir
        
        #sl
        self.inv_nets = []
        self.input_nets = {k:[v] for k,v in self.init_ckt.pin_map_r.items()}
        self.input_control = False #if input D is processed. e.g. D with inv/D0 D1/D E/D Sync RNSN/D SE SI...    
        
        #key_nets
        self.data_net = {}
        self.m_net = 'undef'
        self.s_net = 'undef'
        
        # self.input_point = self.net_map_r[self.ckt_type['input_pins'][0]]
        # self.power_match_list = ['CROSS_NOD_2','CROSS_NOD_3','CROSS_NOD_P1']
        # self.struct_array = {'match':[],'devices':[],'struct':[],'struct_t':[]}
    
    
    # def __repr__(self):
    #     return str(self.struct_array['struct_t']) + ' ' + str(self.struct_array['struct'])
    
    def run(self):
        logger.info('%s, %s, %d devices'%(self.tech_name,self.ckt, len(self.ckt.devices)))
        aux_file = os.path.join(self.output_dir,'DEC_REPORT_%s.txt'%(time.strftime('%m_%d_%H_%M')))


        
        #Sequential logic processing
        if self.init_ckt.ckt_type in ['ff', 'scanff', 'latch', 'clockgate']:
            try:
                self.sequential_logic_processing()
                self.out_aux_netlist(aux_file, self.init_ckt, self.ckt, self.sub_ckts)  
            
                if len(self.ckt.devices) == 0:
                    return 1
                else:
                    print('-----Decompose Failed (Left Devices): %s-----'%(self.init_ckt.name))
                    return 0  
                
            except:
                print('-----Decompose Failed (Search Error): %s-----'%(self.init_ckt.name))
                self.out_aux_netlist(aux_file, self.init_ckt, self.ckt, self.sub_ckts)   
                return 0
    
            
            '''
            TODO: Bug: Add a mechanism for checking double parallel connections.
            E.g. VDD D net1 E net4
                 VDD D net2 E net4
                 VDD D net3 E net4
                The current consequence of this type of structure is the generation of a large number of matches.
            '''
            #5.2 second transmission gate if needed
            
            
            
            #pull up/down
          
         
            #left cells?
            #aux
           
            
            
        elif self.ckt.ckt_type in ['arithmetic','complex','multiplex']:
            pass
        else:
            raise ValueError('%s is not a right circuit type!'%(self.ckt.ckt_type))
        
        return False   
    

    def sequential_logic_processing(self):
        logger.info('-----%10s: %7s %5s %5s %5s'%(self.ckt.name, self.ckt.ckt_type, str(self.ckt.enable), str(self.ckt.mul_in),self.ckt.se_net))
        if self.init_ckt.ckt_type == 'clockgate':
            self.data_net = {'IN1':self.init_ckt.enable_net} 
        else:
            self.data_net = {'IN1':self.init_ckt.din_net} 
        #1. search clock patterns 
        self.sub_ckts['clk'] = self.search_clk(self.ckt, self.init_ckt )
        if not(self.sub_ckts['clk']):
            raise ValueError('CLK patterns are not found in netlist!')
        else:
            #remove device                 
            self.ckt = self.ckt.sub_ckt(self.sub_ckts['clk'].ckt.devices, remove=True)  
            #set key net c and cn:
            self.init_ckt.c_net = self.sub_ckts['clk'].net_map['C']
            self.init_ckt.cn_net = self.sub_ckts['clk'].net_map['CN']
            self.inv_nets.append((self.init_ckt.c_net,self.init_ckt.cn_net))
            
            logger.info('1. clock pattern: %s: %s'%(str(self.sub_ckts['clk']),'clk'))
        
        #2. search inputs inv
        inpins = ['D', 'E' ,'D0','D1','S0','RN','SN','SE','SI']
        inputs_inv = self.search_inputs_inv(inpins, self.ckt, self.init_ckt)
        for pin, patterns in inputs_inv.items():
            #one pin may have multiple inverters
            for i,pattern in enumerate(patterns):
                ckt_name = 'ininv_%s_%d'%(pin,i)
                net_name = '%s_N%d_net'%(pin,i)
                output_net = pattern.net_map['OUT1']
                self.input_nets[pin].append(output_net)
                self.sub_ckts[ckt_name] = pattern
                self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
                self.init_ckt.__setattr__(net_name,output_net)
                self.init_ckt.key_nets[net_name] = '%s_N%d'%(pin,i)
                logger.info('2. inputs inv pattern: %s: %s'%(str(pattern),ckt_name))
                if pin == 'D':
                    #input D with inverter
                    self.input_control = True
                    self.data_net = {'IN1':output_net}
                #
                if pin=='E' and self.init_ckt.ckt_type=='clockgate':
                    #input E with inverter
                    self.input_control = True
                    self.data_net = {'IN1':output_net}   
        
        #3. search output
        out_patterns, self.to_out_net = self.search_output(self.ckt, self.init_ckt)
        for pin, pattern in out_patterns.items():
            ckt_name = 'out_%s'%(pin)
            self.sub_ckts[ckt_name] = pattern
            self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
            logger.info('3. output pattern: %s: %s'%(str(pattern),ckt_name))
            # self.init_ckt.__setattr__(net_name,output_net)
            # self.init_ckt.key_nets[net_name] = '%s_N%d'%(pin,i)
        
        #4 process inputs that not a single D 
        #4.1 process input for more than 1 input: mul-d, d with e, e with se,
        pattern = self.search_multi_inputs(self.ckt, self.init_ckt)
        if pattern:
            # print(pattern)
            ckt_name = 'inputs'
            self.sub_ckts[ckt_name] = pattern
            self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
            logger.info('4.1 inputs(D0 D1 S0/D E/E SE) pattern: %s: %s'%(str(pattern),ckt_name))
            self.input_control = True
            self.data_net = {'IN1':pattern.net_map['OUT1']}
            if 'OUT2' in pattern.net_map:
                self.data_net['IN2'] = pattern.net_map['OUT2']
            
        #4.2 search_synchronous
        pattern = self.search_synchronous(self.ckt, self.init_ckt)
        if pattern:
            # print(pattern)
            ckt_name = 'sync'
            self.sub_ckts[ckt_name] = pattern
            self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
            logger.info('4.2 synchronous inputs(D with RN or SN) pattern: %s: %s'%(str(pattern),ckt_name))
            self.input_control = True
            self.data_net = {'IN1':pattern.net_map['OUT1']}
            if 'OUT2' in pattern.net_map:
                self.data_net['IN2'] = pattern.net_map['OUT2']
                
        #4.3 process SE and SI
        if self.init_ckt.ckt_type == 'scanff':
            pattern = self.search_scanff_inputs(self.ckt, self.init_ckt)
            if pattern:
                # print(pattern)
                ckt_name = 'sesi'
                self.sub_ckts[ckt_name] = pattern
                self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
                logger.info('4.3 inputs(D with SE or SI) pattern: %s: %s'%(str(pattern),ckt_name))
                self.input_control = True
                self.data_net = {'IN1':pattern.net_map['OUT1']}
                if 'OUT2' in pattern.net_map:
                    self.data_net['IN2'] = pattern.net_map['OUT2']

        #5 cross recognization
        #5.1 first transmission gate
        pattern,cross1_match = self.search_cross1(self.ckt, self.init_ckt)
        
        ckt_name = 'cross1'
        self.sub_ckts[ckt_name] = pattern
        self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
        self.init_ckt.pm0_net = cross1_match['PM0']
        self.init_ckt.m_net = cross1_match['M']
        if 'PM1' in cross1_match:
            self.init_ckt.__setattr__('pm1_net',cross1_match['PM1'])
            self.init_ckt.key_nets['pm1_net'] = 'PM1'
        logger.info('5.1 cross1 pattern: %s: %s'%(str(pattern),ckt_name))
        
        #5.2 back track1
        net_match = {'IN0':self.init_ckt.pm0_net,'OUT':self.init_ckt.m_net}
        if 'PM1' in cross1_match: 
            net_match['IN1'] = cross1_match['PM1']
        pattern = self.search_backtrack(self.ckt, self.init_ckt, **net_match)
        self.sub_ckts['backtrack1'] = pattern
        self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
        logger.info('5.2  back track 1 pattern: %s: %s'%(str(pattern),ckt_name))
        
        #5.3 cross2
        if self.init_ckt.ckt_type in ['ff', 'scanff']: 
            pattern,cross2_match = self.search_cross2(self.ckt, self.init_ckt,M=self.m_net)
            ckt_name = 'cross2'
            self.sub_ckts[ckt_name] = pattern
            self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
            self.init_ckt.bm0_net = cross2_match['BM0']
            self.init_ckt.s_net = cross2_match['S']
            if 'BM1' in cross2_match:
                self.init_ckt.__setattr__('bm1_net',cross2_match['BM1'])
                self.init_ckt.key_nets['bm1_net'] = 'BM1'
            logger.info('5.3 cross2 pattern: %s: %s'%(str(pattern),ckt_name))
            
            #5.4 back track2
            net_match = {'IN0':self.init_ckt.bm0_net,'OUT':self.init_ckt.s_net}
            if 'BM1' in cross2_match: 
                net_match['IN1'] = cross2_match['BM1']
            pattern = self.search_backtrack(self.ckt, self.init_ckt, **net_match)
            self.sub_ckts['backtrack2'] = pattern
            self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
            logger.info('5.4  back track 2 pattern: %s: %s'%(str(pattern),ckt_name))
           
    
    
    
    #match two graph with net match
    def match(self,devices_graph,struct_graph, net_match, nopower=False):
        #{p1:p2,...} :p1 is pin in pattern, p2 ckt net 
        if nopower:
            matches = devices_graph.find_subgraph_matches(struct_graph)
    
        else:

            matches = devices_graph.find_subgraph_matches(struct_graph,
                                                          node_match=MosGraph.node_match_power,
                                                          edge_match=MosGraph.edge_match_power)
        searched = []
        for match in matches:
            if len(net_match) == 0:
                cond = True
            else:
                cond = False
            for p1,p2 in net_match.items(): 
                if p1 in match:
                    p1 = match[p1]  
                    if (p1 == p2):
                        cond = True
                    else:
                        cond = False
                        break
            if cond:
                searched.append(match)       
        return searched
    
    #search inv
    def search_inv(self, devices_graph, IN1=None, OUT1=None):
        inv_graph = self.patterns.ckt_graph['INV']  
        net_match = {}
        if IN1:
            net_match['IN1']=IN1
        if OUT1:
            net_match['OUT1']=OUT1              
        matches = self.match(devices_graph,inv_graph,net_match,nopower=False)
        return matches  

    # #search output
    # def search_output(self, devices_graph, IN1=None, OUT1=None):
    #     inv_graph = self.patterns.ckt_graph['INV']  
    #     net_match = {}
    #     if IN1:
    #         net_match['IN1']=IN1
    #     if OUT1:
    #         net_match['OUT1']=OUT1              
    #     matches = self.match(devices_graph,inv_graph,net_match,nopower=False)
    #     return matches      
    
    
    
    
    
    #search logic
    def search_logic(self, devices_graph, input_map=None, ouput_map=None, input_num=2):
        #e.g. inputs {'IN1':xxx,'IN2':xxx, ...}
        net_match = {}
        input_pins = ['IN1','IN2','IN3','IN4','IN5','IN6','IN7','IN8']
        output_pins = ['OUT1','OUT2','OUT3','OUT4']
        if input_map:
            for k,v in input_map.items():
                assert k in input_pins, k
                net_match[k]=v                
        if ouput_map:
            for k,v in ouput_map.items():
                assert k in output_pins, k
                net_match[k]=v   
        
        if input_num == 2:
            logic_dict = self.patterns.logic2_dict
        elif input_num == 3:
            logic_dict = self.patterns.logic3_dict
        elif input_num == 4:
            logic_dict = self.patterns.logic4_dict        
        else:
            raise ValueError('input number is not correct')
        result = []
        for ckt_name, ckt in logic_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
            # print(matches,ckt_name)
            # print(matches,net_match)
            if matches:
                result.append([ckt_name, matches])
            
        return result
    
    #search fcross
    def search_fcross(self, devices_graph, D=None, D1=None,nopower=False,aug=False):
        fcross_dict = self.patterns.fcross_dict
        if aug:
            fcross_dict = self.patterns.fcross_aug_dict
        #e.g. inputs {'IN1':xxx,'IN2':xxx, ...}
        net_match = {}
        if D:
            net_match['D']=D
        if D1:
            net_match['D1']=D1
        
        result = []
        for ckt_name, ckt in fcross_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = self.match(devices_graph,ckt_graph,net_match,nopower=nopower)
            if matches:
                result.append([ckt_name, matches])
        return result    

    #search pcross
    def search_pcross(self, devices_graph, IN1=None, IN2=None, D1=None,nopower=False,aug=False):
        pcross_dict = self.patterns.pcross_dict
        if aug:
            pcross_dict = self.patterns.pcross_aug_dict
        net_match = {}
        if IN1:
            net_match['IN1']=IN1
        if IN2:
            net_match['IN2']=IN2
        if D1:
            net_match['D1']=D1           
        result = []
        for ckt_name, ckt in pcross_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = self.match(devices_graph,ckt_graph,net_match,nopower=nopower)
            if matches:
                result.append([ckt_name, matches])
        return result 
    
    
    #search rsn cross
    def search_rscross(self, devices_graph, is_rn,is_sn, IN1=None, IN2=None, D=None,nopower=False):
        net_match = {}
        if D: 
            net_match['D']=D    
            if is_rn and is_sn:
                rs_key = 'FRS'
            elif is_rn:
                rs_key = 'FR'
            elif is_sn:
                rs_key = 'FS'
            else:
                raise ValueError()
                
        elif IN1:
            net_match['IN1']=IN1
            if IN2:
                net_match['IN2']=IN2
                
            if is_rn and is_sn:
                rs_key = 'PRS'
            elif is_rn:
                rs_key = 'PR'
            elif is_sn:
                rs_key = 'PS'
            else:
                raise ValueError()
        else:
            raise ValueError
        
        pattern = self.patterns.rscross_dict[rs_key]            
        result = []
        for ckt_name, ckt in pattern.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            
            matches = self.match(devices_graph,ckt_graph,net_match,nopower=nopower)
            if matches:
                result.append([ckt_name, matches])
        return result     
    
    
    
    
    @staticmethod
    def get_out_match(match):
        out_match={}
        output_pins = ['OUT1','OUT2','OUT3','OUT4']
        for pin in output_pins:
            if pin in match:
                out_match[pin] = match[pin]
        return out_match
    
    
    
    #search input with D and E 
    def search_input_ed(self, devices_graph, D, E):
        search_result = self.search_fcross(devices_graph, D=D)
        result = []
        #get E EN and OUT1 OUT2
        for ckt_name, matches in search_result:
            for match in matches:
                if match['E'] == E: #if E_N should be taken into account
                    out_match = self.get_out_match(match)
                    result.append([ckt_name,match,out_match]) 
        if len(result)>1 or len(result)==0:
            print(result)
            print('Warning! input ed search error!')
            return 0
        return result[0]
        
        
    #search input with D0 and D1 or S0
    def search_input_md(self, devices_graph, D0, D1, S0):
        result = []
        if S0 == 'undef':
            result1 = self.search_logic(devices_graph, input_map={'IN1':D0,'IN2':D1})
            result2 = self.search_logic(devices_graph, input_map={'IN1':D1,'IN2':D0})
            if len(result1)==1 and len(result2)==0:
                result = result1
            elif len(result1)==0 and len(result2)==1:
                result = result2
            else:
                print(result1,result2)
                #TODO: change to warning
                raise ValueError('Warning! input ed is not searched')
            ckt_name,matches = result[0]    
            assert len(matches)==1,matches
            match = matches[0]
            out_match = self.get_out_match(match)
            return [ckt_name, match, out_match]
        else:
            result = self.search_fcross(devices_graph, D=D0, D1=D1)
            if len(result) == 1:
                pass
            else:
                print(result)
                raise ValueError('Warning! input md is not searched')
                
            ckt_name,matches = result[0]    
            assert len(matches)==1,matches
            match = matches[0]
            out_match = self.get_out_match(match)
            return [ckt_name, match, out_match]

        
    #search input with E and SE
    def search_input_ese(self, devices_graph, E, SE):
        result1 = self.search_logic(devices_graph, input_map={'IN1':E, 'IN2':SE})
        result2 = self.search_logic(devices_graph, input_map={'IN1':SE,'IN2':E})
        if len(result1)==1 and len(result2)==0:
            result = result1
        elif len(result1)==0 and len(result2)==1:
            result = result2
        else:
            print(result1,result2)
            #TODO: change to warning
            raise ValueError('Warning! input ed is not searched')
        ckt_name,matches = result[0]    
        assert len(matches)==1,matches
        match = matches[0]
        out_match = self.get_out_match(match)
        return [ckt_name, match, out_match]        
     
    
    #search patterns
    #search clk pattern
    def search_clk(self,ckt,master_ckt):
        clk1_ckt   = self.patterns.clk_dict['CLK1']   
        clk1_graph = self.patterns.ckt_graph['CLK1']
        clk2_ckt   = self.patterns.clk_dict['CLK2']
        clk2_graph = self.patterns.ckt_graph['CLK2']    
        devices_graph = MosGraph(ckt)
        # devices_dict = {t.name:t for t in self.ckt.devices} 
        matches = self.match(devices_graph,clk2_graph,{'CK': self.ckt.clk_net})
        if len(matches) == 1:
            search = matches[0]
            clk_ckt = clk2_ckt
        else:
            matches = self.match(devices_graph,clk1_graph,{'CK': self.ckt.clk_net})    
            if len(matches) == 1:
                search = matches[0]  
                clk_ckt = clk1_ckt
            else: 
                search = None
                clk_ckt = None
        if search:
            pattern = Pattern(clk_ckt, master_ckt, search)
            return pattern
        else:
            return None
            # raise ValueError('CLK patterns are not found in netlist!')        
            
    #search input inv pattern
    def search_inputs_inv(self, pins, ckt, master_ckt):
        devices_graph = MosGraph(ckt)
        inv_ckt   = self.patterns.ckt_dict['INV'] 
        inputs_inv = {}
        for k,v in master_ckt.ipins.items():#v:ascell k:netlist
            if v in pins:
                matches = self.search_inv(devices_graph, IN1=k)
                if len(matches)>0:
                    patterns = []
                    for match in matches:
                        patterns.append(Pattern(inv_ckt, master_ckt, match))
                        self.inv_nets.append((k,match['OUT1']))
                    inputs_inv[v] = patterns
                                        
        return inputs_inv
    
        
    #search out patterns
    def search_output(self, ckt, master_ckt):
        devices_graph = MosGraph(ckt)
        inv_ckt  = self.patterns.ckt_dict['INV'] 
        out_patterns = {}
        for k,v in master_ckt.opins.items():
            # print('test1',master_ckt.opins)
            if v == 'Q' or v == 'QN':
                matches = self.search_inv(devices_graph, OUT1=k)
                if len(matches)>0:
                    assert len(matches) == 1, 'multi-inv to Q/QN'
                    match = matches[0]
                    out_patterns[v] = Pattern(inv_ckt, master_ckt,match)    
                    in_net = match['IN1']
                    self.inv_nets.append((in_net,k))
                    
                    #next inv search
                    if len(master_ckt.nets[in_net])==4:
                        matches = self.search_inv(devices_graph, OUT1=in_net)
                        if len(matches)==1 :
                            match = matches[0]
                            out_patterns[v+'_2'] = Pattern(inv_ckt, master_ckt,match)    
                            next_in_net = match['IN1']
                            self.inv_nets.append((next_in_net,in_net))  
                else:
                    #not inv output,DFBRQ1 153
                    result = self.search_logic(devices_graph, ouput_map={'OUT1':k},input_num=3)
                    if result:
                        ckt_name,matches = result[0]
                        ckt =  self.patterns.ckt_dict[ckt_name]
                        out_patterns[v] = Pattern(ckt, master_ckt, matches[0])
                    else:
                        result = self.search_logic(devices_graph, ouput_map={'OUT1':k},input_num=2)
                        if result:
                            ckt_name,matches = result[0]
                            ckt =  self.patterns.ckt_dict[ckt_name]
                            out_patterns[v] = Pattern(ckt, master_ckt, matches[0])
                            
                            
                            
            
            elif v == 'ECK':
                result = self.search_logic(devices_graph, ouput_map={'OUT1':k})
                ckt_name,matches = result[0]
                ckt =  self.patterns.ckt_dict[ckt_name]
                out_patterns[v] = Pattern(ckt, master_ckt, matches[0])
                # TODO: consider below part
                # logic_di and matches may have many items 
                # out_patterns[v] = []
                # for match in matches:
                #     out_patterns[v].append(Pattern(ckt, master_ckt, match))
            else:
                raise ValueError('%s is not output pin'%(v))
        #TODO: search inv chains
        to_out_net = {}
        return out_patterns, to_out_net
            

    def search_multi_inputs(self, ckt, master_ckt):
        #'ff', 'scanff', 'latch', 'clockgate'
        devices_graph = MosGraph(ckt)
        if master_ckt.ckt_type in ['latch', 'ff', 'scanff']:
            if master_ckt.enable:
                result = self.search_input_ed(devices_graph, master_ckt.din_net, master_ckt.enable_net)
                if result:
                    ckt_name,match,out_match = result
                    ckt =  self.patterns.ckt_dict[ckt_name]
                    return Pattern(ckt, master_ckt, match)
                else:
                    #153:LANHT1
                    return None
            if master_ckt.mul_in:
                result = self.search_input_md(devices_graph, 
                                              master_ckt.md0_net, 
                                              master_ckt.md1_net, 
                                              master_ckt.ms0_net)    
                ckt_name,match,out_match = result
                ckt =  self.patterns.ckt_dict[ckt_name]
                return Pattern(ckt, master_ckt, match)

        if master_ckt.ckt_type == 'clockgate':
            if master_ckt.se_net != 'undef': #clockgate without SE is not mutiple inputs
                result = self.search_input_ese(devices_graph, 
                                          E =master_ckt.enable_net, 
                                          SE=master_ckt.se_net)
                ckt_name,match,out_match = result
                ckt =  self.patterns.ckt_dict[ckt_name]
                return Pattern(ckt, master_ckt, match)
                  
            
        return None
    
    def search_synchronous(self, ckt, master_ckt): 
        is_rn = master_ckt.rn
        is_sn = master_ckt.sn
        if is_rn or is_sn:
            devices_graph = MosGraph(ckt)
            d_net = self.input_nets['D']
            result = []
            if is_rn and is_sn:
                rsn_net = self.input_nets['RN'] + self.input_nets['SN']
            else:
                #only rn or sn
                if is_rn:
                    rsn_net = self.input_nets['RN']
                else:
                    rsn_net = self.input_nets['SN']
                search_results = self.search_logic(devices_graph)  
                if len(search_results)>0:
                    for ckt_name, matches in search_results:
                        for match in matches:
                            in1 = match['IN1']
                            in2 = match['IN2']
                            c1 = (in1 in d_net) and (in2 in rsn_net)
                            c2 = (in2 in d_net) and (in1 in rsn_net)
                            if c1 or c2:
                                result.append([ckt_name,match])
            if len(result)>0:
                assert len(result) == 1,result
                ckt_name, match = result[0]
                pattern_ckt =  self.patterns.ckt_dict[ckt_name]
                # print('%%%%%%%%%%%found%%%%%%%%%%')
                return Pattern(pattern_ckt, master_ckt, match)
            else:
                return None
        else:
            return None
                        

    def search_asynchronous(self, ckt, master_ckt, input_net=None): 
        is_rn = master_ckt.rn 
        is_sn = master_ckt.sn
        devices_graph = MosGraph(ckt)
        
        if self.input_control:
            data_net = self.data_net
        else:
            data_net = {'D':self.data_net['IN1']}
        if input_net:
            data_net = input_net
     
        result = self.search_rscross(devices_graph, is_rn,is_sn,**data_net)
        return result
    
    def search_scanff_inputs(self, ckt, master_ckt):   
        SI = master_ckt.si_net
        SE = master_ckt.se_net       
        assert SE != 'undef' and SI != 'undef'
        devices_graph = MosGraph(ckt)
        if self.input_control:
            search_result = self.search_pcross(devices_graph, D1=SI)
            if len(search_result) == 1:
                ckt_name, matches = search_result[0]
                assert len(matches) == 1,matches
                match = matches[0]
                pattern_ckt =  self.patterns.ckt_dict[ckt_name]
                return Pattern(pattern_ckt, master_ckt, match)
                
            else:
                print(search_result)
                print('scanff no found, multi-d')
        else:
            search_result = self.search_fcross(devices_graph, D1=SI)
            if len(search_result) >= 1:
                ckt_name, matches = search_result[0] #only first 
                # assert len(matches) == 1,matches only first matches
                
                match = matches[0]
                pattern_ckt =  self.patterns.ckt_dict[ckt_name]
                return Pattern(pattern_ckt, master_ckt, match)
            else:
                # print([[t[0],len(t[1])] for t in search_result])
                print('scanff no found, single-d')
                # raise ValueError('Warning! input md is not searched')
        
                
    def search_cross1(self, ckt, master_ckt):
        devices_graph = MosGraph(ckt)
    
        if self.input_control:
            search_result = self.search_pcross(devices_graph,**self.data_net)
            
            # print('test1',len(search_result))
            if len(search_result) ==0:
                search_result = self.search_fcross(devices_graph,D=self.data_net['IN1'])            
        else:
            search_result = self.search_fcross(devices_graph,D=self.data_net['IN1'])
        
        if len(search_result) == 0:
            if master_ckt.rn or master_ckt.sn:
                search_result = self.search_asynchronous(ckt, master_ckt)        
            else:
                raise ValueError
        if len(search_result)>0:
            ckt_name, matches = search_result[0]
            match = matches[0] #may have many matches
            out_match = {'M':match['D1'], 'PM0':match['OUT1']}
            if 'OUT2' in match:
                out_match['PM1'] = match['OUT2']
            self.m_net = match['D1']
            pattern_ckt =  self.patterns.ckt_dict[ckt_name]
            pattern =  Pattern(pattern_ckt, master_ckt, match)
            return [pattern,out_match]
            # if len(matches)>1:
            #     print('muti-matches',ckt_name, len(matches))
        else:
            print(master_ckt.key_net_mapping)
            print('Searched %d'%(len(search_result)),search_result[0][0])            
            assert len(search_result)>0

    def search_cross2(self, ckt, master_ckt, M):
        devices_graph = MosGraph(ckt)

        search_result = self.search_pcross(devices_graph, IN1=M)
        if len(search_result) ==0:
                search_result = self.search_fcross(devices_graph,D=M)            
        if len(search_result) == 0:
            if master_ckt.rn or master_ckt.sn:
                input_net = {'D':M} #for FSC
                search_result = self.search_asynchronous(ckt,master_ckt,input_net=input_net)        
                if len(search_result) == 0:
                    input_net = {'IN1':M} #for PSC
                    search_result = self.search_asynchronous(ckt,master_ckt,input_net=input_net)
        
        
        
        if len(search_result) == 0:   
            search_result = self.search_pcross(devices_graph, IN1=M,aug=True)
            # if len(search_result)>0:
            #     print('&&&&&&&&&&&&&&&Success')
        if len(search_result) ==0:
            search_result = self.search_fcross(devices_graph,D=M,aug=True)            
            # if len(search_result)>0:
            #     print('&&&&&&&&&&&&&&&Success')
        if len(search_result)>0:
            ckt_name, matches = search_result[0]
            match = matches[0] #may have many matches
            out_match = {'S':match['D1'], 'BM0':match['OUT1']}
            if 'OUT2' in match:
                out_match['BM1'] = match['OUT2']
            self.s_net = match['D1']
            pattern_ckt =  self.patterns.ckt_dict[ckt_name]
            pattern =  Pattern(pattern_ckt, master_ckt, match)
            return [pattern,out_match]
        else:
            raise ValueError
            

    def search_backtrack(self, ckt, master_ckt, IN0, OUT, IN1=None):
        devices_graph = MosGraph(ckt)
        if master_ckt.rn or master_ckt.sn:
            #search backtrack with RN SN
            inputs = [IN0]
            if IN1:
                inputs.append(IN1)
            if master_ckt.rn:
                inputs += self.input_nets['RN']
            if master_ckt.sn:
                inputs += self.input_nets['SN'] 
            
            result = []              
            net_match = {'OUT1':OUT}
            #search 3 inputs
            for ckt_name, ckt in self.patterns.backtrack3_dict.items():
                ckt_graph = self.patterns.ckt_graph[ckt_name] 
                matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
                if matches:
                    for match in matches:
                        bt_inputs = [match['IN1'],match['IN2'],match['IN3']]
                        if set(bt_inputs)<=set(inputs):
                            result.append([ckt_name, match])   
            #search 3 inputs aug
            if len(result)==0:
                for ckt_name, ckt in self.patterns.backtrack3_aug_dict.items():
                    ckt_graph = self.patterns.ckt_graph[ckt_name] 
                    matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
                    if matches:
                        for match in matches:
                            bt_inputs = [match['IN1'],match['IN2'],match['IN3']]
                            if set(bt_inputs)<=set(inputs):
                                result.append([ckt_name, match])                      
            #search 2 inputs
            for ckt_name, ckt in self.patterns.backtrack2_dict.items():
                ckt_graph = self.patterns.ckt_graph[ckt_name] 
                matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
                if matches:
                    for match in matches:
                        bt_inputs = [match['IN1'],match['IN2']]
                        if set(bt_inputs)<=set(inputs):
                            result.append([ckt_name, match])   
            #search 2 inputs aug
            if len(result)==0:
                for ckt_name, ckt in self.patterns.backtrack2_aug_dict.items():
                    ckt_graph = self.patterns.ckt_graph[ckt_name] 
                    matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
                    if matches:
                        for match in matches:
                            bt_inputs = [match['IN1'],match['IN2']]
                            if set(bt_inputs)<=set(inputs):
                                result.append([ckt_name, match])  
            #search 1 inputs
            if len(result)==0:
                for ckt_name, ckt in self.patterns.backtrack1_dict.items():
                    ckt_graph = self.patterns.ckt_graph[ckt_name] 
                    matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
                    if matches:
                        for match in matches:
                            if match['IN1'] == IN0:
                                result.append([ckt_name, match])   
            #search 1 inputs aug
            if len(result)==0:            
                for ckt_name, ckt in self.patterns.backtrack1_aug_dict.items():
                    ckt_graph = self.patterns.ckt_graph[ckt_name] 
                    matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
                    if matches:
                        for match in matches:
                            if match['IN1'] == IN0:
                                result.append([ckt_name, match])  
            
            if len(result)>0:
                ckt_name, match = result[0]
                pattern_ckt =  self.patterns.ckt_dict[ckt_name]
                pattern =  Pattern(pattern_ckt, master_ckt, match)
                return pattern
            else:
                raise ValueError
        
        else:
            #search inv
            matches = self.search_inv(devices_graph, IN1=IN0, OUT1=OUT)
            assert len(matches)<=1,'muti-backtrack inveters'
            if len(matches) == 1:
                pattern_ckt =  self.patterns.ckt_dict['INV']
                pattern =  Pattern(pattern_ckt, master_ckt, matches[0])
                return pattern
            else:
                raise ValueError
 

    
    def out_aux_netlist(self, file_path, init_ckt, ckt, sub_ckts):
        def write_line(f,d,key_net_mapping):
            if d.S in key_net_mapping:
                s1 =  key_net_mapping[d.S]
            else:
                s1 = ' '
            if d.G in key_net_mapping:
                s2 =  key_net_mapping[d.G]
            else:
                s2 = ' '
            if d.D in key_net_mapping:
                s3 =  key_net_mapping[d.D]
            else:
                s3 = ' '
            f.write('\t%5s %2s: %5s [%5s], %5s [%5s], %5s [%5s]\n'%(d.name,d.T,d.S,s1,d.G,s2,d.D,s3))
            
        key_net_mapping = init_ckt.key_net_mapping
        with open(file_path,'a+') as f:
            f.write('\n**********%s : %s**********\n'%(init_ckt.ckt_type,init_ckt.name))
            f.write('data:%s,m:%s,s:%s\n\n'%(str(self.data_net),self.m_net,self.s_net))
            for name,pat in sub_ckts.items():
                f.write('%-10s  %s\n'%(name,pat.ckt.name))    
                for d in pat.ckt.devices:
                    write_line(f,d,key_net_mapping)
            f.write('%-10s\n'%('devices left:'))
            for d in ckt.devices:
                write_line(f,d,key_net_mapping)



