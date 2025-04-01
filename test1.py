from ipmigration.cell.apr.cir.patterns import PatternRouter
from ipmigration.cell.apr.cir.patterns import Patterns
track_num = 6


pt = Patterns()
pt.load_route_data(6)
pt.pattern_routing()

pr1 = pt.pattern_route_dict['FCROSS_1']    
pr2 = pt.pattern_route_dict['FCROSS_4']  
pr3 = pt.pattern_route_dict['FRSCROSS_1']  