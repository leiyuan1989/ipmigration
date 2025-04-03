from ipmigration.cell.apr.cir.patterns import PatternRouter
from ipmigration.cell.apr.cir.patterns import Patterns
track_num = 6


pt = Patterns()
pt.load_route_data(6)
pt.pattern_routing()

pr1 = pt.pattern_route_dict['FCROSS_1']    
pr2 = pt.pattern_route_dict['FCROSS_4']  
pr3 = pt.pattern_route_dict['FRSCROSS_1']  
pr4 = pt.pattern_route_dict['INV']  
g1 = pr2.graph[0][0]

pr2.graph[0][0].plot(pre_connect = True)
pr2.graph[1][0].plot(pre_connect = True)
# pr2.graph[2].plot(pre_connect = True)
# pr2.graph[3].plot(pre_connect = True)



# pr2.graph[0].plot()

# open axis 