# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 16:01:35 2025

@author: leiyuan
"""


# Please install OpenAI SDK first: `pip3 install openai`

# import pandas as pd

import json
from openai import OpenAI #versiopn = '1.60.0'

urls   = {"deepseek-ol": "https://api.deepseek.com" ,
          "moonshot": "https://api.moonshot.cn/v1" }

models   = {"deepseek-ol": "deepseek-chat" ,
            "moonshot": "moonshot-v1-8k" }


prompts = json.load(open("./ipmigration/rule/apis/prompt.json",'r'))


class API:
    def __init__(self,name, api,prompts=prompts,urls=urls,models=models):
        self.name = name
        self.prompt = prompts[name]['prompt']
        self.url = urls[name]        
        self.client = OpenAI(api_key=api, base_url=self.url)
        self.model = models[name]
        
    @staticmethod
    def search_available_llm(apis):
        available_llm = []
        names = list(urls.keys())
        print("Searching available LLM models")
        for name in names:
            print('Test if %s is avaliable.'%(name))
            try:
                client = OpenAI(api_key=apis[name]['api'], base_url=urls[name])
                response = client.chat.completions.create(
                    model= models[name],
                    messages=[
                        {"role": "user", "content": "please answer yes"},
                    ],
                    stream=False
                )
                ans = response.choices[0].message.content
                if 'yes' in ans.lower():
                    available_llm.append(name)
                    print('%s is avaliable.'%(name))
                # print(ans)
            except:
                print('!!! %s is not avaliable.'%(name))
            
        
        return available_llm
        
    def response(self,rules):
        print('Begin process rules using %s'%( self.name))
        #rules, dict-> rule_name : rule content
        content =''
        for i,v in rules.items():
            content += '%s : %s \n'%(i,v) 
        
        response = self.client.chat.completions.create(
            model=self.model,
            #TODO prompt once?
            messages=[
                {"role": "system", "content": self.prompt},
                
                {"role": "user", "content": content},
            ],
            stream=False
        )
        return self.process_response(response.choices[0].message.content, list(rules.keys()))
        
     
    def is_valid_response(self,line,rule_names):
        #csv maybe have '||' or '|' delimiter, even if propmt only use '||'
        content = [t.strip() for t in line.split('||')]
        if (content[0] in rule_names) and len(content)>1:
            return content
        else:
            content = [t.strip() for t in line.split('|')]
            if (content[0] in rule_names) and len(content)>1:
                return content
            else:
                return None
        
     
    def process_response(self,response,rule_names):
        print(response)
        csv_content= []
        for line in response.splitlines():
            content = self.is_valid_response(line,rule_names)
            if content:
                # print('test1',content)
                csv_content.append(content)
        return csv_content    

        
        
        
        
        # if self.name == 'deepseek':
        #     load = False
        #     csv_content= []
        #     for line in response.splitlines():
        
        #         if load:
        #             if line.startswith("```"):
        #                 break
        #             else:
        #                 csv_content.append([t.strip() for t in line.split('||')])
        #         if line.startswith("```"):
        #             load = True 
    
        #     return csv_content
        # elif self.name == 'deepseek-ol':
        #     load = False
        #     csv_content= []
        #     for line in response.splitlines():
        
        #         if load:
        #             if line.startswith("```"):
        #                 break
        #             else:
        #                 csv_content.append([t.strip() for t in line.split('||')])
        #         if line.startswith("```"):
        #             load = True 
    
        #     return csv_content
        # elif self.name == 'moonshot':  
        #     csv_content= []
        #     for line in response.splitlines():
        #         csv_content.append([t.strip() for t in line.split('||')])
                
     

