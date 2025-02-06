
"""
Created on Thu Mar 14 15:35:59 2024

@author: shunqidai
add schmittTriggerTran1Simulation
add simulation_schmitt_trigger 28/08/2024
modified generate_all_values: round width
add generate_hierarchy_simulationFun_dict: 
    two level dictionary based on mode and corners 29/08/2024

modified circuitOP1Simulation, simulation_opamp

modify generate_all_corner_simulationFun_dict 
add method __call__ in corner_simulatior
Dec 06, 2024
"""
#This is a linux Pyspice version
# cfg is a dummy variable in linux version
import numpy as np
import os
import time

from ipmigration.analog.opt.simulator import calculator
from ipmigration.analog.opt.simulator import spectre
from ipmigration.analog.opt.utils import figureplot
from ipmigration.analog.opt.utility import configuration

from ipmigration.analog.opt.utils.gui_parser import GuiParser
# from simulation_setup import circuit_simulator_path, \
#                              netlist_template_folder_dir,\
#                              defined_netlist_folder_dir, \
#                              model_card_path


###############define SPICE simulator##########################
r'''
#CFG = r'..\..\\ngspice-41_64\Spice64\bin\ngspice_con' #SPICE simulator path, not use in linux version
#CFG = r'ngspice' # linux version
'''
circuit_simulator_path = r'' # linux spectre version
# 



r"""
#CFG = {
#            'ngspice' : r'..\ngspice\Spice64\bin\ngspice_con', 
#            #'ngspice' : r'D:\01Work\02Sizing\ngspice\Spice64\bin\ngspice_con', 
#            } # SPICE simulator path
###############define SPICE simulator and working folder##########################
#CFG = r'..\ngspice\Spice64\bin\ngspice_con' #SPICE simulator path
#CFG =r'C:\Users\shunqidai\ngspice-41_64\Spice64\bin\ngspice_con'
#CFG = r'..\..\\ngspice-41_64\Spice64\bin\ngspice_con' #SPICE simulator path, not use in linux version
#CFG = r'ngspice' # linux version
#CFG = r'' # linux spectre version

# smic018 work folder
#undefinedNetlist_dir = r'./smic018/tb_template' #netlist template folder
#definedNetlist_dir = r'./smic018/simResult' #defined netlist folder

# smic011 work folder
#undefinedNetlist_dir = r'./smic011/tb_template' #netlist template folder
#definedNetlist_dir = r'./smic011/simResult' #defined netlist folder

######### model card ################
# smic018
#model_card_path=r"/home/shunqidai/Sizing/SizingDemoLinuxSpectre_integer_stdcell/smic018/models/spectre/ms018_v1p7_spe.lib"

# smic011
#model_card_path=r"/home/shunqidai/Sizing/SizingDemoLinuxSpectre_integer_stdcell/smic011/models/spectre/ms011_ms013s_io33_v1p24_spe.lib"
"""



###################SIMULATOR WORK FOLDER AND MODLE CARD SETUP###################
#define simulator
CFG=circuit_simulator_path
#define work folder
undefinedNetlist_dir=GuiParser.netlistFolder
definedNetlist_dir=GuiParser.optNetlistFolder
model_card_path=GuiParser.modelCardFile
corner_name_list=["tt", "ff", "ss", "fnsp", "snfp"]
model_cfg=[model_card_path, corner_name_list]

############## OPAMP SETUP ###############################################
#############setup ac1 config  AC Gain GBW PM#######################################
undefinedNetlist_file=r'/template_diffamp1_ac1.scs'
definedNetlist_file=r'/test_diffamp1_ac1.scs'
data_filename=r"outac1.ac"

simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
ac1_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
ac1_config.setup_cfg(simulation_cfg, model_cfg)

#############setup tran1 config   Slew Rate########################################
undefinedNetlist_file=r'/template_diffamp1_tran1.scs'
definedNetlist_file=r'/test_diffamp1_tran1.scs'
data_filename=r"outtran1.tran.tran"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
tran1_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
tran1_config.setup_cfg(simulation_cfg, model_cfg)

#############setup tran2 config  Negative Slew Rate############################################
undefinedNetlist_file=r'/template_diffamp1_tran2.scs'
definedNetlist_file=r'/test_diffamp1_tran2.scs'
data_filename=r"outtran2.tran.tran"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
tran2_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
tran2_config.setup_cfg(simulation_cfg, model_cfg)

#############setup ac2 config  CMRR#######################################
undefinedNetlist_file=r'/template_diffamp1_ac2.scs'
definedNetlist_file=r'/test_diffamp1_ac2.scs'
data_filename=r"outac2.ac"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
ac2_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
ac2_config.setup_cfg(simulation_cfg, model_cfg)

#############setup ac3 config  PSRR+#######################################
undefinedNetlist_file=r'/template_diffamp1_ac3.scs'
definedNetlist_file=r'/test_diffamp1_ac3.scs'
data_filename=r"outac3.ac"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
ac3_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
ac3_config.setup_cfg(simulation_cfg, model_cfg)

#############setup dc1 config  ICMR########################################
undefinedNetlist_file=r'/template_diffamp1_dc1.scs'
definedNetlist_file=r'/test_diffamp1_dc1.scs'
data_filename=r"outdc1.dc"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
dc1_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
dc1_config.setup_cfg(simulation_cfg, model_cfg)

#############setup dc2 config  OCMR Output Swing########################################
undefinedNetlist_file=r'/template_diffamp1_dc2.scs'
definedNetlist_file=r'/test_diffamp1_dc2.scs'
data_filename=r"outdc2.dc"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
dc2_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
dc2_config.setup_cfg(simulation_cfg, model_cfg)

#############setup op config  OP########################################
undefinedNetlist_file=r'/template_diffamp1_op1.scs'
definedNetlist_file=r'/test_diffamp1_op1.scs'
data_filename=r"outop1.dc"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]
op1_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
op1_config.setup_cfg(simulation_cfg, model_cfg)

DVDSAT=50 #[mV]
#------------------------------------------------------------------------
def circuitAC1Simulation(values, corner=None, output=0, config=ac1_config):
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    ac_data_filename = outputFilePath["data_filename"]
    ac_data_filename = os.path.splitext(ac_data_filename)[0]
    ac_data_file_path = outputFilePath["data_file_path"]
    
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    '''
    undefinedNetlistPath = {
            'undefinedNetlist_dir' : r'./smic018/tb_template',
            'undefinedNetlist_file' : r'/template_diffamp1_ac1.sp',
            } # undefined Netlist path
      
    definedNetlistPath = {
            'definedNetlist_dir' : r'./smic018/simResult',
            'definedNetlist_file' : r'/test_diffamp1_ac1.sp',
            } # defined Netlist path
    
# simulation output file path
    old_data_output_filename = r"old_data_output_filename"
    ac_data_filename = r"outac1.dat"
    ac_data_file_path = r'./smic018/simResult'+r'/'+ac_data_filename
'''
# make values be comparable to design rule:
    parameters_values = values
    # define outputfilename
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, ac_data_filename)
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    
    # define design variable value
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(ac_data_file_path)
# read the simulation output produced by the 'wrdata' command
    freq, vout = circuit.getACData(ac_data_file_path, [[1,2]])    
# calculate DC gain
    dcGain = calculator.dcGain(freq, vout)
# calculate DC gain in dB
    dcGain_dB = calculator.dcGain_dB(freq, vout)
# calculate unityGainFrequency
    ugf = calculator.unityGainFrequency(freq, vout)
# calculate 3dB-bandwidth
    bandwidth = calculator.bandwidth3dB(freq, vout)
# calculate phase margin
    phaseMargin = calculator.phaseMargin(freq, vout)
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)
    
    if output:
        print('dcgain: %.5E X' % dcGain)
        print('dcgain in dB: %.1f dB' % dcGain_dB)
        print('UnityGainFrequency: %.2e kHz' % float(ugf/1e3))
        print('3dB-bandwidth: %.2e kHz' % float(bandwidth/1e3))
        print('PhaseMargin: %.1f degree' % phaseMargin)
        print('parameters:', device_parameters) 
        print('parameters_values:', device_parameter_values) 
    return freq, vout, dcGain, ugf, bandwidth, phaseMargin


def circuitTran1Simulation(values, corner=None, output=0, config=tran1_config):   
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    tran_data_filename = outputFilePath["data_filename"]
    tran_cmd_name = tran_data_filename.split('.')[0]
    tran_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    
    '''
    undefinedNetlistPath = {
            'undefinedNetlist_dir' : r'.\smic018\test\template',
            'undefinedNetlist_file' : r'\template_diffamp1_tran1.sp',
            } # undefined Netlist path
      
    definedNetlistPath = {
            'definedNetlist_dir' : r'.\smic018\test',
            'definedNetlist_file' : r'\test_diffamp1_tran1.sp',
            } # defined Netlist path
    
# simulation output file path
    old_data_output_filename = r"old_data_output_filename"
    tran_data_filename = r"outtran1.dat"
    tran_data_file_path = r'.\smic018\test'+r'\\'+tran_data_filename
'''
# make values be comparable to design rule:
    parameters_values = values
        
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(tran_data_file_path)   
# read the simulation output produced by the 'wrdata' command
    time_var, vout_tran = circuit.getTranData(tran_data_file_path, portname="out", index_list=[1])

# calculate Slew Rate
    slewRate = calculator.slewRate(time_var, vout_tran)
    slewRate_us=slewRate/1e6

# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        print('slewRate: %.1f V/us' % slewRate_us)
        print('parameters:', device_parameters)
        print('parameters_values:', device_parameter_values) 
    return time_var, vout_tran, slewRate


def circuitTran2Simulation(values, corner=None, output=0, config=tran2_config):
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    tran_data_filename = outputFilePath["data_filename"]
    tran_cmd_name = tran_data_filename.split('.')[0]
    tran_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    '''
    undefinedNetlistPath = {
            'undefinedNetlist_dir' : r'.\smic018\test\template',
            'undefinedNetlist_file' : r'\template_diffamp1_tran2.sp',
            } # undefined Netlist path
      
    definedNetlistPath = {
            'definedNetlist_dir' : r'.\smic018\test',
            'definedNetlist_file' : r'\test_diffamp1_tran2.sp',
            } # defined Netlist path
    
# simulation output file path
    old_data_output_filename = r"old_data_output_filename"
    tran_data_filename = r"outtran2.dat"
    tran_data_file_path = r'.\smic018\test'+r'\\'+tran_data_filename
    '''
    
# make values be comparable to design rule:
    parameters_values = values
        
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(tran_data_file_path)
    
# read the simulation output produced by the 'wrdata' command
    time_var, vout_tran = circuit.getTranData(tran_data_file_path, portname="out", index_list=[1]) 

# calculate Slew Rate Negative
    slewRateNeg = calculator.slewRateNeg(time_var, vout_tran)
    slewRateNeg_us=slewRateNeg/1e6
    
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        print('slewRateNeg: %.1f V/us' % slewRateNeg_us)
        print('parameters:', device_parameters)
        print('parameters_values:', device_parameter_values) 
    return time_var, vout_tran, slewRateNeg


def circuitAC2Simulation(values, corner=None, output=0, config=ac2_config):    
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    ac_data_filename = outputFilePath["data_filename"]
    ac_data_filename = os.path.splitext(ac_data_filename)[0]
    ac_data_file_path = outputFilePath["data_file_path"]

    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
# make values be comparable to design rule:
    parameters_values = values 
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, ac_data_filename)
    
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(ac_data_file_path)
# read the simulation output produced by the 'wrdata' command
    freq, vout = circuit.getACData(ac_data_file_path, [[1,2]])    
# calculate CMRR 
    CMRR = calculator.CMRR(freq, vout)
# calculate CMRR_dB 
    CMRR_dB = 20*np.log10(CMRR)
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)
    
    if output:
        print('CMRR: %.5E X' % CMRR)
        print('CMRR in dB: %.1f dB' % CMRR_dB)
        print('parameters:', device_parameters) 
        print('parameters_values:', device_parameter_values) 
    return freq, vout, CMRR

def circuitAC3Simulation(values, corner=None, output=0, config=ac3_config):    
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    ac_data_filename = outputFilePath["data_filename"]
    ac_data_filename = os.path.splitext(ac_data_filename)[0]
    ac_data_file_path = outputFilePath["data_file_path"]

    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
# make values be comparable to design rule:
    parameters_values = values 
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, ac_data_filename)
    
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(ac_data_file_path)
# read the simulation output produced by the 'wrdata' command
    freq, vout = circuit.getACData(ac_data_file_path, [[1,2]])    
# calculate PSRR_pos 
    PSRR_pos = calculator.PSRR(freq, vout)
# calculate PSRR_pos_dB 
    PSRR_pos_dB = 20*np.log10(PSRR_pos)
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)
    
    if output:
        print('PSRR+: %.5E X' % PSRR_pos)
        print('PSRR+ in dB: %.1f dB' % PSRR_pos_dB)
        print('parameters:', device_parameters) 
        print('parameters_values:', device_parameter_values) 
    return freq, vout, PSRR_pos


def circuitDC1Simulation(values, corner=None, output=0, config=dc1_config):    
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    dc_data_filename = outputFilePath["data_filename"]
    dc_data_filename = os.path.splitext(dc_data_filename)[0]
    dc_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
# make values be comparable to design rule:
    parameters_values = values 
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, dc_data_filename)
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(dc_data_file_path)
# read the simulation output produced by the 'wrdata' command
    dc_sweep, vout_dc = circuit.getDCData(dc_data_file_path, [1])    
# calculate ICMR 
    ICMR = calculator.ICMR(dc_sweep, vout_dc)
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)
    
    if output:
        print('ICMR: %.3f V' % ICMR)
        print('parameters:', device_parameters) 
        print('parameters_values:', device_parameter_values) 
    return dc_sweep, vout_dc, ICMR

def circuitDC2Simulation(values, corner=None, output=0, config=dc2_config):    
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    dc_data_filename = outputFilePath["data_filename"]
    dc_data_filename = os.path.splitext(dc_data_filename)[0]
    dc_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
# make values be comparable to design rule:
    parameters_values = values 
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, dc_data_filename)
    
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(dc_data_file_path)
# read the simulation output produced by the 'wrdata' command
    dc_sweep, vout_dc = circuit.getDCData(dc_data_file_path, [1])    
# calculate OCMR 
    OCMR = calculator.OCMR(dc_sweep, vout_dc)
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)
    
    if output:
        print('Outout Swing: %.3f V' % OCMR)
        print('parameters:', device_parameters) 
        print('parameters_values:', device_parameter_values) 
    return dc_sweep, vout_dc, OCMR

def circuitOP1Simulation(values, corner=None, output=0, config=op1_config):    
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    op_data_filename = outputFilePath["data_filename"]
    op_data_filename = os.path.splitext(op_data_filename)[0]
    op_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
# make values be comparable to design rule:
    parameters_values = values 
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, op_data_filename)
    
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(op_data_file_path)
# read the simulation output produced by the 'wrdata' command
    #print("extract vdsat")
    device_name_list, dvdsat_list = circuit.getOpData(op_data_file_path) 
    
# calculate vdsat convert to mV
    dvdsat_list = [float(round(abs(float(item))*1000)) for item in dvdsat_list]
# calculate num_saturation_device
    num_saturation_device=sum(np.array(dvdsat_list)>DVDSAT)
# get device_parameters  
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values) 
    #print("dvdsat_list:", dvdsat_list) 
    #print("num_saturation_device:", num_saturation_device) 
    if output:
        print('{0} devices dvdsat list: {1}'.format(len(dvdsat_list), dvdsat_list))
        print('parameters:', device_parameters) 
        print('parameters_values:', device_parameter_values) 
        print("device_name_list:", device_name_list)
        print("dvdsat_list:", dvdsat_list) 
    return num_saturation_device

#####################################################################################
def simulation_opamp(decision_variable_values, boundary, targets, mode="all", output=0, plot=0, corner=None):
    # mode: select cheep simulation or expensive simulation
    # return sim result unit:
    # [DC Gain, GBW , Phase Margin, Positive Slewrate, slewRate]
    # [dB, MHz, deg, MV/s]
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    component_num = len(bounds["components"])
    #decision_variable_values = convertUnit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = matchDR([values], bounds)
    #print("values:", values)
    
    if mode=='op':
        dvdsat_list = circuitOP1Simulation(values, corner=corner, output=output)
        op_sim_result = dvdsat_list
        if output>0:
            print("Op simulation! \n design variables:{0} \n vdsat_list: {1} \n".format(values, op_sim_result))
        return op_sim_result
    
    if mode=='cheap': 
        cheap_sim_result = list(np.zeros(len(targets['cheap'])))
        # try:
        freq, vout, dcGain, ugf, bandwidth, phaseMargin = circuitAC1Simulation(values, corner=corner, output=output)
        freq_cmrr, vout_cmrr, cmrr = circuitAC2Simulation(values, corner=corner, output=output)
        freq_psrr_pos, vout_psrr_pos, psrr_pos = circuitAC3Simulation(values, corner=corner, output=output)
        dc_sweep_ocmr, vout_dc_ocmr, ocmr = circuitDC2Simulation(values, corner=corner, output=output)
        cheap_sim_result = [dcGain, ugf/1.0e6, phaseMargin, cmrr, psrr_pos, ocmr]
        cheap_sim_result = [float('{:.1f}'.format(i)) for i in cheap_sim_result]
        if output>0:
            print("Cheap simulation! \n design variables:{0} \n [DC Gain, GBW, Phase Margin, CMRR, PSRR, Output Swing]: {1} \n".format(values, cheap_sim_result))
        if plot>0:
            #import figureplot
            figureplot.plotFrequencyResponse(freq, vout)
            figureplot.plotCMRRorPSRR(freq_cmrr, vout_cmrr, title='CMRR')
            figureplot.plotDC(dc_sweep_ocmr, vout_dc_ocmr, title='OCMR')
        return cheap_sim_result
        # except:
        #     print("Cheap simulation error!")
        #     return cheap_sim_result
        
    elif mode=='expensive': 
        expensive_sim_result = list(np.zeros(len(targets['expensive'])))
        # try:
        time_var, vout_tran, slewRate = circuitTran1Simulation(values, corner=corner, output=output)
        time_var1, vout_tran1, slewRateNeg = circuitTran2Simulation(values, corner=corner, output=output)
        expensive_sim_result = [slewRate/1.0e6, slewRateNeg/1.0e6]
        expensive_sim_result = [float('{:.1f}'.format(i)) for i in expensive_sim_result]
        if output>0:
            print("Expensive simulation! \ndesign variables:{0} \n [Positive Slewrate, Negative slewRate]: {1} \n".format(values, expensive_sim_result))
        if plot>0:
            #import figureplot
            figureplot.plotTran(time_var, vout_tran)
            figureplot.plotTran(time_var1, vout_tran1)
        return expensive_sim_result
        # except:
        #     print("Expensive simulation error!")
        #     return expensive_sim_result
    
    elif mode=='all':
        sim_result = list(np.zeros(len(targets['expensive'])+len(targets['cheap'])))
        # try:
        #print("Do OP1 Simulation")
        #num_saturation_device = circuitOP1Simulation(values, corner=corner, output=output)
        #print("dvdsat list:", dvdsat_list)
        #print("Do AC1 Simulation")
        freq, vout, dcGain, ugf, bandwidth, phaseMargin = circuitAC1Simulation(values, corner=corner, output=output)
        #print("Do Trans1 Simulation")
        time_var, vout_tran, slewRate = circuitTran1Simulation(values, corner=corner, output=output)
        #print("Do Trans2 Simulation")
        time_var1, vout_tran1, slewRateNeg = circuitTran2Simulation(values, corner=corner, output=output)
        #print("Do AC2 Simulation")
        freq_cmrr, vout_cmrr, cmrr = circuitAC2Simulation(values, corner=corner, output=output)
        #print("Do AC3 Simulation")
        freq_psrr_pos, vout_psrr_pos, psrr_pos = circuitAC3Simulation(values, corner=corner, output=output)
        #print("Do DC2 Simulation")
        dc_sweep_ocmr, vout_dc_ocmr, ocmr = circuitDC2Simulation(values, corner=corner, output=output)
        
        #op_sim_result=[num_saturation_device]
        op_sim_result=[]
        
        cheap_sim_result = [dcGain, ugf/1.0e6, phaseMargin, cmrr, psrr_pos, ocmr]
        cheap_sim_result = [float('{:.1f}'.format(i)) for i in cheap_sim_result]
        expensive_sim_result = [slewRate/1.0e6, slewRateNeg/1.0e6]
        expensive_sim_result = [float('{:.1f}'.format(i)) for i in expensive_sim_result]
        sim_result = op_sim_result + cheap_sim_result + expensive_sim_result
        if plot>0:
            #import figureplot
            time.sleep(1)
            figureplot.plotFrequencyResponse(freq, vout)
            figureplot.plotTran(time_var, vout_tran)
            figureplot.plotTran(time_var1, vout_tran1)
            figureplot.plotCMRRorPSRR(freq_cmrr, vout_cmrr, title='CMRR')
            figureplot.plotDC(dc_sweep_ocmr, vout_dc_ocmr, title='OCMR')
        if output>0:
            print("Total simulation \n design variables:{0} \n [num_saturation_device, DC Gain, GBW, Phase Margin, CMRR, PSRR, Output Swing, Positive Slewrate, Negative Slewrate]: {1} \n".format(values, sim_result))
        return sim_result
        # except:
        #     print("Total simulation error!")
        #     return sim_result

#############################FOR SCHMITT TRIGGER##################
################## Schmitt Trigger Setup#########################
#############setup tran1 config  Schmitt Trigger Tran######################################
undefinedNetlist_file=r'/template_st1_tran1.scs'
definedNetlist_file=r'/test_st1_tran1.scs'
data_filename=r"outtran1.tran.tran"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]


schmitt_trigger_tran1_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
schmitt_trigger_tran1_config.setup_cfg(simulation_cfg, model_cfg)

#------------------------------------------------------------------------
def schmittTriggerTran1Simulation(values, corner=None, output=0, config=schmitt_trigger_tran1_config):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: time_var_out, vout_tran, time_var_in, vin_tran, v_ih, v_il, window
    #print(config.modelCardParth)
    """
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    tran_data_filename = outputFilePath["data_filename"]
    tran_cmd_name = tran_data_filename.split('.')[0]
    tran_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    #print("cornerNameList:", cornerNameList)
    #print("corner_name in ST trans:", corner_name)
    '''
    undefinedNetlistPath = {
            'undefinedNetlist_dir' : r'.\smic018\test\template',
            'undefinedNetlist_file' : r'\template_diffamp1_tran1.sp',
            } # undefined Netlist path
      
    definedNetlistPath = {
            'definedNetlist_dir' : r'.\smic018\test',
            'definedNetlist_file' : r'\test_diffamp1_tran1.sp',
            } # defined Netlist path
    
# simulation output file path
    old_data_output_filename = r"old_data_output_filename"
    tran_data_filename = r"outtran1.dat"
    tran_data_file_path = r'.\smic018\test'+r'\\'+tran_data_filename
'''
# make values be comparable to design rule:
    parameters_values = values
        
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(tran_data_file_path)   
# read the simulation output produced by the 'wrdata' command
    time_var_out, vout_tran = circuit.getTranData(tran_data_file_path, portname="out", index_list=[1]) 
    time_var_in, vin_tran = circuit.getTranData(tran_data_file_path, portname="in", index_list=[1]) 
# calculate SchmittTriggerResult
    v_ih, v_il, window = calculator.SchmittTriggerResult(time_var_in, vin_tran, time_var_out, vout_tran )

# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        print('v_ih: {0:.3f}V, v_il:{1:.3f}V, window: {2:.1f}mV'.format(v_ih, v_il, window))
        print('parameters:', device_parameters)
        print('parameters_values:', device_parameter_values) 
    return time_var_out, vout_tran, time_var_in, vin_tran, v_ih, v_il, window

#############################################################################
def simulation_schmitt_trigger(decision_variable_values, boundary, targets, mode="all", output=0, plot=0, corner=None):
    """
    # return: sim result
    #unit:
    # [vih, vil, hysterisis_window]
    # [V, V, mV]
    """
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    component_num = len(bounds["components"])
    #decision_variable_values = convertUnit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = matchDR([values], bounds)
     
    sim_result = list(np.zeros(len(targets['all targets value'])))
    # try:
    time_var_out, vout_tran, time_var_in, vin_tran,\
    vih, vil, window = schmittTriggerTran1Simulation(values, corner=corner, output=output)
    sim_result = [vih, vil, window]
    sim_result = [float('{:.2f}'.format(i)) for i in sim_result]
    if output>0:
        print("Schmitt Trigger simulation! \n design variables:{0} \n [vih, vil, hysterisis_window]: {1} \n".format(values, sim_result))
    if plot>0:
        figureplot.plotSchmittTrigger(time_var_in, vin_tran, time_var_out, vout_tran)
    return sim_result
    # except:
        # print("Simulation error!")
        # return sim_result

################################For Level Shifter######################
################## Level Shifter Setup#########################
#############setup tran1 config  Level Shifter Tran######################################
undefinedNetlist_file=r'/template_ls1_tran1.scs'
definedNetlist_file=r'/test_ls1_tran1.scs'
data_filename=r"outtran1.tran.tran"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]

level_shifter_tran1_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
level_shifter_tran1_config.setup_cfg(simulation_cfg, model_cfg)
#------------------------------------------------------------------------
def levelShifterTran1Simulation(values, corner=None, output=0, config=level_shifter_tran1_config):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: time_var_out, vout_tran, time_var_in, vin_tran, v_ih, v_il, window
    #print(config.modelCardParth)
    """
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    tran_data_filename = outputFilePath["data_filename"]
    tran_cmd_name = tran_data_filename.split('.')[0]
    tran_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    #print("cornerNameList:", cornerNameList)
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    #print("cornerNameList:", cornerNameList)
    #print("corner in level shifter trans:", corner)
    #print("corner_name in level shifter trans:", corner_name)

# make values be comparable to design rule:
    parameters_values = values
        
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(tran_data_file_path)   
# read the simulation output produced by the 'wrdata' command
    time_var_out, vout_tran = circuit.getTranData(tran_data_file_path, portname="out", index_list=[1]) 
    time_var_in, vin_tran = circuit.getTranData(tran_data_file_path, portname="in", index_list=[1]) 
    time_var, ivddh_tran = circuit.getTranData(tran_data_file_path, portname="vddh:p", index_list=[1]) 
    time_var, ivddl_tran = circuit.getTranData(tran_data_file_path, portname="vddl:p", index_list=[1]) 
# calculate LevelShifterResult
    rise_time, fall_time, delay, avg_total_power = calculator.LevelShifterResult(time_var_in, vin_tran, time_var_out, vout_tran, ivddl_tran, ivddh_tran )

# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        print('rise_time: {0:.2e}s, fall_time:{1:.2e}s, delay: {2:.2e}s, avg_total_power: {3:.2e}W'.format(rise_time, fall_time, delay, avg_total_power))
        print('parameters:', device_parameters)
        print('parameters_values:', device_parameter_values) 
    return time_var_out, vout_tran, time_var_in, vin_tran,  ivddl_tran, ivddh_tran, rise_time, fall_time, delay, avg_total_power

#----------------------------------------------------------------------------#
def simulation_level_shifter(decision_variable_values, boundary, targets, mode="all", output=0, plot=0, corner=None):
    """
    # return: sim result
    #unit:
    # [rise_time, fall_time, delay, avg_total_power]
    # [sec, sec, sec, W]
    """
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    component_num = len(bounds["components"])
    #decision_variable_values = convertUnit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = matchDR([values], bounds)
     
    sim_result = list(np.zeros(len(targets['all targets value'])))
    # try:
    time_var_out, vout_tran, time_var_in, vin_tran,\
    ivddl_tran, ivddh_tran,\
    rise_time, fall_time, delay, avg_total_power = levelShifterTran1Simulation(values, corner=corner, output=output)
    sim_result = [rise_time, fall_time, delay, avg_total_power]
    sim_result = [float('{:.2e}'.format(i)) for i in sim_result]
    if output>0:
        print("Level Shifter simulation! \n design variables:{0} \n [rise_time, fall_time, delay, avg_total_power]: {1} \n".format(values, sim_result))
    if plot>0:
        figureplot.plotSchmittTrigger(time_var_in, vin_tran, time_var_out, vout_tran)
    return sim_result
    # except:
        # print("Simulation error!")
        # return sim_result


################################For Dynamic Comparator######################
################## Dynamic Comparator Setup#########################
#############setup tran1 config Dynamic Comparator voltage offset######################################
undefinedNetlist_file=r'/template_comparator1_tran1.scs'
definedNetlist_file=r'/test_comparator1_tran1.scs'
data_filename=r"outtran1.tran.tran"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]

dynamic_comparator_tran1_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
dynamic_comparator_tran1_config.setup_cfg(simulation_cfg, model_cfg)
#------------------------------------------------------------------------
#############setup tran2 config  Comparator Delay######################################
undefinedNetlist_file=r'/template_comparator1_tran2.scs'
definedNetlist_file=r'/test_comparator1_tran2.scs'
data_filename=r"outtran2.tran.tran"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]

dynamic_comparator_tran2_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
dynamic_comparator_tran2_config.setup_cfg(simulation_cfg, model_cfg)
#------------------------------------------------------------------------
def dynamicComparatorTran1Simulation(values, corner=None, output=0, config=dynamic_comparator_tran1_config):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: vos(offset voltage) [mV]
    #print(config.modelCardParth)
    """
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    tran_data_filename = outputFilePath["data_filename"]
    tran_cmd_name = tran_data_filename.split('.')[0]
    tran_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    #print("cornerNameList:", cornerNameList)
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    #print("cornerNameList:", cornerNameList)
    #print("corner in level shifter trans:", corner)
    #print("corner_name in level shifter trans:", corner_name)

# make values be comparable to design rule:
    parameters_values = values
        
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(tran_data_file_path)   
# read the simulation output produced by the 'wrdata' command
    time_var_outn, voutn_tran = circuit.getTranData(tran_data_file_path, portname="outn", index_list=[1]) 
    time_var_inn, vinn_tran = circuit.getTranData(tran_data_file_path, portname="inn", index_list=[1]) 
    time_var_outp, voutp_tran = circuit.getTranData(tran_data_file_path, portname="outp", index_list=[1]) 
    time_var_inp, vinp_tran = circuit.getTranData(tran_data_file_path, portname="inp", index_list=[1]) 
    time_var_clk, vclk_tran= circuit.getTranData(tran_data_file_path, portname="clk", index_list=[1]) 
    time_var_vdd, vdd_tran= circuit.getTranData(tran_data_file_path, portname="dd", index_list=[1]) 
# calculate comparator offsetvoltage
    vos = calculator.ComparatorOffset(time_var_inp, vinp_tran, \
                                      time_var_inn, vinn_tran, \
                                      time_var_outp, voutp_tran, \
                                      time_var_vdd, vdd_tran)
# calculate comparator 2 output rise time and fall time
    vop_rise_time, vop_fall_time=calculator.RisetimeFalltime(time_var_outp, voutp_tran, time_var_vdd, vdd_tran)
    von_rise_time, von_fall_time=calculator.RisetimeFalltime(time_var_outn, voutn_tran, time_var_vdd, vdd_tran)
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        print('offset_voltage vos: {0:.3e} mV,\
              vop_rise_time: {1:.3e} ns, vop_fall_time: {2:.3e} ns,  \
              von_rise_time: {3:.3e} ns, von_fall_time: {4:.3e} ns'.format(vos, vop_rise_time, vop_fall_time, \
                  von_rise_time, von_fall_time))
        print('parameters:', device_parameters)
        print('parameters_values:', device_parameter_values) 
    return time_var_clk, vclk_tran, time_var_inp, vinp_tran, \
            time_var_inn, vinn_tran, time_var_outp, voutp_tran, \
           time_var_outn, voutn_tran, \
           vos, vop_rise_time, vop_fall_time, von_rise_time, von_fall_time

#------------------------------------------------------------------------
def dynamicComparatorTran2Simulation(values, corner=None, output=0, config=dynamic_comparator_tran2_config):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: delay
    #print(config.modelCardParth)
    """
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    tran_data_filename = outputFilePath["data_filename"]
    tran_cmd_name = tran_data_filename.split('.')[0]
    tran_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    #print("cornerNameList:", cornerNameList)
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    #print("cornerNameList:", cornerNameList)
    #print("corner in level shifter trans:", corner)
    #print("corner_name in level shifter trans:", corner_name)

# make values be comparable to design rule:
    parameters_values = values
        
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(tran_data_file_path)   
# read the simulation output produced by the 'wrdata' command
    time_var_outp, voutp_tran = circuit.getTranData(tran_data_file_path, portname="outp", index_list=[1]) 
    time_var_clk, vclk_tran = circuit.getTranData(tran_data_file_path, portname="clk", index_list=[1]) 
    time_var_vdd, vdd_tran= circuit.getTranData(tran_data_file_path, portname="dd", index_list=[1]) 
# calculate comparator offsetvoltage
    delay_rise, delay_fall = calculator.ComparatorDelay(time_var_clk, vclk_tran, time_var_outp, voutp_tran, time_var_vdd, vdd_tran)

# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        print('delay_rise: {0:.3e} nsec, delay_fall: {1:.3e}'.format(delay_rise, delay_fall))
        print('parameters:', device_parameters)
        print('parameters_values:', device_parameter_values) 
    return time_var_clk, vclk_tran, time_var_outp, voutp_tran, delay_rise, delay_fall


def simulation_dynamic_comparator(decision_variable_values, boundary, targets, mode="all", output=0, plot=0, corner=None):
    """
    # return: sim result
    #unit:
    # [vos, vop_rise_time, vop_fall_time, von_rise_time, von_fall_time, delay_rise, delay_fall]
    # [mV, nsec, nsec, nsec, nsec, nsec, nsec]
    """
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    component_num = len(bounds["components"])
    #decision_variable_values = convertUnit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = matchDR([values], bounds)
     
    sim_result = list(np.zeros(len(targets['all targets value'])))
    # try:
    time_var_clk1, vclk_tran1, \
    time_var_inp1, vinp_tran1, time_var_inn1,\
    vinn_tran1, time_var_outp1, voutp_tran1, \
    time_var_outn1, voutn_tran1, \
    vos, vop_rise_time, vop_fall_time, \
    von_rise_time, von_fall_time = dynamicComparatorTran1Simulation(values, corner=corner, output=output)
    
    time_var_clk2, vclk_tran2, time_var_outp2,\
        voutp_tran2, delay_rise, delay_fall = dynamicComparatorTran2Simulation(values, corner=corner, output=output)
    sim_result = [vos, vop_rise_time, vop_fall_time, \
                  von_rise_time, von_fall_time, delay_rise, delay_fall]
    sim_result = [float('{:.3e}'.format(i)) for i in sim_result]
    if output>0:
        print("Comparator simulation! \n design variables:{0} \n [vos, delay_rise, delay_fall]: {1} \n".format(values, sim_result))
    if plot>0:
        figureplot.plotDynamicComparatorOffset(time_var_clk1, vclk_tran1, \
                                        time_var_inp1, vinp_tran1, time_var_inn1,\
                                        vinn_tran1, time_var_outp1, voutp_tran1, \
                                        time_var_outn1, voutn_tran1)
        figureplot.plotClockDelay(time_var_clk2, vclk_tran2, \
                                  time_var_outp2,voutp_tran2)
    return sim_result
    # except:
        # print("Simulation error!")
        # return sim_result



################################For Continous Comparator######################
##################  Comparator Setup#########################
#############setup tran1 config Dynamic Comparator voltage offset######################################
undefinedNetlist_file=r'/template_comparator2_tran1.scs'
definedNetlist_file=r'/test_comparator2_tran1.scs'
data_filename=r"outtran1.tran.tran"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]

comparator_tran1_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
comparator_tran1_config.setup_cfg(simulation_cfg, model_cfg)
#------------------------------------------------------------------------
#############setup tran2 config  Comparator Delay######################################
undefinedNetlist_file=r'/template_comparator2_tran2.scs'
definedNetlist_file=r'/test_comparator2_tran2.scs'
data_filename=r"outtran2.tran.tran"
simulation_cfg=[undefinedNetlist_file, definedNetlist_file, data_filename]

comparator_tran2_config=configuration(CFG, undefinedNetlist_dir, definedNetlist_dir)
comparator_tran2_config.setup_cfg(simulation_cfg, model_cfg)
#------------------------------------------------------------------------
def comparatorTran1Simulation(values, corner=None, output=0, config=comparator_tran1_config):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: vos(offset voltage) [mV]
    #print(config.modelCardParth)
    """
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    tran_data_filename = outputFilePath["data_filename"]
    tran_cmd_name = tran_data_filename.split('.')[0]
    tran_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    #print("cornerNameList:", cornerNameList)
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    #print("cornerNameList:", cornerNameList)
    #print("corner in level shifter trans:", corner)
    #print("corner_name in level shifter trans:", corner_name)

# make values be comparable to design rule:
    parameters_values = values
        
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(tran_data_file_path)   
# read the simulation output produced by the 'wrdata' command
    time_var_inn, vinn_tran = circuit.getTranData(tran_data_file_path, portname="inn", index_list=[1]) 
    time_var_out, vout_tran = circuit.getTranData(tran_data_file_path, portname="out", index_list=[1]) 
    time_var_inp, vinp_tran = circuit.getTranData(tran_data_file_path, portname="inp", index_list=[1]) 
    time_var_vdd, vdd_tran= circuit.getTranData(tran_data_file_path, portname="dd", index_list=[1]) 
# calculate comparator offsetvoltage
    vos = calculator.ComparatorOffset(time_var_inp, vinp_tran, \
                                      time_var_inn, vinn_tran, \
                                      time_var_out, vout_tran,\
                                      time_var_vdd, vdd_tran)
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        print('offset_voltage vos: {0:.3e} mV'.format(vos))
        print('parameters:', device_parameters)
        print('parameters_values:', device_parameter_values) 
    return  time_var_inp, vinp_tran, \
            time_var_inn, vinn_tran, time_var_out, vout_tran, \
           vos


#------------------------------------------------------------------------
def comparatorTran2Simulation(values, corner=None, output=0, config=comparator_tran2_config):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: delay, voh, vol, ipwr_avg
    #         nsec, V,     V,  uA
    #print(config.modelCardParth)
    """
    cfg = config.cfg
    undefinedNetlistPath = config.undefinedNetlistPath
    definedNetlistPath = config.definedNetlistPath
    outputFilePath = config.outputFilePath
    old_data_output_filename = outputFilePath["old_data_output_filename"]
    tran_data_filename = outputFilePath["data_filename"]
    tran_cmd_name = tran_data_filename.split('.')[0]
    tran_data_file_path = outputFilePath["data_file_path"]
    
    modelCardParth = config.modelCardParth
    cornerNameList = config.cornerNameList
    dummy_model_card_path = modelCardParth["dummy_model_card_path"]
    model_card_path = modelCardParth["model_card_path"]
    dummy_corner_name = cornerNameList["dummy_corner_name"]
    
    #print("cornerNameList:", cornerNameList)
    if not corner:
        corner="tt"
    corner_name = cornerNameList[corner]
    #print("cornerNameList:", cornerNameList)
    #print("corner in level shifter trans:", corner)
    #print("corner_name in level shifter trans:", corner_name)

# make values be comparable to design rule:
    parameters_values = values
        
    circuit=ngl2.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_ngspice(tran_data_file_path)   
# read the simulation output produced by the 'wrdata' command
    time_var_out, vout_tran = circuit.getTranData(tran_data_file_path, portname="out", index_list=[1]) 
    time_var_inp, vinp_tran = circuit.getTranData(tran_data_file_path, portname="inp", index_list=[1]) 
    time_var_vdd, vdd_tran= circuit.getTranData(tran_data_file_path, portname="dd", index_list=[1]) 
    time_var_ivdd, ivdd_tran = circuit.getTranData(tran_data_file_path, portname="vdd:p", index_list=[1]) 
# calculate comparator delay 
    delay_rise, delay_fall = calculator.ComparatorDelay(time_var_inp, vinp_tran, time_var_out, vout_tran, time_var_vdd, vdd_tran)
# calculate comparator voh vol
    voh, vol = calculator.VOHandVOL(time_var_out, vout_tran)
# calculate comparator static power consumption
    ipwr_avg=calculator.PowerAverage(time_var_ivdd, ivdd_tran)
    ipwr_avg=ipwr_avg*1e6 # A-->uA
# get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        print('delay_rise: {0:.3e} nsec, delay_fall: {1:.3e} nsec, voh: {2:.2f} V, vol: {3:.2f} V, ipwr_avg: {4:.3e} uA'.format(delay_rise, delay_fall, voh, vol, ipwr_avg))
        print('parameters:', device_parameters)
        print('parameters_values:', device_parameter_values) 
        figureplot.plotTranPower(time_var_ivdd, ivdd_tran)
    return time_var_inp, vinp_tran, time_var_out, vout_tran, delay_rise, delay_fall, voh, vol, ipwr_avg


def simulation_comparator(decision_variable_values, boundary, targets, mode="all", output=0, plot=0, corner=None):
    """
    # return: sim result
    #unit:
    # [vos, delay_rise, delay_fall, voh, vol, ipwr_avg]
    # [mV, nsec, V, V, uA]
    """
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    component_num = len(bounds["components"])
    #decision_variable_values = convertUnit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = matchDR([values], bounds)
     
    sim_result = list(np.zeros(len(targets['all targets value'])))
    # try:
    time_var_inp1, vinp_tran1, time_var_inn1,\
    vinn_tran1, time_var_out1, vout_tran1, \
    vos = comparatorTran1Simulation(values, corner=corner, output=output)
    
    time_var_inp2, vinp_tran2,\
    time_var_out2, vout_tran2,\
    delay_rise, delay_fall, voh, vol, ipwr_avg = comparatorTran2Simulation(values, corner=corner, output=output)
    sim_result = [vos, delay_rise, delay_fall, voh, vol, ipwr_avg]
    sim_result = [float('{:.3e}'.format(i)) for i in sim_result]
    if output>0:
        print("Comparator simulation! \n design variables:{0} \n [vos, delay_rise, delay_fall, voh, vol, ipwr_avg]: {1} \n".format(values, sim_result))
    if plot>0:
        figureplot.plotComparatorOffset(time_var_inp1, vinp_tran1, time_var_inn1,\
                                        vinn_tran1, time_var_out1, vout_tran1)
        figureplot.plotClockDelay(time_var_inp2, vinp_tran2, \
                                  time_var_out2,vout_tran2)
    return sim_result
    # except:
    #     print("Simulation error!")
    #     return sim_result


############################### For W L covertion ################
##################################################################

def convertUnit(values, bounds):
    #values:np.array, tmp: np.array
    #print("convertUnit")
    component_num=len(bounds["components"])
    capacitance_num=len(bounds["capacitance"])
    inductance_num=len(bounds["inductance"])
    resistance_num=len(bounds["resistance"])
    current_source_num=len(bounds["current_source"])
    voltage_source_num=len(bounds["voltage_source"])
    index1 = capacitance_num
    index2 = index1+inductance_num
    index3 = index2+resistance_num
    index4 = index3+current_source_num
    index5 = index4+voltage_source_num
    
    tmp1=[]
    if index1>0:
        tmp1.extend(values[0:index1]*1.0e-12) #pF-->F
    if index2>index1:
        tmp1.extend(values[index1:index2]*1.0e-9) #nH-->H
    if index3>index2:
        tmp1.extend(values[index2:index3]*1.0e3) #kohm-->ohm
    if index4>index3:
        tmp1.extend(values[index3:index4]*1.0e-6) #uA-->A
    if index5>index4:
        tmp1.extend(values[index4:index5]*1.0) #V-->V
    tmp1=np.array(tmp1)
    tmp2=values[component_num:]
    #print("tmp1:", tmp1)
    #print("tmp2:", tmp2)
    tmp=np.concatenate((tmp1,tmp2))
    #print("convertUnit:", tmp)
    return tmp


def matchDR(values_list, bounds):
    # values_list:list, tmp_list:list
    #print("matchDR")
    component_num=len(bounds["components"])
    tmp_list=[]
    for values in values_list:
        tmp = [float('{:.3e}'.format(i)) for i in values[:component_num] ] \
            + [float('{:.2f}'.format(i)) for i in values[component_num:]]
        tmp_list.append(tmp)     
    #print("tmp_list:", tmp_list)
    return tmp_list


def generate_all_values(decision_variable_values, boundary):
    # generate all values based on variables and constants relationship
    bounds=boundary.bounds
    component_num=len(bounds["components"])    
    
    lower = np.array(boundary.get_variables_lower())
    upper = np.array(boundary.get_variables_upper())
    step = np.array(boundary.get_variables_step()) 
    # denormalize decision_variable_values
    #print("decision_variable_values:", decision_variable_values)
    decision_variable_values=lower+(decision_variable_values*step)
    for i in range(len(decision_variable_values)):
        if decision_variable_values[i]>upper[i]:
            decision_variable_values[i]=upper[i]
        elif decision_variable_values[i]<lower[i]:
            decision_variable_values[i]=lower[i]
    #print("denormalized_decision_variable_values:", decision_variable_values)
    #convert unit
    decision_variable_values = convertUnit(decision_variable_values, bounds)
    #print("decision_variable_values_after_unit_convertion:", decision_variable_values)
    
    # generate all values
    component_values=decision_variable_values[:component_num]
    # generate width values:
    # if width>=10um, it will be rounded.
    # if 1um<=width<10um, it will be .1f
    # if width<1um, it will be .2f
    width = bounds['constants']*decision_variable_values[component_num:]
    width_tmp =list(width)
    #print(width_tmp)
    """
    for idx in range(len(width_tmp)):
        item=width_tmp[idx]
        if item>=10.0:
            item=round(item)
        elif (item<10.0) and (item>=1.0):
            item=round(item*10.0)/10.0
        else:
            item=round(item*100.0)/100.0
        width_tmp[idx]=item
    #print(width_tmp)
    """
    width = [float('{:.3f}'.format(i)) for i in width_tmp]
    #print(width)
    #generate length
    length = bounds['constants']
    
    all_circuit_design_parameter_values = []
    all_circuit_design_parameter_values.extend(component_values)
    all_circuit_design_parameter_values.extend(length)
    all_circuit_design_parameter_values.extend(width)
    return all_circuit_design_parameter_values


def generate_simulationFun_dict(boundary, targets, simulation, corner="tt"):
    '''
    for Opamp simulation
    generate a simulation function dict for cheap, expensive and OP
    ##################################################
    return: dict: {"cheap": cheap_simulationFun,\
                     "expensive": expensive_simulationFun,\
                     "op": op_simulationFun}
    '''
    all_simulationFun = lambda x: simulation(x, boundary, targets, mode='all', output=0, corner=corner)
    cheap_simulationFun = lambda x: simulation(x, boundary, targets, mode='cheap', output=0, corner=corner)
    expensive_simulationFun = lambda x: simulation(x, boundary, targets, mode='expensive', output=0, corner=corner)
    op_simulationFun = lambda x: simulation(x, boundary, targets, mode='op', output=0)
    simulationFun_dict = {"cheap": cheap_simulationFun,\
                     "expensive": expensive_simulationFun,\
                     "op": op_simulationFun,\
                     "all": all_simulationFun}
    return simulationFun_dict


def generate_all_corner_simulationFun_dict(boundary, targets, simulation, corner_list=None, mode="all"):
    '''
    generate a corner_simulatior dict for all corners
    corner_simulatior is a instance of class corner_simulatior
    ##################################################
    return: dict: {"tt": tt_corner_simulatior,\
                     "ff":ff_corner_simulatior,\
                     "ss": ss_corner_simulatior}
                    "fnsp":fnsp_corner_simulatior,\
                    "snfp": snfp_corner_simulatior}
    '''
    
    '''
    tt_simulationFun = lambda x: simulation(x, boundary, targets, mode=mode, output=0, corner="tt")
    ff_simulationFun = lambda x: simulation(x, boundary, targets, mode=mode, output=0, corner="ff")
    ss_simulationFun = lambda x: simulation(x, boundary, targets, mode=mode, output=0, corner="ss")
    fnsp_simulationFun = lambda x: simulation(x, boundary, targets, mode=mode, output=0, corner="fnsp")
    snfp_simulationFun = lambda x: simulation(x, boundary, targets, mode=mode, output=0, corner="snfp")    
    simulationFun_dict = {"tt": tt_corner_simulatior,
                          "ff":ff_corner_simulatior,
                          "ss": ss_corner_simulatior,
                         "fnsp":fnsp_corner_simulatior,
                         "snfp": snfp_corner_simulatior}
    '''
    #print("generate_all_corner_simulationFun_dict")
    if corner_list is None:
        corner_list=["tt"]
    #print("corner_list:", corner_list)
    simulationFun_dict={}
    
    class corner_simulatior:
        def __init__(self, boundary, targets, mode, corner):
            self.boundary=boundary
            self.targets=targets
            self.mode=mode
            self.corner=corner
        def run(self, x):
            sim_result=simulation(x, self.boundary, self.targets, self.mode, output=0, corner=self.corner)
            return sim_result
        def __call__(self, x):
            sim_result=self.run(x)
            return sim_result
            
        
    for i in range(len(corner_list)):
        corner=corner_list[i]
        #corner_simulationFun = lambda x: simulation(x, boundary, targets, mode=mode, output=0, corner=corner)
        #simulationFun_dict[corner]=corner_simulationFun
        corner_simulator=corner_simulatior(boundary, targets, mode, corner)
        simulationFun_dict[corner]=corner_simulator
    #print("simulationFun_dict:", simulationFun_dict)
    print("$$$$$test2",simulationFun_dict)
    return simulationFun_dict


def generate_hierarchy_simulationFun_dict(boundary, targets, simulation, corner_list=None):
    # two hierarchy dict based on mode and corner
    # first level is mode, second is corner
    # mode: "all", "cheap", "expensive", "op"
    # corner: "tt", "ff", "ss", "fnsp", "snfp"
    if not corner_list:
        corner_list=["tt"]
    print("corner_list:", corner_list)
    mode_list=["all", "cheap", "expensive", "op"]
    hierarchy_simulationFun_dict={}
    #all_simulationFun_dict=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode="all", corner_list=corner_list)
    #cheap_simulationFun_dict=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode="cheap", corner_list=corner_list)
    #expensive_simulationFun_dict=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode="expensive", corner_list=corner_list)
    #op_simulationFun_dict=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode="op", corner_list=corner_list)
    #hierarchy_simulationFun_dict["all"]=all_simulationFun_dict
    #hierarchy_simulationFun_dict["cheap"]=cheap_simulationFun_dict
    #hierarchy_simulationFun_dict["op"]=op_simulationFun_dict
    #hierarchy_simulationFun_dict["expensive"]=expensive_simulationFun_dict
    for mode in mode_list:
        hierarchy_simulationFun_dict[mode]=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode=mode, corner_list=corner_list)
    #print(hierarchy_simulationFun_dict)
    
    print("$$$$$test1",hierarchy_simulationFun_dict)
    
    return hierarchy_simulationFun_dict

############test function###################
'''
import time
values=[1.32e-12, 31900.0, 1e-05, 0.35, 1.4, 1.4, 1.4, 1.4, 0.39, 1.73, 1.4, 49.0, 19.25]
start_time = time.time()
circuitOP1Simulation(values, output=1)
#dc_sweep_2, vout_dc_2, OCMR = circuitDC2Simulation(values, output=1)
#time_var, vout, SR = circuitTran2Simulation(values, output=1)
end_time = time.time()
run_time = end_time - start_time
#freq_cmrr, vout_cmrr, CMRR=circuitAC2Simulation(values, output=1)
#freq_ac, vout_ac=circuitAC1Simulation(values, output=1)[0:2]
#freq_psrr_pos, vout_psrr_pos, PSRR_pos=circuitAC3Simulation(values, output=1)
#figureplot.plotTran(time_var, vout)
#figureplot.plotFrequencyResponse(freq_ac, vout_ac)
#figureplot.plotCMRRorPSRR(freq_cmrr, vout_cmrr, title='CMRR')
#figureplot.plotCMRRorPSRR(freq_psrr_pos, vout_psrr_pos, title='PSRR+')
#figureplot.plotDC(dc_sweep_2, vout_dc_2, title='OCMR')
print("run time:", run_time)
'''
