# -*- coding: utf-8 -*-
import os
import networkx as nx
from ipmigration.cell.apr.cir.graph import MosGraph
from ipmigration.cell.apr.cir.patterns import Pattern

DEBUG=False

class DeCKT:
    def __init__(self, ckt, patterns, tech_name, output_dir):
        self.init_ckt = ckt
        self.ckt = ckt.copy()
        self.patterns = patterns
        self.sub_ckts = {}
        self.tech_name = tech_name
        self.output_dir = output_dir
        # self.input_point = self.net_map_r[self.ckt_type['input_pins'][0]]
        # self.power_match_list = ['CROSS_NOD_2','CROSS_NOD_3','CROSS_NOD_P1']
        # self.struct_array = {'match':[],'devices':[],'struct':[],'struct_t':[]}
    
    
    # def __repr__(self):
    #     return str(self.struct_array['struct_t']) + ' ' + str(self.struct_array['struct'])
    
    def run(self):
        print('%s, %s, %d devices'%(self.tech_name,self.ckt, len(self.ckt.devices)))
        aux_file = os.path.join(self.output_dir,'aux_netlist.txt')

        #Sequential logic processing
        if self.ckt.ckt_type in ['ff', 'scanff', 'latch', 'clockgate']:
            #search clock patterns 
            self.sub_ckts['clk'] = self.search_clk(self.ckt, self.init_ckt )
            if not(self.sub_ckts['clk']):
                raise ValueError('CLK patterns are not found in netlist!')
            else:
                #remove device                 
                self.ckt = self.ckt.sub_ckt(self.sub_ckts['clk'].ckt.devices, remove=True)  
                #set key net c and cn:
                self.init_ckt.c_net = self.sub_ckts['clk'].net_map[self.init_ckt.key_nets['c_net']]
                self.init_ckt.cn_net = self.sub_ckts['clk'].net_map[self.init_ckt.key_nets['cn_net']]
            
            #search inv of D, E ,MD , RN SN SE SI....
            for pin in ['D', 'E' ,'D0','D1','S0','RN','SN','SE','SI']:
                if pin in self.init_ckt.ipins_r:
                    input_net= self.init_ckt.ipins_r[pin]
                    pattern = self.search_input_inv(input_net, self.ckt, self.init_ckt)
                    if pattern:
                        print('input_inv_%s'%(pin))
                        self.sub_ckts['input_inv_%s'%(pin)] = pattern
                        self.ckt = self.ckt.sub_ckt(pattern.ckt.devices, remove=True)  
                        #revise initial ckt and ckt key_nets
                        inv_input_name = 'inv_%s_net'%(pin)
                        inv_input_net = pattern.net_map['OUT1']
                        self.init_ckt.__setattr__(inv_input_name,inv_input_net)
                        self.init_ckt.key_nets[inv_input_name] = '%s_N'%(pin)
            #search output             
         
            #process input for more than 1 input: mul-d d with e, e with se, se and si...

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
        
        
        # t1 = self.search_input()
        
        
        
        
        # print('2',self.tech_name,self.ckt)
        #search RN SN 
        # NRN NSN RNG NRNG SNG NSNG SNP NSNP.....
        # print('3',self.tech_name,self.ckt)
    
        # t1 = self.search_cross1()        
        #search Input
        # t1 = self.search_input()
                
    
        # print(self.tech_name,self.ckt)
        # t1 = self.search_cross()
        
        # remove cross 
        # mark 
        
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
    def search_input_inv(self, input_net, ckt, master_ckt):
        inv_ckt   = self.patterns.ckt_dict['INV']   
        inv_graph = self.patterns.ckt_graph['INV']  
        devices_graph = MosGraph(self.ckt)

    
        matches = self.match(devices_graph,inv_graph,{'IN1':input_net}, nopower=False)
        if len(matches) == 1:
            search = matches[0]
            pattern = Pattern(inv_ckt, master_ckt, search)
            return pattern
        else:
            return None


    #search out inv pattern? 1 and 2 inv. is 3 needed?
    '''
    for all 
    if a inverter is found, 
    
    for single
    if input for the inv is the out of another inv and no other net?  
    
    for both
    '''
    
    def search_output_inv(self, opins, ckt, master_ckt):
        inv_ckt   = self.patterns.ckt_dict['INV']   
        inv_graph = self.patterns.ckt_graph['INV']  
        devices_graph = MosGraph(self.ckt)
        out_patterns = {}
        for opin in opins:
            out_patterns[opin] = {'patterns':[],'input':'none' }
            
            matches = self.match(devices_graph,inv_graph,{'OUT1':opin}, nopower=False)
            if len(matches) == 1:
                search = matches[0]
                pattern = Pattern(inv_ckt, master_ckt, search)
            
                
           # s = [1,2,3]

# In [2]: ls.insert(0, "new")     
                
                
        #find inv
        
        #inv input net has 4 device, search next inv
        
        #how to find 
        if len(matches) == 1:
            search = matches[0]
            pattern = Pattern(inv_ckt, master_ckt, search)
            return pattern
        else:
            return None






    def ckt_net_map(self, netlist_pin_map):
        net_map = {}
        for p in self.ckt.pins:
            net_map[p] = netlist_pin_map[p]
        net_map_r = {v: k for k, v in  net_map.items()} 
        self.net_map = net_map   # ckt to pattern
        self.net_map_r = net_map_r #pattern to ckt 
    
    # def classify_ckt(self):
    #     mapped_pins = []
    #     for p in self.ckt.pins:
    #         # if p == 'EN' or p == 'E':
    #         #     print('aaaa',p)
    #         if not(p in self.netlist_pin_map):
    #             raise ValueError('Pin not found in netlist pin map',self.tech_name,self.ckt.name,p,self.netlist_pin_map)
    #         else:
    #             p1 = self.netlist_pin_map[p]
    #             if p1 != 'VDD' and p1 != 'VSS':
    #                 mapped_pins.append(p1)        
    #     # self.mapped_pins = mapped_pins
    #     self.ckt_type = classify_ckt(mapped_pins)
    
    # @staticmethod
    # def _add_net(net_map, net_map_r, nets):
    #     for a,b in nets.items():
    #         net_map[a] = b
    #         net_map_r[b] = a


    
     
        
    # def add_struct(self, struct_t, match_dict):
    #     for k,v in match_dict.items():
    #         self.struct_array[k].append(v)
    #     self.struct_array['struct_t'].append(struct_t)    





    def search_inv(self,devices_graph):
        self.sub_ckts['inv_in'] = {}
        self.sub_ckts['inv_out'] = {}
        inv_ckt   = self.patterns.ckt_dict['INV']   
        inv_graph = self.patterns.ckt_graph['INV']  
        
        matches = devices_graph.find_subgraph_matches(inv_graph,
                                                      node_match=MosGraph.node_match_power,
                                                      edge_match=MosGraph.edge_match_power)
        searched_in = []
        searched_out = []
        for match in matches:
            pin_in = match['IN1'] 
            pin_out = match['OUT1'] 
            if pin_in in self.net_map:  #may include rn sn
                searched_in.append([pin_in, match] )
            if pin_out in self.ckt_type['output_pins']:
                searched_out.append([pin_out, match] ) 
        if len(searched_in) > 0: 
            for pin_in,match in searched_in:
                self.net_map[match['OUT1']] = 'N_' + self.net_map[pin_in]
                self.net_map_r['N_' + self.net_map[pin_in]] = match['OUT1']
                pattern = Pattern(inv_ckt, self.init_ckt, match)    
                self.sub_ckts['inv_in'][pin_in] = pattern                         
        if len(searched_out) > 0: 
            for pin_out,match in searched_out:
                pattern = Pattern(inv_ckt, self.init_ckt, match)    
                self.sub_ckts['inv_out'][pin_out] = pattern  
        
        
    def search_logic(self,devices_graph):
        self.sub_ckts['logic_in'] = {}
        self.sub_ckts['logic_out'] = {}
        #logic
        for ckt_name, ckt in self.patterns.logic_dict.items():
            ckt_graph = self.patterns.ckt_graph[ckt_name] 
            matches = devices_graph.find_subgraph_matches(ckt_graph,
                                                          node_match=MosGraph.node_match_power,
                                                          edge_match=MosGraph.edge_match_power)
            for match in matches:
                pin_in1 = match['IN1'] 
                pin_in2 = match['IN2']
                pin_out = match['OUT1']
                if  (pin_in1 in self.net_map) and (pin_in2 in self.net_map):
                    print('logic input found: ',pin_in1,pin_in2,ckt_name)
                    pattern = Pattern(ckt, self.init_ckt, match)  
                    self.sub_ckts['logic_in'][(pin_in1,pin_in2)] = pattern                         
                    break
                if pin_out in self.ckt_type['output_pins']:
                    if self.ckt_type['type'] == 'CG':
                        print('logic output found: ',pin_out,ckt_name)
                        pattern = Pattern(ckt, self.init_ckt, match)  
                        self.sub_ckts['logic_out'][pin_out] = pattern                         
                        break      

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
            f.write('\t%5s : %5s [%5s], %5s [%5s], %5s [%5s]\n'%(d.name,d.S,s1,d.G,s2,d.D,s3))
            
        key_net_mapping = init_ckt.key_net_mapping
        with open(file_path,'a+') as f:
            f.write('\n**********%s : %s**********\n'%(init_ckt.ckt_type,init_ckt.name))
            for name,pat in sub_ckts.items():
                f.write('%-10s\n'%(name))
                for d in pat.ckt.devices:
                    write_line(f,d,key_net_mapping)
            f.write('%-10s\n'%('devices left:'))
            for d in ckt.devices:
                write_line(f,d,key_net_mapping)



