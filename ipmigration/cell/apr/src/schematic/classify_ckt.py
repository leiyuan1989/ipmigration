                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    # -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 20:41:25 2024

@author: Administrator
"""

#classify ckts


all_pins_type_with_RSN = [
 {'D', 'RN', 'SN'},
 {'D', 'RN'},
 {'D'},
 {'D', 'E'},
 {'D', 'SN'},
 {'E', 'ECK'},
 {'E', 'ECK', 'SE'},
 {'BC', 'E', 'ECK'},
 {'E', 'ECK', 'FC'},
 {'D0', 'D1'},
 {'D0', 'D1', 'S0'},
 {'D', 'E', 'RN'},
 {'D', 'RN', 'SE', 'SI', 'SN'},
 {'D', 'RN', 'SE', 'SI'},
 {'D', 'SE', 'SI'},
 {'D', 'SE', 'SI', 'SN'},
 {'D0', 'D1', 'SE', 'SI'},
 {'D0', 'D1', 'S0', 'SE', 'SI'},
 {'D', 'E', 'SE', 'SI'},
 {'D', 'E', 'RN', 'SE', 'SI'}]
   

all_pins_type = [
 {'D'},
 {'D', 'E'},
 {'E', 'ECK'},
 {'E', 'ECK', 'SE'},
 {'BC', 'E', 'ECK'},
 {'E', 'ECK', 'FC'},
 
 {'D0', 'D1'},
 {'D0', 'D1', 'S0'},
 
 {'D', 'SE', 'SI'},
 {'D', 'E', 'SE', 'SI'},
 {'D0', 'D1', 'SE', 'SI'},
 {'D0', 'D1', 'S0', 'SE', 'SI'}
]

'''
input: 


'''


def classify_ckt(mapped_pins):
    ckt_type = {} 
    
    Q = 'Q'   in mapped_pins
    QN = 'QN'  in mapped_pins
    
    CK = 'CK'  in mapped_pins
    CKN = 'CKN' in mapped_pins
    G = 'G'   in mapped_pins
    GN = 'GN'  in mapped_pins
    
    D = 'D'   in mapped_pins
    E = 'E'  in mapped_pins
    
    ECK = 'ECK' in mapped_pins
    FC = 'FC' in mapped_pins
    BC = 'BC' in mapped_pins
    
    SE = 'SE'  in mapped_pins
    SI = 'SI' in mapped_pins
    
    SN = 'SN' in mapped_pins
    RN = 'RN' in mapped_pins    
        
    D0 = 'D0' in mapped_pins    
    D1 = 'D1' in mapped_pins  
    S0 = 'S0' in mapped_pins  
  
    # mapped_pins = set(mapped_pins)
    # for t in ['G','GN','Q','QN','VDD','VSS','CK','CKN','RN','SN']:
    #     if t in mapped_pins:
    #         mapped_pins.remove(t)
        
    #classify
    if ECK and E:
        ckt_type['type'] = 'CG' #clock gate
        if not(SE) and not(FC) and not(BC):
            ckt_type['input_pins'] = ['E']
            ckt_type['input_type'] = (1,1)
        elif SE:
            ckt_type['input_pins'] = ['E','SE']
            ckt_type['input_type'] = (1,2)
        elif FC:
            ckt_type['input_pins'] = ['E','FC']
            ckt_type['input_type'] = (1,3)
        elif BC:
            ckt_type['input_pins'] = ['E','BC']
            ckt_type['input_type'] = (1,4)
        else:
         print(mapped_pins)
         raise ValueError('CLK error')           
    
    elif  (not(SE) and not(SI)):
        if (G or GN) and not(CK or CKN):
            ckt_type['type'] = 'LA' #Latch
            
            if D and not(E):
                ckt_type['input_pins'] = ['D']
                ckt_type['input_type'] = (2,1)
            elif D and E:
                ckt_type['input_pins'] = ['D','E']
                ckt_type['input_type'] = (2,2)
            else:
                print(mapped_pins)
                raise ValueError
            
            
        elif not(G or GN) and (CK or CKN):
            ckt_type['type'] = 'DF' #DFF
            if D0 and D1 and not(S0):
                ckt_type['input_pins'] = ['D0','D1']
                ckt_type['input_type'] = (3,3)
            elif D0 and D1 and S0:
                ckt_type['input_pins'] = ['D0','D1','S0']
                ckt_type['input_type'] = (3,4)
            elif D and not(E):
                ckt_type['input_pins'] = ['D']
                ckt_type['input_type'] = (3,1)
            elif D and E:
                ckt_type['input_pins'] = ['D','E']
                ckt_type['input_type'] = (3,2)
            else:
                print(mapped_pins)
                raise ValueError
            
        else:
            print(mapped_pins)
            raise ValueError
        
    elif SE and SI:
        ckt_type['type'] = 'SD' #Scan DFF
        if D0 and D1 and not(S0):
            ckt_type['input_pins'] = ['D0','D1']
            ckt_type['input_type'] = (4,3)
        elif D0 and D1 and S0:
            ckt_type['input_pins'] = ['D0','D1','S0']
            ckt_type['input_type'] = (4,4)
        elif D and not(E):
            ckt_type['input_pins'] = ['D']
            ckt_type['input_type'] = (4,1)
        elif D and E:
            ckt_type['input_pins'] = ['D','E']
            ckt_type['input_type'] = (4,2)
        else:
            print(mapped_pins)
            raise ValueError
    else:
        print(mapped_pins)
        raise ValueError('LA DF SD CLK error')
    #total 14
  
    #clk
    if  ckt_type['type']  == 'LA':
        if G:
            ckt_type['clk'] = 'G'
            ckt_type['postive'] = True
        elif GN:
            ckt_type['clk'] = 'GN'
            ckt_type['postive'] = False
        else:  
            raise  ValueError('No G GN in LA error') 
    else:
        if CK:
            ckt_type['clk'] = 'CK'
            ckt_type['postive'] = True
        elif CKN:
            ckt_type['clk'] = 'CKN'
            ckt_type['postive'] = False
        else:
            raise  ValueError('No G GN in LA error') 

    #out
    if Q and QN:
        ckt_type['output_pins'] = ['Q','QN']
    elif Q and not(QN):
        ckt_type['output_pins'] = ['Q']
    elif QN and not(Q):
        ckt_type['output_pins'] = ['QN']
    else:
        if ECK:                                                                          
            ckt_type['output_pins'] = ['ECK']
        else:
            print(mapped_pins)
            raise ValueError('Q, QN ECK error!')
  
    #SN RN
    if SN and RN:
        ckt_type['set'] = ['RN','SN']
    elif SN and not(RN):
        ckt_type['set'] = ['SN']
    elif RN and not(SN):
        ckt_type['set'] = ['RN']
    elif not(SN) and not(SN):
        ckt_type['set'] = []
    else:
        raise  ValueError('RN SN error')    
  

    
    #input pins
    ckt_type['scan'] = []
    
    if ckt_type['type'] == 'CG':
        ckt_type['input_pins'] = ['E']
        
        
        #TODO SE, PC, BC
    else:
        #input 
        if D and not(E):    
            ckt_type['input_pins'] = ['D']
        elif D and E:
            ckt_type['input_pins'] = ['D', 'E']
        elif D0 and D1 and not(S0):
            ckt_type['input_pins'] = ['D0', 'D1']
        elif D0 and D1 and S0:
            ckt_type['input_pins'] = ['D0', 'D1', 'S0']
        else:
            raise ValueError(mapped_pins)
        



    return ckt_type  


    
