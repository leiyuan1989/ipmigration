# -*- coding: utf-8 -*-
import os
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
        
        self.inv_nets = []
        self.input_nets = {}
        
        # self.input_point = self.net_map_r[self.ckt_type['input_pins'][0]]
        # self.power_match_list = ['CROSS_NOD_2','CROSS_NOD_3','CROSS_NOD_P1']
        # self.struct_array = {'match':[],'devices':[],'struct':[],'struct_t':[]}
    
    
    # def __repr__(self):
    #     return str(self.struct_array['struct_t']) + ' ' + str(self.struct_array['struct'])
    
    def run(self):
        logger.info('%s, %s, %d devices'%(self.tech_name,self.ckt, len(self.ckt.devices)))
        aux_file = os.path.join(self.output_dir,'aux_netlist.txt')

        #Sequential logic processing
        if self.ckt.ckt_type in ['ff', 'scanff', 'latch', 'clockgate']:
            print('-----%10s: %7s %5s %5s %5s'%(self.ckt.name, self.ckt.ckt_type, str(self.ckt.enable), str(self.ckt.mul_in),self.ckt.se_net))
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
                self.inv_nets.append(set([self.init_ckt.c_net,self.init_ckt.cn_net]))
                
                logger.info('1. clock pattern: %s: %s'%(str(self.sub_ckts['clk']),'clk'))
            
            #2. search inputs inv
            inpins = ['D', 'E' ,'D0','D1','S0','RN','SN','SE','SI']
            inputs_inv = self.search_inputs_inv(inpins, self.ckt, self.init_ckt)
            for pin, patterns in inputs_inv.items():
                self.input_nets[pin] = [self.init_ckt.pin_map_r[pin]]
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
            
            #3. search output
            out_patterns, self.to_out_net = self.search_output(self.ckt, self.init_ckt)
            for pin, pattern in out_patterns.items():
                ckt_name = 'out_%s'%(pin)
                self.sub_ckts[ckt_name] = pattern
                self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
                logger.info('3. output pattern: %s: %s'%(str(pattern),ckt_name))
                # self.init_ckt.__setattr__(net_name,output_net)
                # self.init_ckt.key_nets[net_name] = '%s_N%d'%(pin,i)
            
            #4.1  
            #process input for more than 1 input: mul-d, d with e, e with se,
            pattern = self.search_multi_inputs(self.ckt, self.init_ckt)
            if pattern:
                print(pattern)
                ckt_name = 'inputs'
                self.sub_ckts[ckt_name] = pattern
                self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
                logger.info('4. inputs(D0 D1 S0/D E/E SE) pattern: %s: %s'%(str(pattern),ckt_name))

            #4.2 search_synchronous
            if self.init_ckt.rn or self.init_ckt.sn:
                pattern = self.search_synchronous(self.ckt, self.init_ckt)

            #4.3 process SE and SI
            if self.init_ckt.ckt_type == 'scanff':
                pattern = self.search_scanff_inputs(self.ckt, self.init_ckt)
            


            #cross recognization

            #pull up/down
          
         
            #left cells?
            #aux
            self.out_aux_netlist(aux_file, self.init_ckt, self.ckt, self.sub_ckts)
            
            
        elif self.ckt.ckt_type in ['arithmetic','complex','multiplex']:
            pass
        else:
            raise ValueError('%s is not a right circuit type!'%(self.ckt.ckt_type))
        # ckt.c = 
        # ckt.cn = 
        # ckt.add_pin_map(pin_map)
        
        self.input = []
        self.net_pm = None
        self.net_bm = None
        self.net_m = None
        self.net_s = None
        
        # self.search_clk()
        # devices_graph = MosGraph(self.ckt)
        # self.search_inv(devices_graph)
        # self.search_logic(devices_graph)   
        # self.search_out(devices_graph)
        
        

        
        return 0   
    
    #match two graph with net match
    def match(self,devices_graph,struct_graph, net_match, nopower=True):
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
    def search_inv(self, devices_graph, in1=None, out1=None):
        inv_graph = self.patterns.ckt_graph['INV']  
        net_match = {}
        if in1:
            net_match['IN1']=in1
        if out1:
            net_match['OUT1']=out1              
        matches = self.match(devices_graph,inv_graph,net_match,nopower=False)
        return matches  
    
    #search logic
    def search_logic(self, devices_graph, input_map=None, ouput_map=None):
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
        result = []
        for ckt_name, ckt in self.patterns.logic_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
            # print(matches,net_match)
            if matches:
                result.append([ckt_name, matches])
            
        return result
    
    #search fcross
    def search_fcross(self, devices_graph, D=None, D1=None):
        #e.g. inputs {'IN1':xxx,'IN2':xxx, ...}
        net_match = {}
        if D:
            net_match['D']=D
        if D1:
            net_match['D1']=D1
        
        result = []
        for ckt_name, ckt in self.patterns.fcross_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
            if matches:
                result.append([ckt_name, matches])
        return result    

    #search pcross
    def search_pcross(self, devices_graph, IN0, IN1=None, D1=None):
        net_match = {'D':D}
        
        
        if D1:
            net_match['D1']=D1
        
        result = []
        for ckt_name, ckt in self.patterns.fcross_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = self.match(devices_graph,ckt_graph,net_match,nopower=False)
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
                matches = self.search_inv(devices_graph, in1=k)
                if len(matches)>0:
                    patterns = []
                    for match in matches:
                        patterns.append(Pattern(inv_ckt, master_ckt, match))
                        self.inv_nets.append(set([k,match['OUT1']]))
                    inputs_inv[v] = patterns
                                        
        return inputs_inv
    
        
    #search out patterns
    def search_output(self, ckt, master_ckt):
        devices_graph = MosGraph(ckt)
        inv_ckt  = self.patterns.ckt_dict['INV'] 
        out_patterns = {}
        for k,v in master_ckt.opins.items():
            if v == 'Q':
                matches = self.search_inv(devices_graph, out1=k)
                if len(matches)>0:
                    assert len(matches) == 1, 'multi-inv to Q'
                    match = matches[0]
                    out_patterns[v] = Pattern(inv_ckt, master_ckt,match)    
                    self.inv_nets.append(set([k,match['IN1']]))
            elif v == 'QN':
                matches = self.search_inv(devices_graph, out1=k)
                if len(matches)>0:
                    assert len(matches) == 1, 'multi-inv to QN'
                    match = matches[0]
                    out_patterns[v] = Pattern(inv_ckt, master_ckt, match)
                    self.inv_nets.append(set([k,match['IN1']]))
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
                ckt_name,match,out_match = result
                ckt =  self.patterns.ckt_dict[ckt_name]
                return Pattern(ckt, master_ckt, match)

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
        
        pass
    

    def search_asynchronous(self, ckt, master_ckt): 
        #RN and SN with PM and M 
        pass
    
 
    
    def search_scanff_inputs(self, ckt, master_ckt):   
        SI = master_ckt.si_net
        SE = master_ckt.se_net       
        assert SE != 'undef' and SI != 'undef'
        
        devices_graph = MosGraph(ckt)
        
        #synchronous RN SN process
        
        
        
        
        if master_ckt.enable or  master_ckt.mul_in:
            pass
        else:
            search_result = self.search_fcross(devices_graph, D1=SI)
            if len(search_result) == 1:
                print('***************************found*****************')
            else:
                print(search_result)
                print('^^^^^^^^^^^^^^^^^^^^^^^^^^^nofound*****************')
                # raise ValueError('Warning! input md is not searched')
        
         
    
    
 
  

    # def search_rnsn
    def search_out(self,devices_graph):
        self.sub_ckts['output'] = {}
        assert len(self.sub_ckts['logic_out']) <= 1
        if len(self.sub_ckts['logic_out']) == 1:
            self.sub_ckts['output'] = self.sub_ckts['logic_out']

        else:
            for out_pin, pattern in self.sub_ckts['inv_out'].items():
                double_inv_ckt   = self.patterns.clk_dict['CLK1']   
                double_inv_graph = self.patterns.ckt_graph['CLK1']
                matches = self.match(devices_graph,double_inv_graph,{'C': out_pin})
                if len(matches) == 1:
                    net1 = matches[0]['CN']
                    if len(self.ckt.nets_cdl[net1]) == 4:
                        self.sub_ckts['output'][out_pin] = Pattern(double_inv_ckt, self.init_ckt,matches[0])

                    else:
                        self.sub_ckts['output'][out_pin] = pattern
                else:
                    self.sub_ckts['output'][out_pin] = pattern
        
        #remove
        # print('before output remove', self.ckt)
        for out_pin, pattern in self.sub_ckts['output'].items(): 
            
            self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
            # print(self.ckt)
            print('02 Output found! Pattern: %s, %d devices left!'%(pattern.ckt.name, len(self.ckt.devices)))

    def search_cross(self, devices_graph, net_match):       
        searched = []
        for ckt_name, ckt in self.patterns.cross_dict.items():
            if  ckt_name in self.power_match_list:
                nopower = False
            else:
                nopower = True
                
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches=self.match(devices_graph,ckt_graph,net_match,nopower=nopower)
        
            for match in matches:
                pinA = match['A']
                pinB = match['B']
                
                if (pinA==self.clk_n and pinB==self.clk_p) or (pinB==self.clk_n and pinA==self.clk_p):
                    searched.append([ckt_name, match])

        return searched

    def classify_cross(self,searched,input_node):
        #split search cn/c cross patterns into front and back
        dist_graph = MosGraph(self.ckt)
        dist_graph.remove_nodes_from(['VDD','VSS',self.clk_n,self.clk_p])
        nodes_d = dict(nx.all_pairs_shortest_path_length(dist_graph))
        nodes_d_i = nodes_d[input_node] 
        dist_set_l = []
        for ckt_name,match in searched:
            dp1 = nodes_d_i[match['PMA:G']]
            dp2 = nodes_d_i[match['PMB:G']]
            dn1 = nodes_d_i[match['NMB:G']]
            dn2 = nodes_d_i[match['NMA:G']]
            dist_set = [dp1,dp2,dn1,dn2]
            dist_set.sort()
            if not(dist_set) in dist_set_l:
                dist_set_l.append(dist_set)

        # print(searched)
        # print(dist_set_l)
        
        if len(dist_set_l) != 2:
            print(searched)
            print(dist_set_l)     
        assert len(dist_set_l) == 2  
   
        if sum(dist_set_l[0]) > sum(dist_set_l[1]) :
            cross1_dist_set = dist_set_l[1]
            cross2_dist_set = dist_set_l[0]
        else:
            cross1_dist_set = dist_set_l[0]
            cross2_dist_set = dist_set_l[1]           
        
        cross1 = []
        cross2 = []
        for ckt_name,match in searched:
            dp1 = nodes_d_i[match['PMA:G']]
            dp2 = nodes_d_i[match['PMB:G']]
            dn1 = nodes_d_i[match['NMB:G']]
            dn2 = nodes_d_i[match['NMA:G']]
            dist_set = [dp1,dp2,dn1,dn2]
            dist_set.sort()
            if dist_set == cross1_dist_set:
                cross1.append([ckt_name,match])
            if dist_set == cross2_dist_set:
                cross2.append([ckt_name,match])
        return cross1,cross2

    def fix_cross(self, searched, input_node, name='cross1'):
        dist_graph = MosGraph(self.ckt)
        dist_graph.remove_nodes_from(['VDD','VSS',self.clk_n,self.clk_p])
        nodes_d = dict(nx.all_pairs_shortest_path_length(dist_graph))
        nodes_d_i = nodes_d[input_node] 
        

        if len(searched) == 1:     
            ckt_name,match = searched[0]
            pattern = Pattern(self.patterns.ckt_dict[ckt_name], self.init_ckt, match)
            self.sub_ckts[name] = pattern
            return pattern.net_map['PM']
        else: #symmetry
            for ckt_name,match in searched:
                dp1 = nodes_d_i[match['PMA:G']]
                dp2 = nodes_d_i[match['PMB:G']]
                dn1 = nodes_d_i[match['NMB:G']]
                dn2 = nodes_d_i[match['NMA:G']]
                # print(ckt_name,dp1,dp2,dn1,dn2)
                if (dp1 + dn1) < (dp2 + dn2) :      
                    pattern = Pattern(self.patterns.ckt_dict[ckt_name], self.init_ckt, match)
                    self.sub_ckts[name] = pattern
                    return  pattern.net_map['PM']
        raise ValueError #error in found searched
        # return False
    
    # def find_pm(self, cross_pattern):
                
    def search_backtrack(self, devices_graph, input_net, name='backtrack1'):
        
        #search inv
        inv_ckt   = self.patterns.ckt_dict['INV']   
        inv_graph = self.patterns.ckt_graph['INV'] 
        
        matches = self.match(devices_graph,inv_graph,{'IN1': input_net}, nopower=False)
        # print(matches)
        assert len(matches)<=1
        if len(matches) == 1:
            pattern = Pattern(inv_ckt, self.init_ckt, matches[0])
            self.sub_ckts[name] = pattern            
            return True

        #search logic
        for ckt_name, ckt in self.patterns.logic_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = devices_graph.find_subgraph_matches(ckt_graph,
                                                          node_match=MosGraph.node_match_power,
                                                          edge_match=MosGraph.edge_match_power)
            for match in matches:
                pin_in1 = match['IN1'] 
                pin_in2 = match['IN2']
                if  (pin_in1 in self.net_map) and (pin_in2 == input_net) or \
                    (pin_in2 in self.net_map) and (pin_in1 == input_net) :
                    pattern = Pattern(ckt, self.init_ckt, match)  
                    self.sub_ckts[name] = pattern            
                    return True
        
        #backtrack paddings
        for ckt_name, ckt in self.patterns.backtrack_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = devices_graph.find_subgraph_matches(ckt_graph,
                                                          node_match=MosGraph.node_match_power,
                                                          edge_match=MosGraph.edge_match_power)
            for match in matches:
                pins = []
                for t in ['IN1','IN2','IN3','IN4','IN5']:
                    if t in match:
                        pins.append(match[t])
         
                if_match = True
                for p in pins:
                    if p in self.net_map or p ==input_net:
                        pass
                    else:
                        if_match = False
                        break
                if if_match: 
                    pattern = Pattern(ckt, self.init_ckt, match)  
                    self.sub_ckts[name] = pattern            
                    return True  

        print(self.clk_n,self.clk_p,self.net_pm,self.net_bm)
        raise ValueError
      
    
    def search_rnsn(self):
        self.rnsn_signal = []
        self.rnsn_switch = []
        
        for p in ['RN','SN']:
            if p in self.net_map_r:
                self.rnsn_signal.append(self.net_map_r[p])
                if p in self.sub_ckts['inv_in']:
                    self.rnsn_signal.append(self.net_map_r['N_' + p] )
            
        # for d in self.ckt.devices:
        #     if d.G in self.rnsn_signal:
                
        #
    
    
    def search_pull(self,devices_graph, input_net, name='pull1'):
        #PM BM 
        #search logic
        for ckt_name, ckt in self.patterns.pull_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = devices_graph.find_subgraph_matches(ckt_graph)
            matches = self.match(devices_graph,ckt_graph,{'PM':input_net })    
            for match in matches:
                pins = []
                for t in ['IN1','IN2','IN3','IN4','IN5']:
                    if t in match:
                        pins.append(match[t])
                
                if_match = True
                for p in pins:
                    if p in self.rnsn_signal:
                        pass
                    else:
                        if_match = False
                        break
                if if_match: 
                    pattern = Pattern(ckt, self.init_ckt, match)  
                    self.sub_ckts[name] = pattern            
                    return True  
            return False
    
        
    def pruning(self):
        assert  'cross1' in self.sub_ckts
        assert  'backtrack1' in self.sub_ckts
        # print('1',self.ckt)
        self.ckt = self.ckt.sub_ckt( self.sub_ckts['cross1'].ckt.devices, remove=True)  
        self.ckt = self.ckt.sub_ckt( self.sub_ckts['backtrack1'].ckt.devices, remove=True)  
        # print('2',self.ckt)
        if 'cross2' in self.sub_ckts:
            self.ckt = self.ckt.sub_ckt( self.sub_ckts['cross2'].ckt.devices, remove=True)  
            print('cross2', self.sub_ckts['cross2'])
        if 'backtrack2' in self.sub_ckts:
            self.ckt = self.ckt.sub_ckt( self.sub_ckts['backtrack2'].ckt.devices, remove=True)  
            # print('3',self.ckt)          
        
        self.sub_ckts['inv'] = {}
        for name, pattern in self.sub_ckts['inv_in'].items():
            prune = False
            for device in pattern.ckt.devices:
                if self.ckt.find_device(device.name):
                    pass
                else:
                    prune=True
            if not(prune):
                self.sub_ckts['inv'][name] = pattern
                self.ckt = self.ckt.sub_ckt( pattern.ckt.devices, remove=True)  
        
        devices_graph = MosGraph(self.ckt)
        self.search_rnsn()
        t1 = self.search_pull(devices_graph,self.net_pm, name='pull1')
        if t1:
            print('YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
            self.ckt = self.ckt.sub_ckt( self.sub_ckts['pull1'].ckt.devices, remove=True)  
        
        
        # print(self.clk_n,self.clk_p,self.net_pm,self.net_bm,self.net_map)
        # print(self.ckt.devices)
    
    # def 

        
    
    
    
    # def expand_cross(self, cross_pattern, input_pn): #important
    #     #IN1 IN2 OUT1 OUT2
        
        
        
        
    #     p_devices = [t for t in self.ckt.devices if t.T == 'P']
    #     n_devices = [t for t in self.ckt.devices if t.T == 'N']

    #     g1 = ChainGraph(p_devices)
    #     g2 = ChainGraph(n_devices)
    
    #     pma = cross_pattern.device_map['PMA']
    #     pmb = cross_pattern.device_map['PMB']
    #     nmb = cross_pattern.device_map['NMB']
    #     nma = cross_pattern.device_map['NMA']        
    #     # t1
    #     path_p = nx.all_simple_paths(g1,pma+':G',pmb+':G')
    #     path_n = nx.all_simple_paths(g2,nmb+':G',nma+':G') 
    #     t1 = list(path_p)
    #     t2 = list(path_n)
    #     if len(t1) != 2 or  len(t2) != 2:
    #         print('aaaaaaa',t1,len(t1))
    #         print('bbbbbbb',t2,len(t2))
    
    
    
    
    
    def search_input(self):
        devices_graph = MosGraph(self.ckt)
        
        self.sub_ckts['input'] = {}
        itype = self.ckt_type['input_type']
        
        if itype == (1,1) or itype == (2,1):
            searched = self.search_cross(devices_graph,{})
            assert len(searched) > 0 #cross not found
            input_node = self.ckt_type['input_pins'][0] 
            self.net_pm = self.fix_cross(searched, input_node)
            self.search_backtrack(devices_graph, self.net_pm )
            
            
            self.pruning()

                
                
                
 
                
        elif itype == (1,2):
            pass        
        
        elif itype == (1,3):
            pass   
        elif itype == (1,4):
            pass   
        elif itype == (2,1):
            pass   
        elif itype == (2,2):
            pass   
        elif itype == (3,1):
            searched = self.search_cross(devices_graph,{})  
            assert len(searched) > 1
            
            input_node = self.ckt_type['input_pins'][0] 
            cross1,cross2 = self.classify_cross(searched,input_node)
            self.net_pm = self.fix_cross(cross1,input_node)
            self.net_bm = self.fix_cross(cross2,self.net_pm,name='cross2')
            
            self.search_backtrack(devices_graph, self.net_pm )
            self.search_backtrack(devices_graph, self.net_bm,name='backtrack2' )
            
            self.pruning()
    
        elif itype == (3,2):
            pass   
        elif itype == (3,3):
            pass   
        elif itype == (3,4):
            pass   
        elif itype == (4,1):
            pass   
        elif itype == (4,2):
            pass   
        elif itype == (4,3):
            pass   
        elif itype == (4,4):
            pass   
        else:
            raise ValueError
        # no_scan = (self.ckt_type['scan'] == [])
        # if no_scan:
        #     #D 
        #     if self.ckt_type['input_pins'] == ['D'] or self.ckt_type['input_pins'] == ['E']:
        #         return 1        #no need to search input
            
        #     #Enable D
        #     if self.ckt_type['input_pins'] == ['D', 'E']:
        #         for ckt_name, ckt in self.patterns.input_ed_dict.items():
        #             ckt_graph = self.patterns.ckt_graph[ckt_name] 
        #             devices_graph = MosGraph(self.ckt)
        #             if 'N_D' in self.net_map_r:
        #                 net_match={'N_D': self.net_map_r['N_D'],'E':self.net_map_r['E'],'N_E':self.net_map_r['N_E'] }
        #             else:   
        #                 net_match={'D': self.net_map_r['D'],'E':self.net_map_r['E'],'N_E':self.net_map_r['N_E'] }
        #             # net_match={ 'E':self.net_map_r['E']}
        #             matches=self.match(devices_graph,ckt_graph,net_match,nopower=True)
    
            
        #             if len(matches) == 1:
        #                 pattern = Pattern(ckt, self.init_ckt, matches[0])  
        #                 self.sub_ckts['input']['pattern'] = pattern  
        #                 self.sub_ckts['input']['type'] = 'ED'              
                        
        #                 return 1
        #         print("!!!!!!!!!!!! No Enable D found!!!!!!!!!")
           
        #     #D0 D1
        #     if self.ckt_type['input_pins'] == ['D0', 'D1'] or self.ckt_type['input_pins'] == ['D0', 'D1', 'S0']:      
        #         print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        #         # print(self.sub_ckts)
                
        #         if ('D0','D1') in self.sub_ckts['logic_input']:
        #             pass
        #         else:
        #             pass
        #         print(self.sub_ckts['logic_input'] )
                
        #         for ckt_name, ckt in self.patterns.input_md_dict.items():
        #             ckt_graph = self.patterns.ckt_graph[ckt_name] 
        #             devices_graph = MosGraph(self.ckt)
                    
        #             # net_match={'D': self.net_map_r['D'],'E':self.net_map_r['E'],'N_E':self.net_map_r['N_E'] }
        #             # net_match={'N_D': self.net_map_r['N_D'],'E':self.net_map_r['E'],'N_E':self.net_map_r['N_E'] }
                    
        #             # matches=self.match(devices_graph,ckt_graph,net_match,nopower=True)
                
        # else:
        #     pass
        
        
        
        return 0
 
    #for netlist mapping support
    
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
            for name,pat in sub_ckts.items():
                f.write('%-10s  %s\n'%(name,pat.ckt.name))
                for d in pat.ckt.devices:
                    write_line(f,d,key_net_mapping)
            f.write('%-10s\n'%('devices left:'))
            for d in ckt.devices:
                write_line(f,d,key_net_mapping)



