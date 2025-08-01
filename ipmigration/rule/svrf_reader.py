# -*- coding: utf-8 -*-
"""
@author: leiyuan
"""

#calibre rule deck reader


import os
import re
import collections
import json
import pandas as pd#'2.0.3'
import numpy as np #version '1.26.4'
import ollama
from ollama import Client


def str2float(val):
    unit = next((x for x in unit_multipliers if val.endswith(x.upper()) or val.endswith(x.lower())), None)
    numstr = val if unit is None else val[:-1*len(unit)]
    return float(numstr) * unit_multipliers[unit] if unit is not None else float(numstr)


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
            '#ENCRYPT','#ENDCRYPT','POLYGON','[', 
            ] 


class RuleFile:
    def __init__(self, args):       
        self.format = "svrf"
        self.tvf_rules = None
        self.tech_name = args.tech_name
        self.dir_path = os.path.dirname(args.drc_deck)
        self.read_layer_def(args.layer_def)
        if args.drs:
            self.read_drs(args.drs)
        self.save_dir = args.save_dir
        self.client_host = args.client_host
        self.model = args.client_model

        self.output_mode = args.output_mode
        self.debug = args.debug
        self.command = 'ipmigration/rule/pe/command_v1.txt'
        self.review = 'ipmigration/rule/pe/review_v1.txt'
        self.revise = 'ipmigration/rule/pe/revise_v1.txt'
        self.preprocess(args.drc_deck)
                    
    
    def preprocess(self, file):
        file_name = os.path.basename(file)
        self.file_name = file_name
        temp_dir = os.path.join(self.save_dir,'temp')
        if not(os.path.exists(temp_dir)):
            os.mkdir(os.path.join(self.save_dir,'temp'))
        
        f = open(file,'rb')
        text = f.read()
        f.close()
        
        #clear rule file comment, remove gbk codec can't decode
        #TODO, add a decode examine function
        try:
            text = text.decode().strip()
        except:
            #non utf-8 decode
            text = text.replace(b'\xb5',b'u')
            text = text.replace(b'\xbf',b' ')
            try:
                text = text.decode().strip()
            except:
                raise ValueError("non utf-8 decode found")
        
        if "namespace import tvf" in text:
            self.format = "tvf"

            
        if self.format == 'svrf':
            text = self.clean_comment_svrf(text)
            text,bracket_dic = self.extract_bracket_svrf(text)
            self.bracket_dic = bracket_dic

            # text = self.preprocess_svrf(text)
        else:
            svrf_text,rulecheck_dic = self.tvf_to_svrf(text)
            text = self.clean_comment_svrf(svrf_text)
            text,bracket_dic = self.extract_bracket_svrf(text)
            self.bracket_dic = bracket_dic

        self.cache = [t.strip() for t in text.splitlines() if t.strip()]


        if self.debug:
            f = open(os.path.join(temp_dir,file_name + '_clean'),'w')
            f.write(text)
            f.close()
            f = open(os.path.join(temp_dir,file_name + '_bracket'),'w')
            for i,v in bracket_dic.items():
                f.write("%s++++++++++++++++++++++\n"%(i))
                f.write("%s\n"%(v))
            f.close()
        
    @staticmethod
    def extract_bracket_svrf(text, l='{',r='}'):
        l_n=0 
        r_n=0 
        new_text = ''
        cache = ''
        cache_0 = ''     
        
        load_bracket= False
        bracket_str=''
        bracket_dic={}
        
        special_c = [' ', '\n', '\r' ,'\t']
        
        def char_generator(string):
            yield from string
        
        gen = char_generator(text)
        while True:    
            try:
                c=next(gen)                
                if load_bracket:
                    bracket_str += c 
                    if c == l:
                        l_n += 1
                    if c == r:
                        r_n += 1
                    
                    # print('##',l_n,r_n)
                    if l_n==r_n and l_n>0:
                        l_n=0 
                        r_n=0
                        load_bracket = False        
                        bracket_dic[cache_0] =  bracket_str
                        cache_0 = ''
                        cache = ''
                        bracket_str = ''
                        
                else:
                    new_text+=c
                    if c in special_c or c == l:
                        # raise ValueError
                        if cache != '':
                            cache_0 = cache
                            cache=''
                        if c == l:
                            if new_text[-2] == '\n' or new_text[-1] == '\r':
                                new_text = new_text[:-2] + l
                            new_text+='bracket%s'%(r)
                            l_n += 1
                            load_bracket = True     
                    else:
                        cache+=c

            except StopIteration:
                break
        
        return new_text, bracket_dic       
 
    @staticmethod
    def extract_bracket_tvf(text, l='{',r='}'):
        l_n=0 
        r_n=0 
        new_text = ''
        cache = ''
        cache_0 = ''   
        cache_1 = ''
        
        load_bracket= False
        bracket_str=''
        
        verbatim_list=[]
        rulecheck_dic={}
        
        special_c = [' ', '\n', '\r' ,'\t']
        
        def char_generator(string):
            yield from string
        
        gen = char_generator(text)
        while True:    
            try:
                c=next(gen)                
                if load_bracket:
                    bracket_str += c 
                    if c == l:
                        l_n += 1
                    if c == r:
                        r_n += 1
                    
                    # print('##',l_n,r_n)
                    if l_n==r_n and l_n>0:
                        l_n=0 
                        r_n=0
                        load_bracket = False        
                        if cache_1 == 'RULECHECK':
                            rulecheck_dic[cache_0] = bracket_str
                        elif cache_0 == 'VERBATIM':
                            verbatim_list.append(bracket_str[:-1])
                        
                        cache_0 = ''
                        cache_1 = ''
                        cache = ''
                        bracket_str = ''
                        
                else:
                    new_text+=c
                    if c in special_c or c == l:
                        # raise ValueError
                        if cache != '':
                            cache_1 = cache_0
                            cache_0 = cache
                            cache=''
                        if c == l:
                            new_text+='bracket%s'%(r)
                            l_n += 1
                            load_bracket = True     
                    else:
                        cache+=c

            except StopIteration:
                break
        
        return rulecheck_dic, verbatim_list  
 
    
    def clean_comment_svrf(self,text):
        # p0 = r'//.*'

        p1 = r'//.*?\n' #shortest match
        p2 = r'\/\*(?:[^\*]|\*+[^\/\*])*\*+\/'  
        # text = re.sub(p0, '\n', text, count=0, flags=0)
        text = re.sub(p1, '\n', text, count=0, flags=0)
        text = re.sub(p2, '\n', text, count=0, flags=0)
        
        new_text = ''
        for line in text.splitlines():
            line = line.strip()
            if line:
                new_text+=line+'\n'
        
        return new_text
    
    '''
    deprecated    
    def preprocess_svrf(self,text,count=1):

        
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
        matches = re.findall(braces, text, re.DOTALL) # 

        count = count       
        # print(result0)
        for match_ in matches:
            tag = 'brace_data_%.10d'%(count)
            self.braces_data[tag] = match_
            if '{%s}'%(match_) in text:
                # print('bbb',match)
                text = text.replace('{%s}'%(match_), '\n'+tag, 1)#first encounter 
                count += 1
            else:
                raise ValueError
        
        return text
    '''    
    
    def tvf_to_svrf(self,text):
        self.tvf_text = text #backup
        #clean tvf comment
        
        #if
        # pattern = re.compile(r'\bif\s+\{.*?\}\s+\{.*?\}', re.DOTALL) # re.DOTALL next line
        # results = pattern.findall(text)
        #extract set foreach add 
        temp_var = {}
        for line in text.splitlines():
            line = line.strip()
            if ';' in line:
                line = line.split(';')[0].strip()
            if line.startswith('set') and ('{' in line) and  line.endswith('}'):
                pattern = re.compile(r'\{(.*?)\}')
                value = pattern.findall(line)[0]
                value = value.strip().replace(' ','_')
                temp_var[line.split()[1]] = value
                
            if line.startswith('foreach') and ('$' in line):
                for word in line.split():
                    if word.startswith('$'):
                        if word[1:] in temp_var:
                            for_ = line.split()[1]
                            if not(for_ in temp_var):
                                temp_var[for_] = temp_var[ word[1:]]
             
                        
        
        pattern = re.compile(r'\$\{(.*?)\}')
        matches = pattern.findall(text)

        for m in matches:
            if m in temp_var:
                text = text.replace('${%s}'%(m), temp_var[m])
            else:
                text = text.replace('${%s}'%(m),'NOTFOUND')
        
        # temp_dir = os.path.join(self.save_dir,'temp')
        
        # f = open(os.path.join(temp_dir, 'test0'),'w')
        # f.write(text)
        # f.close()
 

        rulecheck_dic, verbatim_list = self.extract_bracket_tvf(text)
        
        self.tvf_rules = rulecheck_dic
        svrf_text = ''
        for s in verbatim_list:
            svrf_text+=s
            
        if self.debug:
            temp_dir = os.path.join(self.save_dir,'temp')
            
            f = open(os.path.join(temp_dir, 'test1'),'w')
            f.write(svrf_text)
            f.close()
            
            f = open(os.path.join(temp_dir, 'test2'),'w')
            for i,v in rulecheck_dic.items():
                f.write("%s++++++++++++++++++++++\n"%(i))
                f.write("%s\n"%(v))
            f.close()
        

        return svrf_text,rulecheck_dic

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
                elif '{bracket}' in line:
                    rule_name = line.split('{')[0].strip()
                    for layer in self.layers:
                        if rule_name.startswith(layer):
                            return True, 'RULE', rule_name, None   
                    #not in layer list or others
                    return True, None, None, None
                else:
                    print('warning!: ',line)
                    return True, None, None, None
                    #raise ValueError

    def extract_rules(self):
        self.cal_rules = {t:[] for t in self.layers}
        self.layer_name2cal = {} #name to number
        self.layer_cal2name = {} #number to name
        self.layer_name2gds = {} #name to gds
        self.defined = {}
        self.variables = {}        
        self.if_define = False        
        self.ignore = False

        if self.tvf_rules:
            for i,v in self.tvf_rules.items():
                for layer in self.layer_match_r:
                    if i.startswith(layer):
                        rule = RuleCheck(i, v, self.kws_map,self.variables)
                        if rule.layer:
                            if rule.layer in self.layer_list:
                                # print('test',rule.name, rule.comment)
                                # comments = rule.process_comments()
                                if rule.comment:
                                    self.cal_rules[rule.layer].append(rule)
        

        while(1):
            result, token_type, token, data_tag = self.pop_data()
            # print(self.ignore)
            if data_tag == '#ELSE':
                self.ignore = not(self.ignore)
            elif data_tag == '#ENDIF':
                self.ignore = False  
            
            if not(self.ignore):
                if token_type == 'RULE':
                    # print('test1:',self.variables)
                    rule = RuleCheck(token, self.bracket_dic[token], self.variables)
                    if rule.layer:
                        if rule.layer in self.layers:
                            # print('test',rule.name, rule.comment)
                            # comments = rule.process_comments()
                            if rule.comment: #not density
                                self.cal_rules[rule.layer].append(rule)
                
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
                # pass
                break
  
        #extract and process rules of select layer     

        data =[]
        df = pd.DataFrame(columns=['layer','layer_def', 'dr', 'comment'])
        for layer,rules in self.cal_rules.items():
            if len(rules)>0:
                for rule in rules:
                    data = [layer,self.layers[layer],rule.name,rule.comment]
                    df.loc[len(df)] = data
        self.bracket_dic = {}
        self.cal_rules = {}#clear cache
        self.dr_df = df
        self.parse_data(df)

        
        
        # print(df)
                # print(rules_dict) 
        #         ers = self.llm.response(rules_dict)   
        #         # print('test1:',ers)
        #         assert len(ers) != 0, 'llm may not work!'
        #         for er in ers[1:]:
        #             if len(er) == 4:
        #                 data.append({'Layer':rule_layer,'Rule':er[0],'Category':er[1],'Description':er[2],'Value':er[3]})
        #             else:
        #                 print("Warning: Rule not extracted:", er)
        # df = pd.DataFrame(columns=['Layer','Rule','Category','Description','Value'],data=data)
        # self.extracted_file = os.path.join(self.save_dir, self.file_name + '_extract_rules.csv')
        # df.to_csv(self.extracted_file)
        
    def parse_data(self,df):
        with open(self.command,'r') as f:
            command = f.read()
        
        self.extracted_dr = []
        all_data = []
        client = Client(host=self.client_host)
        for layer in self.layers:
            print('\n-----------------------%s:%s----------------------------\n'%(self.tech_name,layer))
            layer_data = []
            df_layer = df[df.layer==layer]
            if len(df_layer) ==0:
                print('No design rule data for layer %s'%(layer))
            else:
                for i,r in df_layer.iterrows():
                    data = {"design rule":r.dr,"layer":r.layer,"layer description":r.layer_def, "rule description":r.comment}

                    messages = [
                                {"role": "user", "content": command},
                                {"role": "user", "content": str(data)},
                                ]

                    response = client.chat(self.model, messages)
                    response_content,answer = self.extract_response(response)
        
                    print('**input**: rule:%s, comment:%s'%(r.dr,r.comment))
                    # print('**ouput**:',answer)
                    try:
                        result = self.extract_jsons(answer)[0]
                        data['classification'] = result['classification']
                        data['symbol'] = result['symbol']
                        data['value'] = result['value']
                        if self.output_mode  == 'single':
                            all_data.append(data)
                        else:
                            layer_data.append(data)
                        print('**ouput**:',result)
                    except:
                        print('**parse_error**:', answer)
                        #TODO: There are no problems encountered so far, but issues may arise, and the reflection module needs to be updated according to specific problems.
                        # raise ValueError()
        
            if self.output_mode  == 'split':
                layer_file = os.path.join(self.save_dir,self.tech_name + '_' + layer + '.csv')
                layer_df = pd.DataFrame(layer_data)
                layer_df.to_csv(layer_file, index=False)
           
        
        if self.output_mode  == 'single':
            layers_file = os.path.join(self.save_dir,self.tech_name + '_all.csv')
            layers_df = pd.DataFrame(all_data)
            layers_df.to_csv(layers_file, index=False)       
            
            
                # layer_df = pd.DataFrame(columns=columns,data=all_data)    
                # layer_file = os.path.join(self.save_dir,self.tech_name + '_rules.csv')
                # layer_df.to_csv(layer_file, index=False)
                # review_result,review_content, review_message= self.reflection(answer)
                # print('**review**:',review_result)

                # if review_result:
                #     csv_text = answer
                # else:
                #     print("**begin revise**: ")
                #     # messages.append({"role": "assistant", "content": answer})
                #     # messages.append(review_message)
                #     # messages.append({"role": "user", "content": review_content})
                #     review_result,answer= self.revision(messages)
                #     if review_result:
                #         csv_text = answer
                #     else:
                #         print("**begin 2nd revise**: ")
                #         review_result,answer= self.revision(messages)
                #         if review_result:
                #             csv_text = answer
                #         else:
                #             csv_text = ''
                # print('**ouput**:',csv_text)
                # csv_data = self.extract_csv_data(csv_text)
                # print('**csv_data**:',csv_data)
                # layer_rule = {}
                # for d in csv_data:
                #     layer_rule[d[0]] = [d[1],d[3],d[4]]
                # for i,r in df_layer.iterrows():
                #     if r.dr in layer_rule:
                #         rule_t,rule_s,rule_v = layer_rule[r.dr]
                #         rule_data = [r.layer,r.layer_def,r.dr,r.comment,rule_t,rule_s,rule_v]

                #         print('rule:',rule_data)
                #         #layer_file = os.path.join(self.save_dir,self.tech_name + '_' + layer + '.csv')
                #         all_data.append(rule_data)
                #     else:
                #         #TODO: may have some rules are missed
                #         pass
  
    @staticmethod
    def extract_response(response):          
        # print('response type:',type(response))
        # print(response)
        if isinstance(response, dict) and "message" in response and "content" in response["message"]:
            response_content = response["message"]["content"]
        elif isinstance(response, ollama._types.ChatResponse):
            response_content = response.message.content
        else:
            #print()
            response_content = "<think>NA</think>NA"
        answer = response_content.split('</think>')[-1]           
        return response_content,answer
    @staticmethod
    def extract_jsons(text):
        pattern = r'\{[\s]*"classification":\s*"[^"]+",[\s]*"symbol":\s*"[^"]+",[\s]*"value":\s*"[^"]+"[\s]*\}'
        json_strings = re.findall(pattern, text, re.DOTALL)
        # print(json_strings)
        results = []
        for json_str in json_strings:
            try:
                # 解析JSON字符串
                obj = json.loads(json_str)
                results.append(obj)
            except json.JSONDecodeError:
                print(f"Json Error: {json_str}")
        
        return results
    
    
    def reflection(self, text):
        with open(self.review,'r') as f:
            review = f.read()
        messages = [
            {"role": "user", "content": review + text}
            ]
        client = Client(host=self.client_host)
        response = client.chat(self.model, messages)
        response_content,answer = self.extract_response(response)
        result = ('Yes' in answer) or ('YES' in answer) or ('yes' in answer) 
        return result,response_content, messages[0]

    def revision(self, messages):
        with open(self.revise,'r') as f:
            revise = f.read()

        messages.append({"role": "user", "content": revise})
        client = Client(host=self.client_host)
        response = client.chat(self.model, messages)
        response_content,answer = self.extract_response(response)
        review_result,review_content, review_message = self.reflection(answer)
        return review_result,answer


    
    # @staticmethod
    # def csv_to_list(csv_lines):
    #     # 检测分隔符
    #     if '||' in data:
    #         delimiter = '||'
    #     else:
    #         delimiter = ','
    #     lines = data.split('\n')
    #     reader = csv.reader(lines, delimiter=delimiter)
    #     return list(reader)   
    
    def extract_csv_data(self,csv_text):
        csv_text = csv_text.split('```csv')[-1].split('```')[0]
        csv_lines = [t for t in csv_text.splitlines() if t]
        if '|' in csv_text:
            delimiter = '|'
        else:
            delimiter = ','
    
        result = []
        for line in csv_lines:
            result.append(line.split(delimiter))
        csv_data = list(result)[1:]
        
        return csv_data
        
        
        
    def read_LAYER(self,token):
        '''
        desprecated
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



    def extract_value_nm(self,rule_value):
        value,value_type = rule_value
        if value_type == 'NUM':
            return int(1000*value)
        elif value_type == 'VAR':
            value = value.replace('^','')
            if value.endswith('.'):
                value = value[:-1]
            return int(1000*self.variables[value])
        else:
            return -0.999
            
        
        
    def read_layer_def(self, file):
        assert os.path.exists(file), "layer align file is not exist"
        
        df = pd.read_csv(file)
        self.layers = {}
        for i,r in df.iterrows():
            self.layers[r['layer'].strip()] = r['defination'].strip()
        
        

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
    def __init__(self, name, data, variables):
        self.name = name
        self.comment = []
        self.rules = []
        self.layer = ''
        self.variables =variables
        assert len(data)>0
        
        if '.' in name:
            self.layer = name.split('.')[0]
        elif '_' in name:
            self.layer = name.split('_')[0]
        elif 'DMACRO' in name: #Pass DMACRO
            pass
        elif ':' in name: #?
            pass
        else:
            print('warning %s not a regular rule name!'%(name))
            # raise ValueError(name)

    
        for line in data.split('\n'):
            line = line.strip()
            if line:
                if line.startswith('@'):
                    self.comment.append(line[1:])
                else:
                    self.rules.append(line)

        self.process_comments()

    def process_comments(self):
        valid_comment = ''
        if len(self.comment) >0:
            for comment in self.comment:
                if '^' in comment:
                    # print(comment)
                    new_comment = ''
                    for word in comment.split(' '):
                        if word.startswith('^'):
                            try:
                                # print(self.variables.keys())
                                # print(word[1:], self.variables[word[1:]])
                                new_comment += str(self.variables[word[1:]]) + ' '
                            except:
                                new_comment += word + ' '
                        else:
                            new_comment += word + ' '
                    # print(new_comment)
                    comment = new_comment
                    # raise ValueError
                # init_comment = comment
                # if not('density') in comment: #clear density
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
                if ':' in comment:
                    comment = comment.replace(':', ' ')                      
                    # if 'um' in comment:
                    #     comment = comment.replace('um', ' um ') 
                    # if 'um2' in comment:
                    #     comment = comment.replace('um2', ' um2 ') 
                    
                if ',' in comment: #?
                    comment = comment.replace(',', ' , ') 
                
                valid_comment += comment.strip() + '  '                
        self.comment = valid_comment    
        # return valid_comment      

    '''
    despreated
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
                    # comment = re.sub("([\(\[]).*?([\)\]])", " (x) ", comment)   
                    
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
    '''         
    '''
    deprecated
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
                cond3 = next_word in symbols #error: transistors to trans tor
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
    '''



    def __repr__(self):
        return self.name + str(self.comment) 



class DR(object):
    dr_list =[]
    def __init__(self, name, layer1, value = -9999, layer2='', note='', pos_v ='', neg_v='', ico_v=''):
        self.name = name
        self.layer1 = layer1
        self.value = value
        self.layer2 = layer2
        self.note = note
        self.tokens = [t.strip() for t in note.split('\n')]
        self.pos_v = [t.strip() for t in pos_v.split('\n')]
        self.neg_v = [t.strip() for t in neg_v.split('\n')]      
        
        if ico_v:
            self.ico_v = [t.strip() for t in ico_v.split('\n')] 
        else:
            self.ico_v = []
        # self.run_length = run_length #TODO
        self.dr_list.append(self)
    def __repr__(self):
        return self.name + ' : ' + str(self.value) + 'nm\n' + self.note 
    def write_drc(self):
        return self.name + ' # ' + str(self.value) + ' # ' + self.note 
    
    @property
    def v(self):
        return self.value
    @property
    def h_v(self):
        return int(0.5*self.value)
  