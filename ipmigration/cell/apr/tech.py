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
        
        self._init_tech(cfgs.rule_file)

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
        self.SUBTXT ='SUBTXT'
        # self.BK1TXT = 'BK1TXT'
        # self.BK2TXT = 'BK2TXT'
        # self.BK3TXT = 'BK3TXT'
        
        self.layer_list = [self.NW, self.AA, self.GT, self.SP, self.SN, 
                           self.CT, self.M1, self.V1, self.M2, 
                           self.BORDER, self.M1TXT, self.SUBTXT ]
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
            self.SUBTXT:['false','#004080','#004080','0','0','I5','true','true' ,'false','false','false','0']  }

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
            
            
    def _init_tech(self, design_rule_file):
        #init design rules 
        df = pd.read_csv(design_rule_file)
        for i,r in df.iterrows():
            rule = r['rule'].strip()
            layers = [t.strip() for t in r['layer'].split('/')]
            if len(layers)==1:
                layer1 = layers[0]
                layer2 = layers[0]
            elif len(layers)>1:
                layer1 = layers[0]
                layer2 = layers[0]
            else:
                raise ValueError('%s is not a valid layer'%(r['layer']))
            assert layer1 in self.layer_list, 'layer %s is not in layer_list!'%(layer1)
            assert layer2 in self.layer_list, 'layer %s is not in layer_list!'%(layer2)
            
            value = int(float(r['value'])*1000)
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
        self.GT_CT_W = DR(name='GT_CT_W',layer1=self.GT,layer2=self.CT,
                          value=self.CT_W.v + 2*self.CT_E_GT.v,
                          note='Min Widht of GT with CT')
        self.M1_S_W =  DR(name='M1_S_W',layer1=self.M1,layer2=self.M1,
                          value=self.M1_W.v + self.M1_S.v,
                          note='M1 space + width')
        
        
        
        #vdd and vss rails        
        self.rail_vdd = Range(cfgs.cell_height , cfgs.power_rail_width) 
        self.rail_vss = Range(0, cfgs.power_rail_width) 
        
        #vdd and vss aa
        self.rail_vdd_aa = Range(self.rail_vdd.p2 - self.AA_S.h_v, 
                                 self.rail_vdd.p1 + self.AA_S.h_v, 
                                 set_t='pp')
        self.rail_vss_aa = Range(self.rail_vss.p2 - self.AA_S.h_v, 
                                 self.rail_vss.p1 + self.AA_S.h_v, 
                                 set_t='pp')
        
        #calculate tracks number 
        self.tracks_num = int(cfgs.cell_height / cfgs.v_pin_grid) + 1
        assert cfgs.cell_height % cfgs.v_pin_grid == 0, 'Height can not be divided by v grid'
        #for pin assesment 
        self.v_grids = [cfgs.v_pin_grid*t for t in range(self.tracks_num)]
        self.h_grids = [cfgs.h_pin_grid*t for t in range(100)] #temp
        

        print("Tech-> Track Number is %d!"%(self.tracks_num) )
                      
        #up and down poly tracks, also gt top/bottom 
        self.gt_up_range = Range(cfgs.cell_height - self.GT_W.h_v - self.GT_W.v, 
                                 cfgs.cell_height - self.GT_W.h_v, 
                                 set_t='pp')
        self.gt_down_range = Range(0 + self.GT_W.h_v, 
                                   0 + self.GT_W.h_v + self.GT_W.v, 
                                   set_t='pp')        
        
        #power rail diffusion contact
        #TODO consider AA space? Add AA space to dr
        self.ct_up_range = Range(cfgs.cell_height - self.CT_S.h_v - self.CT_W.v, 
                                 cfgs.cell_height - self.CT_S.h_v, 
                                 set_t = 'pp')
        self.ct_down_range = Range(0 + self.CT_S.h_v, 
                                   0 + self.CT_S.h_v + self.CT_W.v, 
                                   set_t = 'pp')        
       
        # m1 tracks on top and bottom
        top    = self.ct_up_range.p1 - self.CT_E_M1.v  
        bottom = self.ct_down_range.p2 + self.CT_E_M1.v  
        
        #Middle 2 tracks can also be connected by poly.  
        s1 = self.M1_W.v + self.M1_S.v
        s2 = self.GT_CT_W.v + self.GT_S.v
        if s2>=s1:
            mid_s = 0
        else:
            mid_s = s2-s1
            
        locs = place_rectangles(top-bottom-mid_s, self.M1_W.v, self.M1_S.v)
        assert len(locs)<5,'Cell Height is too low!'
        
        num = len(self.M1_tracks)
        if num % 2 == 0:
            median1 = num // 2
            median2 = median1 - 1
            median = median2
        else:
            median1 = num // 2
            median2 = median1 - 1
            median = median1
    
        
        self.M1_tracks = [Range(bottom+t,bottom+t+self.M1_W.v,set_t='pp') for t in locs]
        self.mid_track1 = self.M1_tracks[median]
        self.mid_track2 = [self.M1_tracks[median2],self.M1_tracks[median1]]

        #AA up and down
        # AA_p_up   = self.net_gt_up.p2   - tech.GT_X_AA.v
        # AA_n_down = self.net_gt_down.p1 + tech.GT_X_AA.v
        
        #TODO, may extract this to DB
        self.v_mode = {}     
        '''
        Principle:
        1. gt up and down are only used for cn/c
        2. m/bm/pm/s must be used
        3. Not may cross pattern nets, only cn/c and RN/SN pull
        4. 
        5. 
        
        0: GT connected and with 1 CT, INV, Logic, CLK...
        Detection conditions, all columns are GT pair.
        
        0: GT connected and with 2 CTs, and not GT up/down: INV, Logic, CLK...
        Detection conditions, all columns are GT pair.
            
            
        1: GT not connected and with 2 CTs, and not GT up/down: Cross, Backtrack...
        Detection conditions, not all columns are GT pair.
            
        2-n: TO be designed
        '''
        
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

class VMode:
    #based on mos pair
    def __init__(self):
        pass
        pmos_aa
        nmos_aa
        m1_nets
        
    def 
        








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
    def h_v(self):
        return int(0.5*self.value)


def place_rectangles(height, h, s):
    # 先计算理论上最多能放的长方形数量
    max_possible_n = 0
    while True:
        total_height_needed = max_possible_n * h + (max_possible_n + 1) * s
        if total_height_needed > height:
            break
        max_possible_n += 1
    # 确定实际能放置的长方形数量
    n = max_possible_n - 1
    if n < 0:
        print("给定的总高度无法放置任何长方形。")
        return []
    # 计算所有长方形占用的总高度
    total_rect_height = n * h
    # 计算至少需要的间距总长度，n 个长方形有 n + 1 个间距
    min_gap_space = (n + 1) * s
    # 计算剩余可用于分配额外间距的空间
    remaining_space = height - total_rect_height - min_gap_space
    # 尝试均匀分配剩余空间作为额外间距
    extra_gap = remaining_space // (n + 1)
    actual_gap = s + extra_gap
    positions = []
    current_height = actual_gap
    for i in range(n):
        positions.append(current_height)
        current_height += h + actual_gap
    return positions

    

    
