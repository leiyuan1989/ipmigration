# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 16:01:35 2025

@author: leiyuan
"""


# Please install OpenAI SDK first: `pip3 install openai`

# import pandas as pd
from openai import OpenAI #versiopn = '1.60.0'


f= open("./ipmigration/rule/apis/deepseek/licence.txt",'r')
licence = f.read()
f.close()

f = open("./ipmigration/rule/apis/deepseek/prompt_drc_v1.txt",'r')
prompt = f.read()
f.close()

class API:
    def __init__(self,licence=licence,prompt=prompt):
        lic = [t.strip() for t in licence.splitlines()]
        self.client = OpenAI(api_key=lic[0], base_url=lic[1])
        self.prompt = prompt
        
    def response(self,rules):
        print('Begin process rules using deepseek-chat')
        #rules, dict-> rule_name : rule content
        content =''
        for i,v in rules.items():
            content += '%s : %s \n'%(i,v) 
        
        response = self.client.chat.completions.create(
            model="deepseek-chat",
            #TODO prompt once?
            messages=[
                {"role": "system", "content": prompt},
                
                {"role": "user", "content": content},
            ],
            stream=False
        )

        return self.process_response(response.choices[0].message.content)
        
        
    def process_response(self,response):
        load = False
        csv_content= []
        for line in response.splitlines():
    
            if load:
                if line.startswith("```"):
                    break
                else:
                    csv_content.append([t.strip() for t in line.split('||')])
            if line.startswith("```"):
                load = True 

        return csv_content