# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 15:22:58 2024

@author: Administrator
"""



#
from circuits import Circuits 
import time
import random


speed = 20

model_cdl = 'model.cdl'
netlist_cdl = 's65.cdl'
pin_align_file = 'pin_align.csv'


def main():
    ckts = Circuits('s65', pin_align_file, model_cdl, netlist_cdl)
    count = 1

    for ckt_name,ckt in ckts.ckt_dict.items():
        with open('log/log_%.5d.txt'%(count),'w') as f:
            write(f,ckt_name,len(ckt.devices))
            f.close()
            count +=1
            
def write(f,ckt,device_num):
    t1 = int(device_num/speed)
    t2 = int(device_num/(speed/2))
    interval = random.randint(t1, t2)
    time.sleep(interval)
    print('%s: Begin processing netlist( %s ), total %d devices.'%(time.asctime(),ckt, device_num))
    f.write('%s: Begin processing netlist( %s ), total %d devices.\n'%(time.asctime(),ckt, device_num))
    f.write('%s: 01 Netlist deconstruction.\n'%(time.asctime()))
    f.write('%s: 02 SubCircuits Merge.\n'%(time.asctime()))
    interval = random.randint(t1, t2)
    time.sleep(interval)
    f.write('%s: 03 Placeing.\n'%(time.asctime()))
    f.write('%s: 04 Grid Generation.\n'%(time.asctime()))
    interval = random.randint(t1, t2)
    time.sleep(interval)
    f.write('%s: 05 Routing.\n'%(time.asctime()))
    f.write('%s: 06 Detail Processing.\n'%(time.asctime()))
    f.write('%s: Successfully processing netlist( %s )\n'%(time.asctime(),ckt))
if __name__ == "__main__":
    main()