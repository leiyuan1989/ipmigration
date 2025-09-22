# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:45:48 2024

@author: leiyuan
"""

#tech 
import os
import logging
import pandas as pd
from ipmigration.cell.apr.lyt.shape import Range

# from src.writer.gds_writer import GdsWriter
# from src.writer.oasis_writer import OasisWriter

logger = logging.getLogger(__name__)

class Tech(object):
    def __init__(self, cfgs):
        self.tech_name = cfgs.tech_name
        self._init_layer_name()
        self._read_tech_align(cfgs.layer_align)
        self._read_layermap(cfgs.mapping_file)   
        
        self._gen_lyp(cfgs.output_dir)#maybe give user the option to gen it
        
        self._read_rule_align(cfgs.rule_file,cfgs.rule_align)

        self.gate_length = cfgs.gate_length

    def _init_layer_name(self):
        self.NW = 'NW' 
        self.AA = 'AA'
        self.GT = 'GT'
        self.SP = 'SP'
        self.SN = 'SN'
        self.CT = 'CT'
        self.M1 = 'M1'
        self.V1 = 'V1'
        self.M2 = 'M2'
        self.BORDER = 'BORDER'
        self.M1TXT = 'M1TXT'
        self.TEXT ='TEXT'
        # self.BK1TXT = 'BK1TXT'
        # self.BK2TXT = 'BK2TXT'
        # self.BK3TXT = 'BK3TXT'
        
        self.layer_list = [self.NW, self.AA, self.GT, self.SP, self.SN, 
                           self.CT, self.M1, self.V1, self.M2, 
                           self.BORDER, self.M1TXT, self.TEXT ]
        logger.info('tech->layers: '+ str(self.layer_list))
        
    def _read_tech_align(self, layer_align_file):
        assert os.path.exists(layer_align_file), "layer align file is not exist"
        
        df = pd.read_csv(layer_align_file,index_col=0)
        
        # layer_n = self.tech_name +'_ln'
        # layer_p = self.tech_name +'_lp'
        layer_n = 'name'
        layer_p = 'purpose'
        assert layer_n in df.columns
        assert layer_p in df.columns
        
        #clear blank in csv data
        ascell_layers = [t.strip() for t in df.index.tolist()] 
        tech_layers_n = [t.strip() for t in df[layer_n].tolist()] 
        tech_layers_p = [t.strip() for t in df[layer_p].tolist()] 
        
        layer_match = {t1:(t2,t3) for t1,t2,t3 in zip(ascell_layers,tech_layers_n,tech_layers_p)}
        
        self.layer_match = {}
        for layer in self.layer_list:
            assert layer in ascell_layers, 'layer %s not found in csv index!'%(layer)
            self.layer_match[layer] = layer_match[layer]

        
    def _read_layermap(self, layer_mapping_file):
        assert os.path.exists(layer_mapping_file), "layer mapping file not found! "
        
        with open(layer_mapping_file,'r') as f:
            lines = [t.strip() for t in f.readlines()]
        layer_to_stream = {}
        for line in lines:
            if len(line) > 0:
                if (line[0] == '#') or (line[0] == ';'):
                    pass
                else:
                    layerdata = line.split()

                    assert len(layerdata) == 4
                    layer_to_stream[(layerdata[0],layerdata[1])] = (int(layerdata[2]),int(layerdata[3]))
        self.output_map = {}
        for layer in self.layer_list:
            layer_p = self.layer_match[layer]
            assert layer_p in layer_to_stream, '%s is not found in layermaping file!'%(layer)        
            self.output_map[layer] = layer_to_stream[layer_p]

    def _gen_lyp(self,folder):
        #generate lyp file
        lyp_dict = {
            self.NW:    ['false','#800080','#800080','0','0','I5','true','false','false','false','false','0'],
            self.AA:    ['false','#ff0000','#ff0000','0','0','I2','true','true' ,'false','false','false','0'],
            self.GT:    ['false','#0000ff','#0000ff','0','0','I2','true','true' ,'false','false','false','0'],
            self.SP:    ['false','#ff0080','#ff0080','0','0','I9','true','false','false','false','false','0'],            
            self.SN:    ['false','#8086ff','#8086ff','0','0','I5','true','false','false','false','false','0'],
            self.CT:    ['false','#008080','#008080','0','0','I0','true','true' ,'false','false','false','0'],            
            self.M1:    ['false','#008080','#008080','0','0','I12','true','true','false','false','false','0'],
            self.V1:    ['false','#ffa080','#ffa080','0','0','I0','true','true' ,'false','false','false','0'],            
            self.M2:    ['false','#ffa080','#ffa080','0','0','I12','true','true','false','false','false','0'],
            self.BORDER:['false','#80ff8d','#80ff8d','0','0','I9','true','false','false','false','false','0'],            
            self.M1TXT: ['false','#ff0000','#ff0000','0','0','I5','true','true' ,'false','false','false','0'],
            self.TEXT:['false','#004080','#004080','0','0','I5','true','true' ,'false','false','false','0']  }
        self.lyp_dict = lyp_dict
        with open(os.path.join(folder,'kl_' + self.tech_name + '.lyp'),'w') as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<layer-properties>\n')
            for l,gds in self.output_map.items():
                f.write('<properties>\n')
                f.write('  <expanded>%s</expanded>\n'%(lyp_dict[l][0]))
                f.write('  <frame-color>%s</frame-color>\n'%(lyp_dict[l][1]))            
                f.write('  <fill-color>%s</fill-color>\n'%(lyp_dict[l][2]))
                f.write('  <frame-brightness>%s</frame-brightness>\n'%(lyp_dict[l][3]))
                f.write('  <fill-brightness>%s</fill-brightness>\n'%(lyp_dict[l][4]))
                f.write('  <dither-pattern>%s</dither-pattern>\n'%(lyp_dict[l][5]))
                f.write('  <line-style/>\n')
                f.write('  <valid>%s</valid>\n'%(lyp_dict[l][6]))
                f.write('  <visible>%s</visible>\n'%(lyp_dict[l][7]))
                f.write('  <transparent>%s</transparent>\n'%(lyp_dict[l][8]))
                f.write('  <width/>\n')
                f.write('  <marked>%s</marked>\n'%(lyp_dict[l][9]))
                f.write('  <xfill>%s</xfill>\n'%(lyp_dict[l][10]))
                f.write('  <animation>%s</animation>\n'%(lyp_dict[l][11]))
                f.write('  <name/>\n')
                f.write('  <source>%d/%d@1</source>\n'%(gds[0],gds[1]))
                f.write(' </properties>\n')                
            f.write(' <name/>\n')   
            f.write('</layer-properties>\n')      
            
            
    def _read_rule_align(self, design_rule_file, rule_align_file):
        #init design rules 
        df = pd.read_csv(rule_align_file)
        rules = {}
        dr_df =  pd.read_csv(design_rule_file)
        for i,r in dr_df.iterrows():
            rule = r['design rule'].strip()
            rules[rule] = [r['value'],r['rule description']]
        
        
        for i,r in df.iterrows():
            rule = r['rule'].strip()
            layers = [t.strip() for t in r['layer'].split('/')]
            if len(layers)==1:
                layer1 = layers[0]
                layer2 = layers[0]
            elif len(layers)>1:
                layer1 = layers[0]
                layer2 = layers[1]
            else:
                raise ValueError('%s is not a valid layer'%(r['layer']))
            assert layer1 in self.layer_list, 'layer %s is not in layer_list!'%(layer1)
            assert layer2 in self.layer_list, 'layer %s is not in layer_list!'%(layer2)
            
            number  = r['number'].strip()
            if number in rules:
                value =  int(float(rules[number][0])*1000)
                note =  rules[number][1]
            else:
                value = int(float(number)*1000)        
                note = r['description'].strip()
            dr = DR(name=rule,layer1=layer1,layer2=layer2,value=value,note=note)
            self.__setattr__(rule,dr)
            
        self.rule_list = dr.dr_list
        
        #rules of each layer
        for l in self.layer_list:
            self.__setattr__(l+'_dr_list',[])
        for dr in self.rule_list:
            self.__getattribute__(dr.layer1 + '_dr_list').append(dr)
            



        if self._check_rules():
            print("tech->Load tech files of tech:%s sucessfully"%(self.tech_name))
            logger.info("tech->rules: %s"%(str(self.rule_list)))
            logger.info("tech->Load tech files of tech:%s sucessfully"%(self.tech_name))

        else:
            raise ValueError("load tech file sucessfully, but there are some error values -9999!")
    

        # self.mos_space = 2*self.M1_S.v + self.M1_W.v
        

    def _check_rules(self):
        for rule in self.rule_list:
            if rule.v < 0:
                return False
        return True

    def preprocess(self,cfgs):
        #other design rules
        self.GT_CT_W = DR(name='GT_CT_W',layer1=self.GT,layer2=self.CT,
                          value=self.CT_W.v + 2*self.CT_E_GT.v,
                          note='Min Widht of GT with CT')
        self.M1_S_W =  DR(name='M1_S_W',layer1=self.M1,layer2=self.M1,
                          value=self.M1_W.v + self.M1_S.v,
                          note='M1 space + width')
        
        self.GT_CT_S_AA = DR(name='GT_CT_S_AA',layer1=self.GT,layer2=self.AA,
                             value= max(self.GT_S_LGT_AA.v, 
                                        self.CT_S_AA.v-self.CT_E_GT.v),
                             note='Min Space of GT with CT to AA')
        
        
        
        #vdd and vss rails        
        self.rail_vdd = Range(cfgs.cell_height , cfgs.power_rail_width) 
        self.rail_vss = Range(0, cfgs.power_rail_width) 
        
        #vdd and vss aa
        self.rail_vdd_aa = Range(cfgs.cell_height, self.AA_W.v)
        self.rail_vss_aa = Range(0, self.AA_W.v)
        
        #calculate tracks number 
        self.tracks_num = int(cfgs.cell_height / cfgs.v_pin_grid)
        assert cfgs.cell_height % cfgs.v_pin_grid == 0, 'Height can not be divided by v grid'
        #for pin assesment 
        self.v_grids = [cfgs.v_pin_grid*t for t in range(self.tracks_num)]
        self.h_grids = [cfgs.h_pin_grid*t for t in range(100)] #temp
        

        print("Tech-> Track Number is %d!"%(self.tracks_num) )
                      
        #up and down poly tracks, also gt top/bottom
        #gate top and bottom range: consider gt space and gt to vdd/vss aa
        t1 =  self.AA_W.hv + self.GT_S_AA.v
        t2 = self.GT_S.hv
        t = max(t1,t2)        
        self.gt_up = cfgs.cell_height - t
        self.gt_dn = t


        #power rail diffusion contact
        #consider AA space and CT space for abutment rule        
        t1 = self.rail_vdd_aa.p2 - self.CT_E_AA.v
        t2 = cfgs.cell_height - self.CT_S.hv
        t = min(t1,t2)
        self.ct_up_rg = Range(t - self.CT_W.v, t, set_t = 'pp')
        t1 = self.rail_vss_aa.p1 + self.CT_E_AA.v
        t2 = 0 + self.CT_S.hv
        t = max(t1,t2)
        self.ct_dn_rg = Range(t, t + self.CT_W.v, set_t = 'pp')        
       
        # m1 tracks on top and bottom
        top    = self.ct_up_rg.p1 - self.CT_E_M1_END.v  
        bottom = self.ct_dn_rg.p2 + self.CT_E_M1_END.v  
        
        locs = place_rectangles((bottom,top), self.M1_W.v,self.M1_W.v + self.CT_E_M1_END.v, self.M1_S.v)

        
        self.M1_tracks_num = len(locs)
        assert len(locs)>=5,'Cell Height is too low!'
        
        self.M1_tracks = [Range(t1,t2,set_t='pp') for t1,t2 in locs]
        self.CT_tracks = [Range(t.c, self.CT_W.v) for t in self.M1_tracks]
        
        print("Tech-> M1 Track Number is %d!"%(self.M1_tracks_num) )

        #
        num = len(self.M1_tracks)
        if num % 2 == 0:
            self.middle_up = num // 2
            self.middle_dn = self.middle_up - 1
            self.middle = int(0.5*(self.M1_tracks[self.middle_up].c + self.M1_tracks[self.middle_dn].c ))
        else:
            median = num // 2
            self.middle_up = median+1
            self.middle_dn = median-1
            self.middle = self.M1_tracks[median].c 
        
    

        
        self.gt_pmos_rg = Range(self.middle + self.GT_S.hv, 
                                   self.gt_up, 
                                   set_t='pp')

        self.gt_nmos_rg = Range(self.gt_dn, 
                                   self.middle - self.GT_S.hv, 
                                   set_t='pp')

        
        
        #below is for processing clk 
        
        self.clk_aap_rg = Range(self.gt_up - self.GT_X_AA.v, 
                                self.M1_tracks[self.middle_up+1].c + self.CT_W.hv + self.GT_CT_S_AA.v, 
                                   set_t='pp')
        
        self.clk_aan_rg = Range(self.M1_tracks[self.middle_dn].c - self.CT_W.hv - self.GT_CT_S_AA.v, 
                                self.gt_dn + self.GT_X_AA.v, 
                                   set_t='pp')        
        
        
        
        #TODO: a class called Editor
        
        #TODO: calculate horizon side widht here
        
        
        
        # self.M1_tracks[self.middle_up+1].c + self.CT_W.hv + self.GT_CT_S_AA
        
        # self.aap_up = self.gt_up_rg.p2 - self.GT_X_AA.v
        # self.aan_dn = self.gt_up_rg.p1 + self.GT_X_AA.v
        
        # self.aap_up = self.CT_tracks[-1].p1 - self.CT_S_AA.v  #gt_ct on top m1
        # self.aan_dn = self.CT_tracks[0].p2  + self.CT_S_AA.v  #gt_ct on bottom m1
        
        
        # #TODO:
        # self.aap_up_pc_c = self.gt_up_rg.p1 - self.GT_X_AA.v #polyconnect and connect to poly net
        # self.aap_up_pc_nc = self.gt_up_rg.p1 - self.GT_S.v - self.GT_X_AA.v #polyconnect and not connect to poly net

        # self.aan_dn_pc_c = self.gt_up_rg.p2 + self.GT_X_AA.v        
        # self.aan_dn_pc_nc = self.gt_up_rg.p2 + self.GT_S.v + self.GT_X_AA.v  
        
        
        
        # num = len(self.M1_tracks)
        # if num % 2 == 0:
        #     median1 = num // 2
        #     median2 = median1 - 1
        #     median = median2
        #     self.middle = int(0.5*(self.M1_tracks[median2].c + self.M1_tracks[median1].c))
        # else:
        #     median1 = num // 2
        #     median2 = median1 - 1
        #     median = median1
        #     self.middle = self.M1_tracks[median1].c 
        # self.median  = median
        # self.median1 = median1
        # self.median2 = median2       
        # self.mid_track1 = self.M1_tracks[median]
        # self.mid_track2 = [self.M1_tracks[median2],self.M1_tracks[median1]]



        







                                
        #AA up and down
        # AA_p_up   = self.net_gt_up.p2   - tech.GT_X_AA.v
        # AA_n_down = self.net_gt_down.p1 + tech.GT_X_AA.v
        
        #TODO, may extract this to DB
        # self.vmode = {i:VMode(self, i)  for i in range(VMode.total_vmodes)}     
        
        
            
        

        
        #V-Mode 0
        
        
        
        
        
        
        
        
        

        
        #1 2 gt-ct in middle, gt are connected. e.x. clk and output, dff cn c c cn 
        #2 1 gt-ct in middle,  e.x. inv  
        #output 6 tracks, track2 and 5 may not exist
        #output AA range 
        
        # #1e3
        # t1 = int(0.5*(tech.GT_S.v + tech.CT_W.v + 2*tech.CT_E_GT.v))
        # t2 = int(0.5*(tech.M1_S.v + tech.CT_W.v + 2*tech.CT_E_M1.v))
        # t = max(t1,t2)
        
        # gt_ct_up   = Range(self.middle + t,  tech.CT_W.v)  
        # gt_ct_down = Range(self.middle - t,  tech.CT_W.v)  
        
        # # gt_ct_up center to next ct center
        # t = max(tech.GT_S_LGT_AA.v + tech.CT_E_GT.v, tech.CT_S_AA.v) + tech.CT_E_AA.v + tech.CT_W.v
        
        # mos_ct_up  = Range( gt_ct_up.c   + t,  tech.CT_W.v)  
        # mos_ct_down = Range( gt_ct_down.c - t,  tech.CT_W.v) 
        
        # AA_p_down = mos_ct_up.p1   - tech.CT_E_AA.v
        # AA_n_up   = mos_ct_down.p2 + tech.CT_E_AA.v
        
        # #drc check
        # assert self.net_m1_up.p1 - mos_ct_up.p2 - tech.CT_E_M1.v >= tech.M1_S.v  
        # assert mos_ct_down.p1 - self.net_m1_down.p2 - tech.CT_E_M1.v >= tech.M1_S.v
        
        # self.v_mode[0] = {'tracks': [self.net_m1_down, mos_ct_down, gt_ct_down,gt_ct_up,mos_ct_up, self.net_m1_up]}
        
        # self.v_mode[0]['AA_pmos'] = Range(AA_p_up, AA_p_down,set_t='pp')
        # self.v_mode[0]['AA_nmos'] = Range(AA_n_up, AA_n_down,set_t='pp')
        # self.v_mode[0]['GT_pmos'] = Range(self.net_gt_up.p2, gt_ct_up.p1 - tech.CT_E_GT.v,set_t='pp')
        # self.v_mode[0]['GT_nmos'] = Range(gt_ct_down.p2 + tech.CT_E_GT.v, self.net_gt_down.p1,set_t='pp')        
        # #2       
        
        
        
        
        '''
        self.CT_W_half = int(0.5*self.CT_W.v)
        self.CT_GT_W_half = self.CT_W_half + self.CT_E_GT.v
        self.CT_M1_W_half = self.CT_W_half + self.CT_E_M1.v

        self.min_width = 2*self.CT_E_AA.v + self.CT_W.v
        self.aa_width1 =  self.CT_E_AA.v + self.CT_W.v + self.CT_S_GT.v
        
        self.gt_space1 = self.CT_S_GT.v + self.CT_W.v + self.CT_S_GT.v
        self.gt_space2 = self.GT_S.v
        self.gt_space3 = self.GT_S_LAA_GT.v + self.aa_width1  #abut
        self.gt_space4 = 2*self.GT_S_LAA_GT.v + self.min_width  #abut
                
        self.m1_width_end = self.M1_W.v + 2*self.CT_E_M1_END.v
        '''

# class VMode:
#     total_vmodes = 6
#     #based on mos pair
    
            
#     '''
#     Principle:
#     1. gt up and down are only used for cn/c
#     2. m/bm/pm/s must be used
#     3. Not may cross pattern nets, only cn/c and RN/SN pull
#     4. 
#     5. 
    
    
#     0:
#     1:
#     2:
#     3: GT connected and with 1 CT, INV, Logic, CLK...
#     Detection conditions, all columns are GT pair.
    
#     4: GT connected and with 2 CTs, and not GT up/down: INV, Logic, CLK...
#     Detection conditions, all columns are GT pair. GT connect is pin(2 CTs is a must)
        
        
#     5: GT not connected and with 2 CTs, and not GT up/down: Cross, Backtrack...
#     One M1 Track in 2-GT/CT to avoid dr violation
#     Detection conditions, not all columns are GT pair.
    
        
#     2-n: TO be designed
#     '''
    
    
#     def __init__(self, tech, vmode):
#         self.tech = tech
#         self.vmode = vmode
#         # self.init_vmode()
        
#         if self.vmode == 0:     
#             t = tech.median
#             self.gt_nodes = [(0,t-1,0),(0,t,0),(0,t+1,0)]
#             self.gt_nets = {}
#             self.connected = {}
#             self.edges = [] #edges that not nearby
#             self.ct_nodes = [(0,t,0.5)]

            
#         elif self.vmode == 1: #only pmos
#             self.pmos_aa_max = Range(tech.gt_up_rg.p2 - tech.GT_X_AA.v, 
#                                      tech.mid_track1.c + tech.GT_CT_W.hv + tech.GT_CT_S_AA.v, 
#                                      set_t='pp')
        
#             t1 = tech.median1
#             t2 = tech.median2  
#             self.gt_nodes = [(-1,t1,0),(0,t1,0),(1,t1,0),
#                              (-1,t2,0),(0,t2,0),(1,t2,0)]  
            
#             self.gt_nets = {(0,t1,0):'P'}
#             self.connected = {}
#             self.edges = [] #edges that not nearby
#             # self.ct_nodes = [(-1,t,0.5),(0,t,0.5),(1,t,0.5)]
#             self.ct_nodes = [(-1,t1,0.5),(0,t1,0.5),(1,t1,0.5),
#                              (-1,t2,0.5),(0,t2,0.5),(1,t2,0.5) ]
        
#         elif self.vmode == 2: #only nmos
#             self.nmos_aa_max = Range(tech.gt_dn_rg.p1 + tech.GT_X_AA.v, 
#                                      tech.mid_track1.c - tech.GT_CT_W.hv - tech.GT_CT_S_AA.v, 
#                                      set_t='pp')      
            
#             t1 = tech.median1
#             t2 = tech.median2  
#             self.gt_nodes = [(-1,t1,0),(0,t1,0),(1,t1,0),
#                              (-1,t2,0),(0,t2,0),(1,t2,0)]  
#             self.gt_nets = {(0,t2,0):'N'}
#             self.connected = {}
#             self.edges = [] #edges that not nearby
#             self.ct_nodes = [(-1,t1,0.5),(0,t1,0.5),(1,t1,0.5),
#                              (-1,t2,0.5),(0,t2,0.5),(1,t2,0.5) ]
            
#         elif vmode == 3:          
#             self.pmos_aa_max = Range(tech.gt_up_rg.p2 - tech.GT_X_AA.v, 
#                                      tech.mid_track1.c + tech.GT_CT_W.hv + tech.GT_CT_S_AA.v, 
#                                      set_t='pp')
            
#             self.nmos_aa_max = Range(tech.gt_dn_rg.p1 + tech.GT_X_AA.v, 
#                                      tech.mid_track1.c - tech.GT_CT_W.hv - tech.GT_CT_S_AA.v, 
#                                      set_t='pp')
        
#             t = tech.median
#             self.gt_nodes = [(-1,t,0),(0,t,0),(1,t,0)]
#             self.gt_nets = {(0,t,0):'P'}
#             self.connected = {}
#             self.edges = [] #edges that not nearby
#             self.ct_nodes = [(-1,t,0.5),(0,t,0.5),(1,t,0.5)]
            
#         elif vmode == 4:
#             self.pmos_aa_max = Range(tech.gt_up_rg.p2 - tech.GT_X_AA.v, 
#                                      tech.mid_track2[1].c + tech.GT_CT_W.hv + tech.GT_CT_S_AA.v, 
#                                      set_t='pp')
            
#             self.nmos_aa_max = Range(tech.gt_dn_rg.p1 + tech.GT_X_AA.v, 
#                                      tech.mid_track2[0].c - tech.GT_CT_W.hv - tech.GT_CT_S_AA.v, 
#                                      set_t='pp')
        
#             t1 = tech.median1
#             t2 = tech.median2       
#             self.gt_nodes = [(-1,t1,0),(0,t1,0),(1,t1,0),
#                              (-1,t2,0),(0,t2,0),(1,t2,0)]         
#             self.gt_nets = {(0,t1,0):'P'}
#             #key is the node with net labels
#             self.connected = {(0,t1,0): [
#                                            (( 0,t1,0),  (  0,t2,0)),
#                                           # (( 0,t1,1),  (  0,t2,1)),
#                                           (( 0,t1,0),  (  0,t1,0.5)),
#                                           (( 0,t1,0.5),(  0,t1,1)),
#                                           # (( 0,t2,0),  (  0,t2,0.5)),
#                                           # (( 0,t2,0.5),(  0,t2,1))
#                                           ]
#                               }
            
#             # self.connected = {}
            
#             self.ct_nodes = [(-1,t1,0.5),(0,t1,0.5),(1,t1,0.5),(0,t2,0.5)]
#             self.edges = []
            
#         elif vmode == 5:
#             assert (tech.GT_S.v + tech.GT_W.v) <= (tech.M1_S.v + tech.M1_W.v)
            
#             t1 = tech.M1_tracks[tech.median - 1]
#             t2 = tech.M1_tracks[tech.median + 1]        
                
#             self.pmos_aa_max = Range(tech.gt_up_rg.p2 - tech.GT_X_AA.v, 
#                                      t2.c + tech.GT_CT_W.hv + tech.GT_CT_S_AA.v, 
#                                      set_t='pp')
#             self.nmos_aa_max = Range(tech.gt_dn_rg.p1 + tech.GT_X_AA.v, 
#                                      t1.c - tech.GT_CT_W.hv - tech.GT_CT_S_AA.v, 
#                                      set_t='pp')
        
#             t = tech.median
#             t1 = t + 1
#             t2 = t - 1           
            
#             # self.gt_nodes = [(-1,t1,0),(0,t1,0),(1,t1,0),
#             #                  (-1,t,0), (0,t,0), (1,t,0),
#             #                  (-1,t2,0),(0,t2,0),(1,t2,0)]    
#             self.gt_nodes = [          (0,t1,0),
#                              (-1,t,0), (0,t,0), (1,t,0),
#                                        (0,t2,0),        ]             
#             self.gt_nets = {(0,t1,0):'P',(0,t2,0):'N'}
#             self.connected= {}
#             self.ct_nodes = [(0,t1,0.5),(0,t2,0.5),(-1,t,0.5),(1,t,0.5)]
#             self.edges = []
            
            

#         else:
#             raise ValueError('vmode is error!')
#     def __repr__(self):
#         return 'vmode: %d'%(self.vmode)
        
#     def gen_grids(self, offset):
#         gt_nodes = {'s':[],'g':[],'d':[]}
#         ct_nodes  = {'s':[],'g':[],'d':[]}
#         gt_nets = {}
#         connected = {}
#         edges = []
#         for t in self.gt_nodes:
#             if t[0] == -1:
#                 gt_nodes['s'].append((t[0] + offset,t[1],t[2]))
#             elif t[0] == 0:
#                 gt_nodes['g'].append((t[0] + offset,t[1],t[2]))
#             elif t[0] == 1:
#                 gt_nodes['d'].append((t[0] + offset,t[1],t[2]))
                
                
#         for t in self.ct_nodes:
#             if t[0] == -1:
#                 ct_nodes['s'].append((t[0] + offset,t[1],t[2]))
#             elif t[0] == 0:
#                 ct_nodes['g'].append((t[0] + offset,t[1],t[2]))
#             elif t[0] == 1:
#                 ct_nodes['d'].append((t[0] + offset,t[1],t[2]))   
        
#         for k,v in self.gt_nets.items():
#             gt_nets[(k[0]+offset,k[1],k[2])] = v
#         for k,v in self.connected.items():
#             new_v = []
#             for t in v:
#                 t1,t2 =t
#                 new_v.append(((t1[0]+offset,t1[1],t1[2]), (t2[0]+offset,t2[1],t2[2])))
#             connected[(k[0]+offset,k[1],k[2])] = new_v

#         for t in self.edges:
#             t1,t2 =t
#             edges.append(((t1[0]+offset,t1[1],t1[2]), (t2[0]+offset,t2[1],t2[2])))
#         return [gt_nodes,ct_nodes,gt_nets,connected,edges]

#     @staticmethod 
#     def get_vmode(pn_pairs,io_map):
#         pmos = pn_pairs['P']
#         nmos = pn_pairs['N']
#         if not(pmos) and not(nmos):
#             return 0
#         elif not(nmos) and pmos:
#             return 1
#         elif not(pmos) and nmos:
#             return 2
#         else:
#             if pmos.G == nmos.G:
#                 return 4
#                 # if pmos.G in io_map:
#                 #     return 4 
#                 # else:
#                 #     return 3
#             else:
#                 #TODO, will add more modes
#                 return 5

#     @staticmethod    
#     def gen_m1_grids(tech,max_col,offset=0):
#         nodes = {}
#         for i in range(tech.M1_tracks_num):
#             for j in range(max_col):
#                 nodes[(offset + j,i,1)] = {'net':'',
#                                            'loc':(offset + j,i),
#                                            'color':'orange'}
        
#         return nodes

        

class DR(object):
    dr_list =[]
    def __init__(self, name, layer1, value = -9999, layer2='', note='', pos_v ='', neg_v='', ico_v=''):
        self.name = name
        self.layer1 = layer1
        self.value = value
        self.layer2 = layer2
        self.note = note
        
        #TODO: left for auto-load drc deck
        # self.tokens = [t.strip() for t in note.split('\n')]
        # self.pos_v = [t.strip() for t in pos_v.split('\n')]
        # self.neg_v = [t.strip() for t in neg_v.split('\n')]      
        
        if ico_v:
            self.ico_v = [t.strip() for t in ico_v.split('\n')] 
        else:
            self.ico_v = []
        # self.run_length = run_length #TODO
        self.dr_list.append(self)
    def __repr__(self):
        return self.name + ' : ' + str(self.value) + ' nm' 
    def write_drc(self):
        return self.name + ' # ' + str(self.value) + ' # ' + self.note 
    
    @property
    def v(self):
        return self.value
    @property
    def hv(self):
        return int(0.5*self.value)





class Editor:
    def __init__(self,tech):
        pass






def place_rectangles(height_tuple, h1, h2, s):
    # Parse the height range tuple (low, high)
    low, high = height_tuple
    total_available_height = high - low  # Calculate total available height
    
    # Determine the maximum number of rectangles (n) that can be placed, with a minimum of 4
    n = 4  # Start with the minimum of 4 rectangles
    while True:
        # Calculate total height required for current n rectangles
        # Formula: (n-2) rectangles of h1 + 2 rectangles of h2 + (n-1) spaces of s
        total = (n - 2) * h1 + 2 * h2 + (n + 1) * s
        
        # If total exceeds available height, previous n is maximum possible
        if total > total_available_height:
            n -= 1
            break
        
        # Try increasing n to fit more rectangles
        n += 1
    
    # Calculate excess space to be placed at the top
    total_used_height = (n - 2) * h1 + 2 * h2 + (n + 1) * s
    excess = total_available_height - total_used_height
    
    # Calculate positions for each rectangle
    positions = []
    current_low = low + s  # Starting position of the topmost rectangle (accounting for excess space)
    
    for i in range(n):
        # Determine height for current rectangle:
        # h2 for second from top (i=1) and second from bottom (i=n-2)
        # h1 for all other positions
        
        #TODO: Below need consider other Tracks
        # current_height = h2 if i == 2 or i == n - 3 else h1
        current_height = h2 if i == n//2 or i == n//2 - 1 else h1
        
        current_high = current_low + current_height
        positions.append([current_low, current_high])
        
        # Set starting position for next rectangle (current top + space)
        current_low = current_high + s
    
    return positions






