# -*- coding: utf-8 -*-
"""

@author: leiyuan
"""

import json
queue_data = 'ipmigration/cell/apr/pr/place/queue.json'


output_mappings = {
    frozenset({'out_Q', 'out_QN', 'out_Q_2'}): [['out_Q_2'], ['out_Q', 'out_QN']],
    frozenset({'out_Q', 'out_Q_2'}): [['out_Q_2', 'out_Q']],
    frozenset({'out_Q', 'out_QN'}): [['out_Q', 'out_QN']],
    frozenset({'out_Q'}): [['out_Q']],
    frozenset({'out_QN'}): [['out_QN']],
    frozenset({'out_ECK'}): [['out_ECK']]
}



class CircuitSorter:
    def __init__(self, ckt, sub_ckts, place_file, load):
        
        self.ckt = ckt
        self.sub_ckts = sub_ckts
        self.place_file = place_file
        self.load = load
        
        # self.cal_cross()
    
    
    
        if load:
            if self.ckt.ckt_type in  ['ff'       ,'scanff'   ,'latch'     ,'clockgate']:
                self.queue = self.place_file[self.ckt.name]
                self.ready=True
                    
        else:
            # sub_ckts_names = [k + ': ' + v.ckt.name for k,v in self.sub_ckts.items()]
            if self.ckt.ckt_type in  ['ff'       ,'scanff'   ,'latch'     ,'clockgate']:
                queue = self.cal_queue()
                self.write_place_file(queue)
                self.ready=False

    def run(self):
        if self.ckt.ckt_type in  ['ff'       ,'scanff'   ,'latch'     ,'clockgate']:
            place_data = self.sl_place()
        else:
            place_data = self.cl_place()
        return place_data

        
        
        
        #TODO, Split place and route
        return self.route()  
    
    def sl_place(self):
        place_data = []
        # pl = self.pin_loc
        self.queue = split_list_elements(self.queue) 
        for combo in self.queue:
            if len(combo) ==1:
                p = self.sub_ckts[combo[0]]
                place_data.append(p.place)
                
            else:
                if type(combo[0]) is list:
                    t_placement = []
                    if len(combo[0]) == 1:
                        p = self.sub_ckts[combo[0][0]]
                        t_placement += p.place
                    else:
                        p1 = self.sub_ckts[combo[0][0]]
                        p2 = self.sub_ckts[combo[0][1]]    
                        t_placement += p1.flip_place() + p2.place
                    t_placement.append({'P':None,'N':None})
                    if len(combo[1]) == 1:
                        p = self.sub_ckts[combo[1][0]]
                        t_placement += p.place
                    else:
                        p1 = self.sub_ckts[combo[1][0]]
                        p2 = self.sub_ckts[combo[1][1]]                  
                        t_placement += p1.flip_place() + p2.place                 
                        
                    place_data.append(t_placement)  
                    
                    
                else:
                    p1 = self.sub_ckts[combo[0]]
                    p2 = self.sub_ckts[combo[1]]                  
                    place_data.append(p1.flip_place() + p2.place)
        
        # self.show_placement()
        return place_data
    def cl_place(self):
        place_data = []
        for k,p in self.sub_ckts.items():
            place_data.append(p.place)

        # print('cl_place')
        return place_data
    
    
    def cal_cross(self):
        print(self.sub_ckts.keys())
        

    
    
    def cal_queue(self):
        with open(queue_data, 'r') as f:
            data = json.load(f)
        ckt_type = self.ckt.ckt_type 
        if ckt_type == 'latch':
            init_queue = data['queue_la']
        elif ckt_type == 'clockgate':
            init_queue = data['queue_cg']
        elif ckt_type == 'ff':
            init_queue = data['queue_ff']  
        elif ckt_type == 'scanff':
            init_queue = data['queue_sf']
        else:
            raise ValueError('ckt type error!')

        queue_t = {t:[] for t in init_queue}
        ininv = []
        out = []
        #cal queue and out and ininv
        for ckt_name in self.sub_ckts:
            for key in queue_t:
                if ckt_name == key:
                    queue_t[key].append(ckt_name)

            if 'ininv' in ckt_name:
              ininv.append(ckt_name)  
            if 'out' in ckt_name:
                out.append(ckt_name)
        
        out0=[]
        out1=[]
        #process out
        out_set = frozenset(out)
        if out_set in output_mappings:
            out_queue = output_mappings[out_set]
            if len(out_queue) == 1:
                out1 = out_queue[0]
            elif  len(out_queue) == 2:
                out1 = out_queue[1]
                out0 = out_queue[0]

        else:
            raise ValueError(out_set)

        #insert ininv to queue  
        #ininv_r0 is merge with output
        if 'ininv_RN_0' in ininv:
            ininv.remove('ininv_RN_0')
            if len(out1) == 2:
                out0 = ['ininv_RN_0']  + out0
            elif len(out1) == 1:
                out1 = out1 + ['ininv_RN_0']  
        
        if 'ininv_SN_0' in ininv:
            ininv.remove('ininv_SN_0')
            queue_t['cross1'] = ['ininv_SN_0','cross1']
            
        if 'ininv_SE_0' in ininv:
            ininv.remove('ininv_SE_0')
            queue_t['sesi'] = ['ininv_SE_0','sesi']            
       
        if 'ininv_E_0' in ininv:
            ininv.remove('ininv_E_0')
            # print('test1',queue_t)
            out1 = out1  + ['ininv_E_0']           
        
        queue_t['ininv'] = ininv
        for k,v in queue_t.items():
            if not v:
                queue_t[k] = 'NA'
            elif len(v) == 1:
                queue_t[k] = v[0]
            else:
                queue_t[k]  = '-'.join(v)
        

        out0 = '-'.join(out0) if len(out0) > 1 else ''.join(out0) 
        out1 = '-'.join(out1) if len(out1) > 1 else ''.join(out1) 
        if out0:
            queue_t['out'] = out0+'|'+out1 
        else:
            queue_t['out'] = out1 
        
        queue = [v for k,v in queue_t.items() if v != 'NA']
        
        return queue
        
        # print(queue_t,ininv)    
    
    
    
    def write_place_file(self,queue):
        with open(self.place_file,'a+') as f:
            line = '%-10s,'%(self.name)
            ql = len(queue) 
            for i in range(10):
                if i < ql:
                    name = queue[i]
                else:
                    name = 'NA'
                
                line += '%-30s,'%(name)
            f.write(line[:-1]+'\n')
    
    
def split_list_elements(input_list):
    result = []
    for item in input_list:
        if '|' in item:
            sub_items = item.split('|')
            temp = []
            for sub in sub_items:
                temp.append(sub.split('-'))
            result.append(temp)
        elif '-' in item:
            result.append(item.split('-'))
        else:
            result.append([item])
    return result


