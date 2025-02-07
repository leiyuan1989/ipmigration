#!/usr/bin/env python3
# -*- coding: utf-8 -*-




import os
import json
import time
import logging
import numpy as np

from ipmigration.analog.opt.simulator import calculator
from ipmigration.analog.opt.utils import figureplot as plt
# from ipmigration.analog.opt.utility import configuration

from ipmigration.analog.opt.simulator import spectre 
#from ipmigration.analog.opt.simulator import hspice
 
logger = logging.getLogger(__name__)

sim_cfg = json.load(open('./ipmigration/analog/opt/edb/sim_cfg.json','r'))



DVDSAT=50 #[mV]

class CirSimCfg:
    def __init__(self, cfg, sim_cfg):
        #simulator 
        if cfg.simulator == 'spectre':    
            self.Circuit = spectre.Circuit
            self.simulator = 'spectre' #command to run on terminal

     
        else:
            raise ValueError("Simulator %s is not support now"%(self.cfg.simulator))
        
        
        self.undefinedNetlistPath = {}
        self.definedNetlistPath = {}
        self.outputFilePath ={}
        self.modelCardParth = {}
        self.cornerNameList = {}
        
        self.undefinedNetlistPath["undefinedNetlist_dir"] = cfg.tb_folder
        self.definedNetlistPath["definedNetlist_dir"] = cfg.result_folder
    
        self._generate_outputFilePath(sim_cfg['data_filename'])
        self._generate_undefinedNetlistPath(sim_cfg['undefinedNetlist_file'])
        self._generate_definedNetlistPath(sim_cfg['definedNetlist_file'])
        
        #if model_cfg: still need it?
        corner_name_list=["tt", "ff", "ss", "fnsp", "snfp"]
        self._generate_modelCardPath_and_cornerNameList(cfg.model_card, corner_name_list)
    

    def _generate_outputFilePath(self, data_filename):
        self.outputFilePath["old_data_output_filename"] = r"old_data_output_filename"
        self.outputFilePath["data_filename"] = data_filename
        self.outputFilePath["data_file_dir"] = self.definedNetlistPath["definedNetlist_dir"]
        self.outputFilePath["data_file_relatively_dir"]=r'psf'
        self.outputFilePath["data_file_path"] = self.outputFilePath["data_file_dir"]+r'/' \
                                                +self.outputFilePath["data_file_relatively_dir"]+r'/' \
                                                +self.outputFilePath["data_filename"]
    def _generate_undefinedNetlistPath(self, undefinedNetlist_file):
        self.undefinedNetlistPath["undefinedNetlist_file"] = undefinedNetlist_file
    def _generate_definedNetlistPath(self, definedNetlist_file):
        self.definedNetlistPath["definedNetlist_file"] = definedNetlist_file
    def _generate_modelCardPath_and_cornerNameList(self, model_card_path, corner_name_list):
        self.modelCardParth["model_card_path"]=model_card_path
        self.modelCardParth["dummy_model_card_path"]=r"dummy_model_card_path"
        corner_key_list=corner_name_list
        for idx in range(len(corner_key_list)):
            self.cornerNameList[corner_key_list[idx]]=corner_name_list[idx]
        self.cornerNameList["dummy_corner_name"]=r"dummy_corner_name"
        






"""
simulation_opamp
simulation_level_shifter
simulation_schmitt_trigger
simulation_comparator
simulation_dynamic_comparator
"""

def simulation_opamp(decision_variable_values, cfg,
                     sim_cfg = sim_cfg, mode="all", 
                     output=None, plot=None, corner=None):
    
    # x, self.cfg, self.mode, output=self.output, corner=self.corner
    boundary = cfg.boundary
    targets = cfg.targets
    # mode: select cheep simulation or expensive simulation
    # return sim result unit:
    # [DC Gain, GBW , Phase Margin, Positive Slewrate, slewRate]
    # [dB, MHz, deg, MV/s]
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    # component_num = len(bounds["components"])
    #decision_variable_values = convert_unit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = match_DR([values], bounds)
    #print("values:", values)
    
    
    
    
    if mode=='op':
        dvdsat_list = cir_op1_sim(values, config=[cfg, sim_cfg],corner=corner, output=output)
        op_sim_result = dvdsat_list
        if output:
            #TODO revise
            print("Op simulation! \n design variables:{0} \n vdsat_list: {1} \n".format(values, op_sim_result))
        return op_sim_result
    
    if mode=='cheap': 
        cheap_sim_result = list(np.zeros(len(targets['cheap'])))
        # try:
        freq, vout, dcGain, ugf, bandwidth, phaseMargin = cir_ac1_sim(values, config=[cfg, sim_cfg],  corner=corner, output=output)
        freq_cmrr, vout_cmrr, cmrr = cir_ac2_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        freq_psrr_pos, vout_psrr_pos, psrr_pos = cir_ac3_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        dc_sweep_ocmr, vout_dc_ocmr, ocmr = cir_dc2_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        cheap_sim_result = [dcGain, ugf/1.0e6, phaseMargin, cmrr, psrr_pos, ocmr]
        cheap_sim_result = [float('{:.1f}'.format(i)) for i in cheap_sim_result]
        
        if output:
            #TODO revise
            print("Cheap simulation! \n design variables:{0} \n [DC Gain, GBW, Phase Margin, CMRR, PSRR, Output Swing]: {1} \n".format(values, cheap_sim_result))
        if plot:
            #import figureplot
            plt.plotFrequencyResponse(freq, vout)
            plt.plotCMRRorPSRR(freq_cmrr, vout_cmrr, title='CMRR')
            plt.plotDC(dc_sweep_ocmr, vout_dc_ocmr, title='OCMR')
        return cheap_sim_result

    elif mode=='expensive': 
        expensive_sim_result = list(np.zeros(len(targets['expensive'])))
        # try:
        time_var, vout_tran, slewRate = cir_tran1_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        time_var1, vout_tran1, slewRateNeg = cir_tran2_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        expensive_sim_result = [slewRate/1.0e6, slewRateNeg/1.0e6]
        expensive_sim_result = [float('{:.1f}'.format(i)) for i in expensive_sim_result]
        if output:
            #TODO revise
            print("Expensive simulation! \ndesign variables:{0} \n [Positive Slewrate, Negative slewRate]: {1} \n".format(values, expensive_sim_result))
        if plot:
            #import figureplot
            plt.plotTran(time_var, vout_tran)
            plt.plotTran(time_var1, vout_tran1)
        return expensive_sim_result
        # except:
        #     print("Expensive simulation error!")
        #     return expensive_sim_result
    
    elif mode=='all':
        sim_result = list(np.zeros(len(targets['expensive'])+len(targets['cheap'])))
        # try:
        #print("Do OP1 Simulation")
        #num_saturation_device = circuitOP1Simulation(values, config=[cfg, sim_cfg], config=[cfg, sim_cfg], corner=corner, output=output)
        #print("dvdsat list:", dvdsat_list)
        #print("Do AC1 Simulation")
        freq, vout, dcGain, ugf, bandwidth, phaseMargin = cir_ac1_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        #print("Do Trans1 Simulation")
        time_var, vout_tran, slewRate = cir_tran1_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        #print("Do Trans2 Simulation")
        time_var1, vout_tran1, slewRateNeg = cir_tran2_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        #print("Do AC2 Simulation")
        freq_cmrr, vout_cmrr, cmrr = cir_ac2_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        #print("Do AC3 Simulation")
        freq_psrr_pos, vout_psrr_pos, psrr_pos = cir_ac3_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        #print("Do DC2 Simulation")
        dc_sweep_ocmr, vout_dc_ocmr, ocmr = cir_dc2_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
        
        #op_sim_result=[num_saturation_device]
        op_sim_result=[]
        
        cheap_sim_result = [dcGain, ugf/1.0e6, phaseMargin, cmrr, psrr_pos, ocmr]
        cheap_sim_result = [float('{:.1f}'.format(i)) for i in cheap_sim_result]
        expensive_sim_result = [slewRate/1.0e6, slewRateNeg/1.0e6]
        expensive_sim_result = [float('{:.1f}'.format(i)) for i in expensive_sim_result]
        sim_result = op_sim_result + cheap_sim_result + expensive_sim_result
        if plot:
            #import figureplot
            time.sleep(1)
            plt.plotFrequencyResponse(freq, vout)
            plt.plotTran(time_var, vout_tran)
            plt.plotTran(time_var1, vout_tran1)
            plt.plotCMRRorPSRR(freq_cmrr, vout_cmrr, title='CMRR')
            plt.plotDC(dc_sweep_ocmr, vout_dc_ocmr, title='OCMR')
        
        logger.info("\n run simulation_opamp: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
        if output:
            print("\n run simulation_opamp: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
                            
        return sim_result


def simulation_level_shifter(decision_variable_values, cfg,
                             sim_cfg = sim_cfg, mode="all", 
                             output=None, plot=None, corner=None):
    """
    # return: sim result
    #unit:
    # [rise_time, fall_time, delay, avg_total_power]
    # [sec, sec, sec, W]
    """
    boundary = cfg.boundary
    targets = cfg.targets
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    # component_num = len(bounds["components"])
    #decision_variable_values = convert_unit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = match_DR([values], bounds)
     
    sim_result = list(np.zeros(len(targets['all targets value'])))
    # try:
    time_var_out, vout_tran, time_var_in, vin_tran,\
    ivddl_tran, ivddh_tran,\
    rise_time, fall_time, delay, avg_total_power = levelShifter_tran1_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
    sim_result = [rise_time, fall_time, delay, avg_total_power]
    sim_result = [float('{:.2e}'.format(i)) for i in sim_result]
    
    logger.info("\n run simulation_level_shifter: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
    if output:
        print("\n run simulation_level_shifter: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
    if plot:
        plt.plotSchmittTrigger(time_var_in, vin_tran, time_var_out, vout_tran)
    return sim_result


def simulation_schmitt_trigger( decision_variable_values, cfg, 
                               sim_cfg = sim_cfg, mode="all", 
                               output=None, plot=None, corner=None):
    """
    # return: sim result
    #unit:
    # [vih, vil, hysterisis_window]
    # [V, V, mV]
    """
    boundary = cfg.boundary
    targets = cfg.targets
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    # component_num = len(bounds["components"])
    #decision_variable_values = convertUnit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = match_DR([values], bounds)
     
    sim_result = list(np.zeros(len(targets['all targets value'])))
    # try:
    time_var_out, vout_tran, time_var_in, vin_tran,\
    vih, vil, window = schmittTrigger_tran1_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
    sim_result = [vih, vil, window]
    sim_result = [float('{:.2f}'.format(i)) for i in sim_result]
    logger.info("\n run simulation_schmitt_trigger: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
    if output:
        print("\n run simulation_schmitt_trigger: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
    if plot:
        plt.plotSchmittTrigger(time_var_in, vin_tran, time_var_out, vout_tran)
    return sim_result
 

def simulation_comparator(decision_variable_values, cfg, 
                          sim_cfg = sim_cfg, mode="all", 
                          output=None, plot=None, corner=None):
    """
    # return: sim result
    #unit:
    # [vos, delay_rise, delay_fall, voh, vol, ipwr_avg]
    # [mV, nsec, V, V, uA]
    """
    boundary = cfg.boundary
    targets = cfg.targets
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    # component_num = len(bounds["components"])
    #decision_variable_values = convert_unit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = match_DR([values], bounds)
     
    sim_result = list(np.zeros(len(targets['all targets value'])))
    # try:
    time_var_inp1, vinp_tran1, time_var_inn1,\
    vinn_tran1, time_var_out1, vout_tran1, \
    vos = comparator_tran1_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
    
    time_var_inp2, vinp_tran2,\
    time_var_out2, vout_tran2,\
    delay_rise, delay_fall, voh, vol, ipwr_avg = comparator_tran2_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
    sim_result = [vos, delay_rise, delay_fall, voh, vol, ipwr_avg]
    sim_result = [float('{:.3e}'.format(i)) for i in sim_result]
    logger.info("\n run simulation_comparator: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
    if output:
        print("\n run simulation_comparator: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
    if plot:
        plt.plotComparatorOffset(time_var_inp1, vinp_tran1, time_var_inn1,\
                                        vinn_tran1, time_var_out1, vout_tran1)
        plt.plotClockDelay(time_var_inp2, vinp_tran2, \
                                  time_var_out2,vout_tran2)
    return sim_result


def simulation_dynamic_comparator(decision_variable_values, cfg,
                                  sim_cfg = sim_cfg, mode="all", 
                                  output=None, plot=None, corner=None):
    """
    # return: sim result
    #unit:
    # [vos, vop_rise_time, vop_fall_time, von_rise_time, von_fall_time, delay_rise, delay_fall]
    # [mV, nsec, nsec, nsec, nsec, nsec, nsec]
    """
    boundary = cfg.boundary
    targets = cfg.targets
    # convert vaules from pF kohm uA to UI
    bounds = boundary.bounds
    # component_num = len(bounds["components"])
    #decision_variable_values = convert_unit(decision_variable_values, bounds)
    #print("decision_variable_values:", decision_variable_values)
    values = generate_all_values(decision_variable_values, boundary)
    [values] = match_DR([values], bounds)
     
    sim_result = list(np.zeros(len(targets['all targets value'])))
    # try:
    time_var_clk1, vclk_tran1, \
    time_var_inp1, vinp_tran1, time_var_inn1,\
    vinn_tran1, time_var_outp1, voutp_tran1, \
    time_var_outn1, voutn_tran1, \
    vos, vop_rise_time, vop_fall_time, \
    von_rise_time, von_fall_time = dynamic_comparator_tran1_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
    
    time_var_clk2, vclk_tran2, time_var_outp2,\
        voutp_tran2, delay_rise, delay_fall = dynamic_comparator_tran2_sim(values, config=[cfg, sim_cfg], corner=corner, output=output)
    sim_result = [vos, vop_rise_time, vop_fall_time, \
                  von_rise_time, von_fall_time, delay_rise, delay_fall]
    sim_result = [float('{:.3e}'.format(i)) for i in sim_result]
    logger.info("\n run simulation_dynamic_comparator: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
    if output:
       print("\n run simulation_dynamic_comparator: \n variables: %s \n outputs: %s"%(str(values), str(sim_result) ))
    if plot:
        plt.plotDynamicComparatorOffset(time_var_clk1, vclk_tran1, \
                                        time_var_inp1, vinp_tran1, time_var_inn1,\
                                        vinn_tran1, time_var_outp1, voutp_tran1, \
                                        time_var_outn1, voutn_tran1)
        plt.plotClockDelay(time_var_clk2, vclk_tran2, \
                                  time_var_outp2,voutp_tran2)
    return sim_result

        
        
   
        




'''
cir_ac1_sim
cir_tran1_sim
cir_tran2_sim
cir_ac2_sim
cir_ac3_sim
cir_dc1_sim
cir_dc2_sim
cir_op1_sim

'''





def cir_ac1_sim(values, config, corner=None, output=None):
    cfg, sim_cfg = config
    # print(config)
    config = CirSimCfg(cfg, sim_cfg['ac1'])
    
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
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, ac_data_filename)
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    
    # define design variable value
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(ac_data_file_path)
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
        #TODO move to log
        logger.info('run cir_ac1_sim')
        logger.info('dcgain: %.5E X'%(dcGain))
        logger.info('dcgain in dB: %.1f dB'%(dcGain_dB))
        logger.info('UnityGainFrequency: %.2e kHz'%(float(ugf/1e3)))
        logger.info('3dB-bandwidth: %.2e kHz'%(float(bandwidth/1e3)))
        logger.info('PhaseMargin: %.1f degree'%(phaseMargin))
        logger.info('parameters: %s'%(str(device_parameters))) 
        logger.info('parameters_values: %s'%(str(device_parameter_values))) 
    return freq, vout, dcGain, ugf, bandwidth, phaseMargin


def cir_tran1_sim(values, config, corner=None, output=None):   
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['tran1'])
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
        
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(tran_data_file_path)   
    # read the simulation output produced by the 'wrdata' command
    time_var, vout_tran = circuit.getTranData(tran_data_file_path, portname="out", index_list=[1])

    # calculate Slew Rate
    slewRate = calculator.slewRate(time_var, vout_tran)
    slewRate_us=slewRate/1e6

    # get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        logger.info('slewRate: %.1f V/us' %(slewRate_us))
        logger.info('parameters: %s'%(str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return time_var, vout_tran, slewRate


def cir_tran2_sim(values, config, corner=None, output=None):
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['tran2'])
    
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
        
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(tran_data_file_path)
    
    # read the simulation output produced by the 'wrdata' command
    time_var, vout_tran = circuit.getTranData(tran_data_file_path, portname="out", index_list=[1]) 

    # calculate Slew Rate Negative
    slewRateNeg = calculator.slewRateNeg(time_var, vout_tran)
    slewRateNeg_us=slewRateNeg/1e6
    
    # get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)   
    
    if output:
        logger.info('slewRateNeg: %.1f V/us'%(slewRateNeg_us))
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return time_var, vout_tran, slewRateNeg


def cir_ac2_sim(values, config, corner=None, output=None):    
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['ac2'])
    
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
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, ac_data_filename)
    
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(ac_data_file_path)
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
        logger.info('CMRR: %.5E X' % CMRR)
        logger.info('CMRR in dB: %.1f dB' % CMRR_dB)
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return freq, vout, CMRR

def cir_ac3_sim(values, config, corner=None, output=None):    
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['ac3'])
    
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
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, ac_data_filename)
    
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(ac_data_file_path)
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
        logger.info('PSRR+: %.5E X' % PSRR_pos)
        logger.info('PSRR+ in dB: %.1f dB' % PSRR_pos_dB)
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return freq, vout, PSRR_pos


def cir_dc1_sim(values, config, corner=None, output=None):    
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['dc1'])
    
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
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, dc_data_filename)
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(dc_data_file_path)
    # read the simulation output produced by the 'wrdata' command
    dc_sweep, vout_dc = circuit.getDCData(dc_data_file_path, [1])    
    # calculate ICMR 
    ICMR = calculator.ICMR(dc_sweep, vout_dc)
    # get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)
    
    if output:
        logger.info('ICMR: %.3f V' % ICMR)
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return dc_sweep, vout_dc, ICMR

def cir_dc2_sim(values, config, corner=None, output=None):    
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['dc2'])
    
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
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, dc_data_filename)
    
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(dc_data_file_path)
    # read the simulation output produced by the 'wrdata' command
    dc_sweep, vout_dc = circuit.getDCData(dc_data_file_path, [1])    
    # calculate OCMR 
    OCMR = calculator.OCMR(dc_sweep, vout_dc)
    # get device_parameters   
    device_parameters=list(circuit.parameters)
    device_parameter_values=list(parameters_values)
    
    if output:
        logger.info('Outout Swing: %.3f V' % OCMR)
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return dc_sweep, vout_dc, OCMR

def cir_op1_sim(values, config, corner=None, output=None):    
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['op1'])
    
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
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, op_data_filename)
    
    # define model card and corner
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)

    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(op_data_file_path)
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
        logger.info('{0} devices dvdsat list: {1}'.format(len(dvdsat_list), dvdsat_list))
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
        logger.info("device_name_list %s:"%(str(device_name_list)))
        logger.info("dvdsat_list: %s"%(str(dvdsat_list))) 
    return num_saturation_device


#------------------------------------------------------------------------------
'''
levelShifter_tran1_sim

'''

def levelShifter_tran1_sim(values, config, corner=None, output=None):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: time_var_out, vout_tran, time_var_in, vin_tran, v_ih, v_il, window
    #print(config.modelCardParth)
    """
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['level_shifter_tran1'])
    
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
        
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(tran_data_file_path)   
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
        logger.info('rise_time: {0:.2e}s, fall_time:{1:.2e}s, delay: {2:.2e}s, avg_total_power: {3:.2e}W'.format(rise_time, fall_time, delay, avg_total_power))
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return time_var_out, vout_tran, time_var_in, vin_tran,  ivddl_tran, ivddh_tran, rise_time, fall_time, delay, avg_total_power


#------------------------------------------------------------------------
'''
schmittTrigger_tran1_sim

'''

def schmittTrigger_tran1_sim(values, config, corner=None, output=None):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: time_var_out, vout_tran, time_var_in, vin_tran, v_ih, v_il, window
    #print(config.modelCardParth)
    """
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['schmitt_trigger_tran1'])
    
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
        
    circuit=config.Circuit(undefinedNetlistPath)
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
        logger.info('v_ih: {0:.3f}V, v_il:{1:.3f}V, window: {2:.1f}mV'.format(v_ih, v_il, window))
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return time_var_out, vout_tran, time_var_in, vin_tran, v_ih, v_il, window


#------------------------------------------------------------------------------
'''
comparator_tran1_sim
comparator_tran2_sim

'''
def comparator_tran1_sim(values, config, corner=None, output=None):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: vos(offset voltage) [mV]
    #print(config.modelCardParth)
    """
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['comparator_tran1'])
    
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
        
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(tran_data_file_path)   
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
        logger.info('offset_voltage vos: {0:.3e} mV'.format(vos))
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return  time_var_inp, vinp_tran, \
            time_var_inn, vinn_tran, time_var_out, vout_tran, \
           vos


def comparator_tran2_sim(values, config, corner=None, output=None):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: delay, voh, vol, ipwr_avg
    #         nsec, V,     V,  uA
    #print(config.modelCardParth)
    """
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['comparator_tran2'])
    
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
        
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(tran_data_file_path)   
    #read the simulation output produced by the 'wrdata' command
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
        logger.info('delay_rise: {0:.3e} nsec, delay_fall: {1:.3e} nsec, voh: {2:.2f} V, vol: {3:.2f} V, ipwr_avg: {4:.3e} uA'.format(delay_rise, delay_fall, voh, vol, ipwr_avg))
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
        plt.plotTranPower(time_var_ivdd, ivdd_tran)
    return time_var_inp, vinp_tran, time_var_out, vout_tran, delay_rise, delay_fall, voh, vol, ipwr_avg



#------------------------------------------------------------------------------
'''
dynamic_comparator_tran1_sim
dynamic_comparator_tran2_sim

'''

def dynamic_comparator_tran1_sim(values, config, corner=None, output=None):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: vos(offset voltage) [mV]
    #print(config.modelCardParth)
    """
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['dynamic_comparator_tran1'])
    
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
        
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(tran_data_file_path)   
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
        logger.info('offset_voltage vos: {0:.3e} mV,\
              vop_rise_time: {1:.3e} ns, vop_fall_time: {2:.3e} ns,  \
              von_rise_time: {3:.3e} ns, von_fall_time: {4:.3e} ns'.format(vos, vop_rise_time, vop_fall_time, \
                  von_rise_time, von_fall_time))
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return time_var_clk, vclk_tran, time_var_inp, vinp_tran, time_var_inn, vinn_tran, time_var_outp, voutp_tran, \
           time_var_outn, voutn_tran, vos, vop_rise_time, vop_fall_time, von_rise_time, von_fall_time

#------------------------------------------------------------------------
def dynamic_comparator_tran2_sim(values, config, corner=None, output=None):   
    """
    # corner: "tt", ["tt", "ff", "ss", "fnsp", "snfp"]
    # return: delay
    #print(config.modelCardParth)
    """
    cfg, sim_cfg = config
    config = CirSimCfg(cfg, sim_cfg['dynamic_comparator_tran1'])
    
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
        
    circuit=config.Circuit(undefinedNetlistPath)
    netlistUndefined=circuit.netlistUndefined.replace(old_data_output_filename, tran_cmd_name)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_model_card_path, model_card_path)
    circuit.netlistUndefined=netlistUndefined
    netlistUndefined=circuit.netlistUndefined.replace(dummy_corner_name, corner_name)
    circuit.netlistUndefined=netlistUndefined
    circuit.getNetlist(parameters_values, definedNetlistPath)
    circuit.run_simulator(tran_data_file_path)   
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
        logger.info('delay_rise: {0:.3e} nsec, delay_fall: {1:.3e}'.format(delay_rise, delay_fall))
        logger.info('parameters: %s'%( str(device_parameters)))
        logger.info('parameters_values: %s'%(str(device_parameter_values)))
    return time_var_clk, vclk_tran, time_var_outp, voutp_tran, delay_rise, delay_fall




'''
match_DR
generate_all_values
convert_unit
'''

##################################################################
def match_DR(values_list, bounds):
    # values_list:list, tmp_list:list
    #print("match_DR")
    component_num=len(bounds["components"])
    tmp_list=[]
    for values in values_list:
        tmp = [float('{:.3e}'.format(i)) for i in values[:component_num] ] \
            + [float('{:.2f}'.format(i)) for i in values[component_num:]]
        tmp_list.append(tmp)     
    #print("tmp_list:", tmp_list)
    return tmp_list

##################################################################
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
    decision_variable_values = convert_unit(decision_variable_values, bounds)
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


##################################################################
'''
For W L covertion
'''
def convert_unit(values, bounds):
    #values:np.array, tmp: np.array
    #print("convert_unit")
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
    #print("convert_unit:", tmp)
    return tmp



class CornerSimulatior:
    def __init__(self, cfg,  mode, corner):
        self.cfg=cfg
        self.boundary=cfg.boundary
        self.targets=cfg.targets
        self.mode=mode
        self.corner=corner
        self.simulation_func = cfg.simulation_func
        self.output = cfg.output
    def run(self, x):
        sim_result=self.simulation_func(x, self.cfg, mode=self.mode, output=self.output, corner=self.corner)
        
        return sim_result
    def __call__(self, x):
        sim_result=self.run(x)
        return sim_result


def gen_corners_sim_dict(cfg,  mode="all"):
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
    # boundary, targets, simulation, 
    corner_list = cfg.corner_list

    if not cfg.corner_list:
        corner_list=["tt"]
    

    #print("corner_list:", corner_list)
    simulationFun_dict={}
    
    for i in range(len(corner_list)):
        corner=corner_list[i]
        #corner_simulationFun = lambda x: simulation(x, boundary, targets, mode=mode, output=0, corner=corner)
        #simulationFun_dict[corner]=corner_simulationFun
        
        # cfg,  mode, corner, output
        corner_simulator=CornerSimulatior(cfg, mode, corner)
        
        simulationFun_dict[corner]=corner_simulator
    #print("simulationFun_dict:", simulationFun_dict)
    return simulationFun_dict


def gen_hierarchy_sim_dict(cfg):
    # boundary = cfg.boundary
    # targets = cfg.targets
    # simulation = cfg.simulation_func

    
    # two hierarchy dict based on mode and corner
    # first level is mode, second is corner
    # mode: "all", "cheap", "expensive", "op"
    # corner: "tt", "ff", "ss", "fnsp", "snfp"
    mode_list=["all", "cheap", "expensive", "op"]
    hierarchy_sim_dict={}
    #all_simulationFun_dict=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode="all", corner_list=corner_list)
    #cheap_simulationFun_dict=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode="cheap", corner_list=corner_list)
    #expensive_simulationFun_dict=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode="expensive", corner_list=corner_list)
    #op_simulationFun_dict=generate_all_corner_simulationFun_dict(boundary, targets, simulation=simulation, mode="op", corner_list=corner_list)
    #hierarchy_sim_dict["all"]=all_simulationFun_dict
    #hierarchy_sim_dict["cheap"]=cheap_simulationFun_dict
    #hierarchy_sim_dict["op"]=op_simulationFun_dict
    #hierarchy_sim_dict["expensive"]=expensive_simulationFun_dict
    for mode in mode_list:
        hierarchy_sim_dict[mode]=gen_corners_sim_dict(cfg, mode=mode)
    #print(hierarchy_sim_dict)

    
    return hierarchy_sim_dict





