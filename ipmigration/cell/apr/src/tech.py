# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 14:45:48 2024

@author: leiyuan
"""

#tech 
import os
import logging
import pandas as pd


from src.basic.rule import DR


# from src.writer.gds_writer import GdsWriter
# from src.writer.oasis_writer import OasisWriter

logger = logging.getLogger(__name__)

class Tech(object):
    def __init__(self, args, from_calibre = False):
       
        '''
        args.tech_align_file = os.path.join(args.data_dir,'tech_align.csv')
        args.cfg_folder = os.path.join(args.data_dir,args.tech_name,'ascell')
        
        args.cell_list_file = os.path.join(args.cfg_folder,'00_cell_list.txt')
        args.cell_para_file = os.path.join(args.cfg_folder,'01_cell_para.txt')
        args.design_rule_file = os.path.join(args.cfg_folder,'02_design_rule.txt')   
        args.model_file = os.path.join(args.cfg_folder,'model.cdl') 
        args.netlist_file = os.path.join(args.cfg_folder,'netlist.cdl') 
        
        '''

        self.tech_name = args.tech_name
        self.tech_dir = args.tech_dir
        
        self._init_layer_name()
        self.read_tech_align(args.tech_align_file)        
        self.read_layermap(args.layer_mapping_file)   
        self.gen_lyp(args.output_dir)
        
        
        if from_calibre:
            # self.extract_calibre_drc()
            pass
        else:
            self._init_tech(args.design_rule_file)

    
        
        
        
        # print(lines)
        
        
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
        


        
    def read_tech_align(self, tech_align_file):
        assert os.path.exists(tech_align_file), "layer align file is not exist"
        
        df = pd.read_csv(tech_align_file,index_col=0)
        
        layer_n = self.tech_name +'_ln'
        layer_p = self.tech_name +'_lp'
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


        
    def read_layermap(self, layer_mapping_file):
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

    def gen_lyp(self,folder):
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
        df = pd.read_excel(design_rule_file)
        for i,r in df.iterrows():
            rule = r['rule'].strip()
            layer1 = r['layer1'].strip()
            layer2 = r['layer2'].strip()
            value = int(float(r['value'])*1000)
            note = r['description'].strip()
            assert layer1 in self.layer_list, 'layer %s is not in layer_list!'%(layer1)
            assert layer2 in self.layer_list, 'layer %s is not in layer_list!'%(layer2)
            dr = DR(name=rule,layer1=layer1,layer2=layer2,value=value,note=note)
            self.__setattr__(rule,dr)
        self.rule_list = dr.dr_list
        
        for l in self.layer_list:
            self.__setattr__(l+'_dr_list',[])
        for dr in self.rule_list:
            self.__getattribute__(dr.layer1 + '_dr_list').append(dr)
            



        if self.check_rules():
            print("tech-> Load tech files of tech [%s] sucessfully"%(self.tech_name))
            logger.info("tech-> Load tech files of tech [%s] sucessfully"%(self.tech_name))
        else:
            raise ValueError("load tech file sucessfully, but there are some error values -9999!")
    
        #for easy program
        
        
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
        
        # self.GT_wire_width = self.CT_W.v + 2*self.CT_E_GT.v
        # # self.AA_side = self.CT_E_AA.v + self.CT_W.v + self.CT_S_GT.v
        # self.AA_side = self.CT_E_AA.v + self.CT_W.v + self.CT_E_AA.v + self.GT_S_AA.v
        # self.AA_middle1 = self.CT_S_GT.v + self.CT_W.v + self.CT_S_GT.v
        # self.AA_middle2 = 2*self.GT_S_AA.v + self.CT_W.v + 2*self.CT_E_AA.v
        # self.AA_middle3 = self.GT_S_AA.v + self.CT_E_AA.v + self.CT_W.v + self.GT_S.v +  self.CT_E_GT.v
        # self.mos_space = 2*self.M1_S.v + self.M1_W.v
        
        # self.GT_CT_W_half = int(0.5*(self.CT_W.v) + self.CT_E_GT.v)
            
            
 

        


    def extract_calibre_drc(self,extracted_rule_file=''):
        if extracted_rule_file == '':
            extracted_rule_file =  os.path.join(self.tech_dir,'calibre','extract_calibre_rule.txt')
        #read calibre drc file and extract useful drc information
        calibre_folder = os.path.join(self.tech_dir,'calibre')
        calibre_drcfile = [t for t in os.listdir(calibre_folder) if t.endswith('.drc') or t.endswith('.rul')]
        assert len(calibre_drcfile) == 1, "no calibre drc file file end up with '.drc' or '.rul' or multiple calibre drc file files" 
        
        layer_name_out = [self.layer_match[t][0] for t in self.layer_list]
        layer_name_dict = {}
        for layer_name in layer_name_out:
            layer_name_dict[layer_name] = []
        
        out_file = open(extracted_rule_file,'w')
        
        with open(os.path.join(calibre_folder,calibre_drcfile[0]),'rb') as f:
            #if not add encoding, will cause 'cp90' error
            #
            passline = False
            cache = False
            # cache = ''
            rule = ''
            variable = {}
            marcodef = []
            for line in f:
                try:
                    line = line.decode().strip()
                except:
                    line = line.replace(b'\xb5',b'u')
                    line = line.replace(b'\xbf',b' ')#add if others found
                    line = line.decode().strip()
                
                if line.startswith('#DEFINE'):
                    t = line.split()
                    marcodef.append(t[1])
                
                if line.startswith('#IFDEF'):
                     t = line.split(line)
                     if not(t[1] in marcodef):
                         passline = True
                if line.startswith('#ELSE'):
                     passline = not(passline)
                if line.startswith('#ENDIF'):
                     passline = False

                if passline:
                    # print(line,marcodef)
                    pass
                else:
                
                    if 'VARIABLE' in line:
                        t = line.split()
                        # assert len(t) ==3 , "%s can not be read"%(line) TODO
                        if len(t) >= 3:
                            variable[t[1]] = t[2] 
                    
                    if '{' in line:
                        rule_name = line.split()[0]
                        for t in layer_name_out:
                            if rule_name.startswith(t):
                                cache = True
                                rule = t
                    if cache:
                        if '@' in line:
                            line = line[line.find('@'):]
                            line = line.replace('^', ' ^')
                            line = line.replace(']', ' ]')
                            line = line.replace('[', '[ ')
                            line = line.replace(')', ' )')
                            line = line.replace('(', '( ')                        
                            #replace variable
                            new_line = ''
                            for t in line.split():
                                if t.startswith('^'):
                                    t = t.replace('^','')
                                    t = t.replace(',','')
                                    t = t.replace('.','')                               
                                    # print('ss',t,self.tech_name)
                                    new_line += variable[t] + ' '
                                else:
                                    new_line += t + ' '
                            layer_name_dict[rule].append(new_line + '\n')
                            # cache += line
                        if '}' in line:                       
                            # out_file.write(cache)
                            cache = False
                            # cache = ''      
                            rule = ''
        # print(layer_name_dict)
        rule_list = self.rule_list.copy()
        for l in self.layer_list:
            out_layer = self.layer_match[l][0]
            out_file.write("@"*60 + '\n')
            out_file.write("@layer: %s, target PDK name is %s:"%(l,out_layer) + '\n')
            for rule in rule_list:
                if rule.layer1 == l:
                    out_file.write(rule.write_drc() + '\n')  
                    # rule_list.remove(rule)
            for line in layer_name_dict[out_layer]:
                out_file.write(line)
        # if len(rule_list) == 0:
        #     logger.info("tech->all rules are extracted")
        # else:
        #     print(rule_list)
        #     raise ValueError("layer list is different with calibre")
                
        
        out_file.close()             
        
        # for layer_name in layer_name_dict:
        #     out_file.write("*"*20 + '\n')
        #     out_file.write(layer_name + '\n')
        #     for line in layer_name_dict[layer_name]:
        #         out_file.write(line)
        # out_file.close()        
                



    def check_rules(self):
        for rule in self.rule_list:
            if rule.v < 0:
                return False
        return True






























