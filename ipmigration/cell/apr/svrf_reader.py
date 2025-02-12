# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""

#calibre rule deck reader


import os
import re
import collections
import pandas as pd#'2.0.3'
import numpy as np #version '1.26.4'
import spacy #'3.7.5'


from src.basic.rule import DR

DEBUG = True
DEBUG = False
unit_multipliers = {
    'T': 1e12,
    'G': 1e9,
    'X': 1e6,
    'MEG': 1e6,
    'K': 1e3,
    'M': 1e-3,
    'U': 1e-6,
    'N': 1e-9,
    'P': 1e-12,
    'F': 1e-15
}   

def str2float(val):
    unit = next((x for x in unit_multipliers if val.endswith(x.upper()) or val.endswith(x.lower())), None)
    numstr = val if unit is None else val[:-1*len(unit)]
    return float(numstr) * unit_multipliers[unit] if unit is not None else float(numstr)


# Token specification
modifiers = '|'.join(unit_multipliers.keys()) # 'T|G|X|MEG|K|M|U|N|P|F'
numericval = fr'[+-]?(?:0|[1-9]\d*)(?:[.]\d+)?(?:E[+\-]?\d+)?(?:{modifiers})?' #fr means {} can be used
identifier = r'[^\s{}()=;*]+'
operator = r'\s*[*+-/%]\s*'
exprcontent = fr'(?:{numericval}|{identifier})(?:{operator}(?:{numericval}|{identifier}))*'
commentchars = r'(?:[;$]|//)'

token_re_map = {
    'ANNOTATION': fr'(^|\s)*(\*|{commentchars})+\s*\@:\s*[^\n\r]*',
    'NLCOMMENT': r'(^|[\n\r])+\*[^\n\r]*',
    'COMMENT': fr'(^|\s)*{commentchars}[^\n\r]*',
    'CONTINUE': r'(^|[\n\r])+\+',
    'CONTINUEBACKSLASH': r'\\\s*[\n\r]',
    'NEWL': r'[\s]*[\n\r]+',
    'EQUALS': r'\s*=\s*',
    'EXPR': fr"""(?P<quote>['"]){exprcontent}(?P=quote)|({{){exprcontent}(}})""",
    'NUMBER': numericval + fr'(?=\s|\Z|{commentchars})',
    'DECL': fr'\.{identifier}',
    'NAME': identifier,
    'WS': r'\s+'}
spice_pat = re.compile('|'.join(fr'(?P<{x}>{y})' for x, y in token_re_map.items()), flags=re.IGNORECASE)
Token = collections.namedtuple('Token', ['type', 'value'])


keywords = ['#DEFINE', '#IFDEF', '#ELSE', '#ENDIF', '#IFNDEF',
            'LAYOUT', 'DRC', 'LVS','VIRTUAL', 'PRECISION', 
            'RESOLUTION','TEXT','FLAG', 'ATTACH','LABEL',
            'PORT','LAYER', 'CONNECT', 'SCONNECT', 'VARIABLE','GROUP',
            '#ENCRYPT','#ENDCRYPT','POLYGON','['
            ] 


class RuleFile:
    def __init__(self, tech_name,  cal_file, tech_align_file, dr_template,kws_file, trained_model='md', alpha=0.5):       
        self.tech_name = tech_name
        self.dir_path = os.path.dirname(cal_file)
        # self.layer_list = ['GT'] 
        self.alpha =alpha

        self.read_dr_template(dr_template)
        self.read_tech_align(tech_align_file)
        self.read_kws_file(kws_file)
        
        self.preprocess(cal_file)
        if trained_model == 'lg':
            self.nlp_engine = spacy.load("en_core_web_lg")
        else:
            self.nlp_engine = spacy.load("en_core_web_md")     
        
        
        # self.extract_rules()
        # print('aaa',len(lines),len(self.data))

    def preprocess(self, file):
        #clear rule file comment, remove gbk codec can't decode
        #TODO, add a decode examine function
        
        self.braces_data = {}
        
        f = open(file,'rb')
        text = f.read()
        f.close()
        
        try:
            text = text.decode().strip()
        except:
            #non utf-8 decode
            text = text.replace(b'\xb5',b'u')
            text = text.replace(b'\xbf',b' ')
            text = text.decode().strip()
        # print(text)
        p0 = r'//.*'
        p1 = r'\/\*(?:[^\*]|\*+[^\/\*])*\*+\/'  
        p2 = r'//.*?\n' #shortest match
 
        text = re.sub(p0, '\n', text, count=0, flags=0)
        text = re.sub(p1, '\n', text, count=0, flags=0)
        text = re.sub(p2, '\n', text, count=0, flags=0)
        
        #replace  {} in @xxx with  ()
        text_t = ''
        for line in text.split('\n'):
            line = line.strip()
            if line:
                #OD2.W.2 { @ Width of {OD2 OR {NW OR NT_N}} >= 0.34 
                #OD2.W.2 { @ Width of {OD2 OR {NW OR NT_N}} >= 0.34  xxxxx}
                #@ Waive if there is redundant CT in the same {(M1[A] and AA intersection) or (M1[A] and GT intersection) } 
                if ('@' in line) and ('{' in line) and ('}' in line):
                    s1,s2 = line.split('@')
                    if (s2.count('}') - s2.count('{') == 1) and s2[-1] == '}':
                        s2 = s2[-1]
                        s2 = s2.replace('}',' ').replace('{',' ') + '}'
                    else:
                        s2 = s2.replace('}',' ').replace('{',' ')

                    line = s1 + '@' + s2
                 
                text_t += line+'\n'
        text = text_t
        
        
        
        braces = r'\{(.*?)\}'
        matches = re.findall(braces, text, re.DOTALL) # learned by kimi

        count = 1        
        # print(result0)
        for match in matches:
            tag = 'brace_data_%.10d'%(count)
            self.braces_data[tag] = match
            if '{%s}'%(match) in text:
                # print('bbb',match)
                text = text.replace('{%s}'%(match), '\n'+tag, 1)#first encounter 
                count += 1
            else:
                raise ValueError

        self.cache = [t.strip() for t in text.split('\n') if t.strip()]

        test = True
        if test:
            f = open(file + '_test','w')
            f.write(text)
            f.close()

        # return text
        

    def pop_data(self):
        if len(self.cache) == 0:
            return False, None, None, None
        else:    
            line = self.cache.pop(0)
            # print(line)
            found_keyword = False
            for word in keywords:
                if line.startswith(word):
                    found_keyword = True
                    return True, 'FUNC', line, word
            if not(found_keyword):
                if '=' in line:     
                    return True,'EXPR', line, None
                elif 'brace_data' in self.cache[0]:
                    return True, 'RULE', line, self.cache.pop(0)      
                else:
                    print('error',line)
                    raise ValueError

    def extract_rules(self):
        self.cal_rules = {t:[] for t in self.layer_list}
        self.layer_name2cal = {} #name to number
        self.layer_cal2name = {} #number to name
        self.layer_name2gds = {} #name to gds
        self.defined = {}
        self.variables = {}        
        self.if_define = False
        
        self.ignore = False
        
        # count= {}
        while(1):
            result, token_type, token, data_tag = self.pop_data()
            # print(self.ignore)
            if data_tag == '#ELSE':
                self.ignore = not(self.ignore)
            elif data_tag == '#ENDIF':
                self.ignore = False  
            
            if not(self.ignore):
                if token_type == 'RULE':
                    rule = RuleCheck(token, self.braces_data[data_tag], self.kws_map)
                    if rule.layer:
                        if rule.layer in self.layer_list:
                            # print('test',rule.name, rule.comment)
                            comments = rule.process_comments()
                            self.cal_rules[rule.layer] += comments
                
                if token_type == 'EXPR':
                    pass
                    #TODO Temporary can not process expression because of internal functions
                
                
                if token_type == 'FUNC':
                    if data_tag == '#DEFINE':
                        words = token.split()
                        if len(words) == 3:
                            self.defined[words[1]] = words[2]
                            if  words[2].replace('.','0').isnumeric(): 
                                self.variables[words[1]] = float(words[2]) 
                            else:
                                self.variables[words[1]] = words[2] 
                        elif len(words) == 2:
                            self.defined[words[1]] = None  
                        else:
                            raise ValueError(words)
    
                    elif data_tag == '#IFDEF' or data_tag == '#IFNDEF': # '#IFDEF', '#ELSE', '#ENDIF', '#IFNDEF',
                        words = token.split()
                        if words[1] in self.defined:
                            if len(words) == 3:
                                if  words[2].replace('.','0').isnumeric(): 
                                    if float(words[2]) == self.defined[words[1]]:
                                        if data_tag == '#IFDEF':
                                            self.ignore = False   
                                        if data_tag == '#IFNDEF':
                                            self.ignore = True  
                                    else:
                                        if data_tag == '#IFDEF':
                                            self.ignore = True   
                                        if data_tag == '#IFNDEF':
                                            self.ignore = False 
                                else:
                                    if words[2] == self.defined[words[1]]:
                                        if data_tag == '#IFDEF':
                                            self.ignore = False   
                                        if data_tag == '#IFNDEF':
                                            self.ignore = True  
                                    else:
                                        if data_tag == '#IFDEF':
                                            self.ignore = True   
                                        if data_tag == '#IFNDEF':
                                            self.ignore = False              
                                    
                            else:
                                if data_tag == '#IFDEF':
                                    self.ignore = False   
                                if data_tag == '#IFNDEF':
                                    self.ignore = True      
                        else:
                            if data_tag == '#IFDEF':
                                self.ignore = True   
                            if data_tag == '#IFNDEF':
                                self.ignore = False                              
                        
                    elif data_tag == 'VARIABLE':
                        words = token.split()
                        if len(words) == 3:
                            if  words[2].replace('.','0').isnumeric(): 
                                self.variables[words[1]] = float(words[2]) 
                            else:
                                if words[2] in self.variables:
                                    self.variables[words[1]] = self.variables[words[2]]
                                else:
                                    try:
                                        t = eval( words[2],self.variables)
                                        self.variables[words[1]] = t
                                    except:
                                        pass
                
            if not(result):
                break
  
                
    def read_LAYER(self,token):
        '''
        create a relationship between laymap and calibre 
        
        Layer
            Specification statement
            Specifies input layer names and numbers to be used in the rule file.
            Usage
            LAYER name original_layer [original_layer …]
        Layer Map
            Specification statement
            Specifies datatype or texttype maps from GDSII or OASIS 
            input to Calibre layer numbers. Used only in Calibre.
            Usage
            LAYER MAP source_layer {DATATYPE source_type target_layer 
            | TEXTTYPE source_type target_layer [target_texttype]}


        Layer Resolution
            Specification statement
            Overrides the default Resolution specification statement 
            parameters for any number of original layers during 
            off-grid vertex checking for Flag Offgrid, Drawn Offgrid, 
            Offgrid, Snap Offgrid, or the ICrules CHEck DRc -FLAGOFFGRID option.
        
        Layer Directory
            Specification statement
            Specifies a directory for disk-based layer storage to be used by 
            the verification application. Not 
            used in Calibre nmLVS or Calibre xRC applications.
            Usage
            LAYER DIRECTORY filename
        
        '''        
        tokens = [t.strip() for t in token.split()]
        
        if 'MAP' in tokens:
            #get layer_cal2name
            for name, nums in self.layer_name2cal.items():
                for num in nums:
                    self.layer_cal2name[num] = name
            
            if 'DATATYPE' in tokens:
                index = tokens.index('DATATYPE')
                
            elif 'TEXTTYPE' in tokens:
                index = tokens.index('TEXTTYPE')
            else:
                raise ValueError(token)
            
            layer_num = tokens[2:index]
            layer_dt  = tokens[index+1:-1]
            cal_layer = tokens[-1]
            assert len(layer_num) ==1          
            # print('aaa',layer_num,layer_dt,cal_layer)
            
            

        else:
            self.layer_name2cal[tokens[1]] = []
            for t in tokens[2:]:
                if t.isdigit():
                    self.layer_name2cal[tokens[1]].append(int(t))
                elif t in self.layer_name2cal:
                    self.layer_name2cal[tokens[1]] = self.layer_name2cal[tokens[1]] + self.layer_name2cal[t]
                else:
                    if tokens[1] not in ['RESOLUTION','DIRECTORY']:
                        raise ValueError(tokens)

    def gen_dr_file(self, file):
        self.search_result = {}
        count=0
        for name, rule in self.rules.items():
            #search 
            cal_scores  = []
            cal_name    = []
            cal_comment = []
            cal_values  = []
            cal_rules = self.cal_rules[rule.layer1]
            if rule.layer1 != rule.layer2:
                cal_rules += self.cal_rules[rule.layer2]
            
            for cal_rul in cal_rules:
                rule_name,rule_comment, symbol, value, value_type,init_comment = cal_rul
                doc1 = self.nlp_engine(rule_comment.lower() )
        
                score_sim = []
                score_pos = 0
                score_neg = 0            
                score_ico = 0
                for token in rule.tokens:

                    doc2 = self.nlp_engine(u'%s'%(token))
                    # print(len(doc1),len(doc2),doc2)
                    
                    score_sim.append(self.simularity(doc1,doc2))
                for pos_v in rule.pos_v:
                    if pos_v in rule_comment:
                        score_pos += 0.1
                for ico_v in rule.ico_v:
                    if ico_v in rule_comment:
                        score_ico += 0.4       
                
                for neg_v in rule.neg_v:
                    if neg_v in rule_comment:
                        score_neg -= 0.2             
                if DEBUG:
                    print('***************************%s*********************'%(name))
                    print(rule_name, rule_comment, score_sim, score_pos, score_neg,score_ico )
                cal_scores.append([max(score_sim), score_pos, score_neg,score_ico])
                cal_name.append(rule_name)
                cal_comment.append(rule_name + ': \n' + rule_comment + '\n' + init_comment)
                cal_values.append((value,value_type))
                
            # print(cal_scores)
            loc = np.argmax(np.sum(cal_scores,axis=1))
            rule_score = cal_scores[loc]
            rule_comment = cal_comment[loc]
            rule_value = cal_values[loc]
            rule_name = cal_name[loc]
            
            value = self.extract_value_nm(rule_value)
            self.search_result[name] = rule_name
            if DEBUG:
                print('$$$$$$$$$$$$$$$$')
                print('Rule:', name, value,rule_score)
                print('Comment: ', rule_comment)
            for i,r in self.df.iterrows():
                if name == r['rule']:
                    self.df.at[i,'value'] = value
                    self.df.at[i,'description'] = rule_comment
            
            # count+=1
            # if count>11:
            #     return  self.search_result
            #     break
        
        self.df.to_excel(file)   
        return  self.search_result


    def extract_value_nm(self,rule_value):
        value,value_type = rule_value
        if value_type == 'NUM':
            return int(1000*value)
        elif value_type == 'VAR':
            return int(1000*self.variables[value.replace('^','')])
        else:
            return -0.999
            
        
        
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
        
        self.layer_match = {} #cell to calibre
        
        for layer in self.layer_list:
            assert layer in ascell_layers, 'layer %s not found in csv index!'%(layer)
            self.layer_match[layer] = layer_match[layer]        
        self.layer_match_r = {v[0]: k for k, v in  self.layer_match.items()} # calibre to cell

    def read_dr_template(self,dr_template):
        self.rules = {}
        self.layer_list = []
        df = pd.read_excel(dr_template)
        self.df = df
        for i,r in df.iterrows():
            rule = r['rule'].strip()
            layer1 = r['layer1'].strip()
            layer2 = r['layer2'].strip()
            value = 0
            note = r['description'].strip()
            pos_v = r['positive'].strip()
            neg_v = r['negative'].strip()
            if r['iconic'] != 'none':
                ico_v = r['iconic'].strip()
            else:
                ico_v=''
            
            self.rules[rule] = DR(name=rule,layer1=layer1,layer2=layer2,
                                  value=value,note=note,pos_v=pos_v, neg_v=neg_v, ico_v=ico_v)
            if not(layer1) in self.layer_list:
                self.layer_list.append(layer1)
            if not(layer2) in self.layer_list:
                self.layer_list.append(layer2)
    def read_kws_file(self, kws_file):
        assert os.path.exists(kws_file), "kws file is not exist"
        df = pd.read_csv(kws_file,index_col=0)
        kws_map1 = {'poly': 'GT','poly': 'GT', 'contact': 'CT', 'active': 'AA',
                    'P+ACTIVE':'P+active', 'P+AA':'P+active',
                    'N+ACTIVE':'N+active', 'N+AA':'N+active'
                    }
        kws_map1_t = {}
        for k,v in kws_map1.items(): # Poly Contact
            new_k = k[0].upper() + k[1:]
            kws_map1_t[new_k] = v
        kws_map1.update(kws_map1_t)  
        kws_map1.update(self.layer_match_r)
        kws_map1_t = {} #
        for k,v in kws_map1.items(): #polys GTs
            kws_map1_t[new_k+'s'] = v+'s'
        kws_map1.update(kws_map1_t) 
        
        
        df_dict = df.to_dict()['map']
        kws_map2 = {}
        kws_map3 = {}
        for k,v in df_dict.items():
            if len(k.strip().split()) == 1:
                kws_map2[k] = v
            else:
                kws_map3[k] = v
        
        
        self.kws_map =[ kws_map1,kws_map2,kws_map3]
    def simularity(self,doc1,doc2):
        t1 = doc1.similarity(doc2)
        t2 = abs(len(doc1) - len(doc2))
        t2 = t2/20    
        return self.alpha*(t1)         
        #generate 

class RuleCheck:
    def __init__(self, name, data, kws_map):
        self.name = name
        self.kws_map = kws_map
        self.comment = []
        self.rules = []
        self.layer = ''
        assert len(data)>0
        
        if '.' in name:
            self.layer = name.split('.')[0]
        elif '_' in name:
            self.layer = name.split('_')[0]
        elif 'DMACRO' in name:
            pass
        elif ':' in name:
            pass
        else:
            print('warning %s not a regular rule name!'%(name))
            # raise ValueError(name)

        if self.layer in self.kws_map[0]:
            self.layer = self.kws_map[0][self.layer]
        else:
            self.layer =  ''
        
        
        for line in data.split('\n'):
            line = line.strip()
            if line:
                if line.startswith('@'):
                    self.comment.append(line[1:])
                else:
                    self.rules.append(line)

    def process_comments(self):
        valid_comment = []
        if len(self.comment) >0:
            for comment in self.comment:
                init_comment = comment
                if not('density') in comment:
                    if self.name in comment:
                        comment = comment.replace(self.name, '')
                    if '=' in comment:
                        comment = comment.replace('=', ' = ')                    
                    for symbol in ['>','<',]:
                        if symbol in comment:
                            comment = comment.replace(symbol, ' %s '%(symbol))   
                    if '>  =' in comment:
                        comment = comment.replace('>  =', '>=') 
                    if '<  =' in comment:
                        comment = comment.replace('<  =', '<=')                         
                    if '=  =' in comment:
                        comment = comment.replace('=  =', '==')     
                    if 'um' in comment:
                        comment = comment.replace('um', ' ') 
                    if 'um2' in comment:
                        comment = comment.replace('um2', ' ') 
                    if ',' in comment:
                        comment = comment.replace(',', ' ') 
                    # desprated
                    # if comment[-1] == '.': #@ Min GT area is 0.038. could not convert string to float: '0.038.'
                    #     comment = comment[:-1]                 
                    
                    #Remove text between () and []   
                    comment = re.sub("([\(\[]).*?([\)\]])", " (x) ", comment)   
                    
                    #replace multi-word kws
                    for kw in self.kws_map[2]:
                        if kw in comment:
                            comment = comment.replace(kw, self.kws_map[2][kw])
                
                    words_list, symbol, value, value_type =  self.extract_value(comment)
                    if value_type:
                        comment = ''
                        for word in words_list:
                            if word in self.kws_map[0]: #now lower() TO and to
                                comment += self.kws_map[0][word] + ' '
                            elif  word.lower() in self.kws_map[1]:
                                comment += self.kws_map[1][word.lower()] + ' '
                            else:
                              comment += word + ' '
                      
                        valid_comment.append([self.name,comment, symbol, value, value_type, init_comment]) 
                        # print(self.name + ': ' ,init_comment, '--->', comment, symbol, value, value_type)

        return valid_comment       
                    
                    
                   
                

    
    def extract_value(self,comment):
        # print(comment)
        symbols = ['>=','<=','==','>','<','is']
        words = list(reversed(comment.split()))
        # if 'Fixed' in words:
        #     print(words)
        for i, word in enumerate(words):
            if i != len(words)-1:
                word = word.strip()
                next_word = words[i+1].strip()
                cond1 = '^' in word
                cond2 = word.replace('.','0').isnumeric()
                cond3 = next_word in symbols
                if cond1 and cond3:
                    comment_t = comment.replace(word,' ')
                    comment_t = comment_t.replace(next_word,' ')
                    return  comment_t.strip().split(), next_word, word, 'VAR'
                elif cond2 and cond3:
                    comment_t = comment.replace(word,' ')
                    comment_t = comment_t.replace(next_word,' ')
                    if word[-1] == '.':
                        word = word[:-1]
                    return  comment_t.strip().split(), next_word, float(word), 'NUM'
        
        return comment, '', '', ''




    def __repr__(self):
        
        return self.name + str(self.comment) 














import matplotlib.pyplot as plt


#test
rul_dir = 'data/rule/'
files = {
          'c153':'data/rule/c153.rul',
          's40' :'data/rule/s40.drc',
          's65' :'data/rule/s65.drc',
          't40' :'data/rule/t40_calibre.drc',
          's110':'data/rule/s110.drc',
          't65' :'data/rule/t65_calibre.drc',
         }
# files = {     't40' :'data/rule/t40_calibre.drc',
#           }

dr_answer_file = 'data/dr_answer.xlsx'

tech_align_file = 'data/tech_align.csv'
dr_template = 'data/dr_template.xlsx'
kws_file =  'data/dr_kws.csv'



right_num = 0
wrong_num = 0

result_df = pd.read_excel(dr_answer_file)
result = result_df.copy()


for tech_name,cal_file in files.items():
    print('***************************%s*********************'%(cal_file))
    dr_file = 'output/%s_design_rule.xlsx'%(tech_name)
    rf = RuleFile(tech_name, cal_file, tech_align_file, dr_template, kws_file)
    rf.extract_rules()
    search_result= rf.gen_dr_file(dr_file)
    # result = {k.strip():v.strip() for k,v in zip(result_df['rule'].tolist(),result_df[tech_name].tolist())}
    
    for i,r in result_df.iterrows():
        name = r['rule'].strip()
        if  name in search_result:
            if search_result[name].strip() == r[tech_name].strip():
                result.at[i,tech_name] = 'Right'
            else:
                result.at[i,tech_name] = 'W: %s %s'%(search_result[name],r[tech_name])
        else:
            result.at[i,tech_name] = 'None'
    print(result[tech_name].value_counts())

# print(result)
    

result.to_csv('result.csv')  
        

   