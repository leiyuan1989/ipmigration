# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:12:19 2023

@author: shunqidai

MODIFIED read_op_analysis
26/09/2024
"""

#import time
import os
import subprocess
import shlex
import numpy as np

import traceback
from string import Formatter


class Circuit:
    """    cfg = {
                'ngspice' : r'C:\\Users\shunqidai\ngspice-41_64\Spice64\bin\ngspice_con.exe', 
                } # ngspice path
        
        undefinedNetlistPath = {
                'undefinedNetlist_dir' : r'.\smic018\netlist',
                'undefinedNetlist_file' : r'\diffamp_ac1.sp',
                } # undefined Netlist path
        
        definedNetlistPath = {
                'definedNetlist_dir' : r'.\smic018\simResult',
                'definedNetlist_file' : r'\test_diffamp_ac1.sp',
                } # defined Netlist path  """

    
    def __init__(self, undefinedNetlistPath,):
        # 指定目录的路径
        self.undefinedNetlist_dir = undefinedNetlistPath['undefinedNetlist_dir']
        self.undefinedNetlist_file_path = undefinedNetlistPath['undefinedNetlist_dir'] + undefinedNetlistPath['undefinedNetlist_file']
        self.cir_file_path = None
        
        # print("&&&&test3",self.undefinedNetlist_file_path)
        # raise ValueError
        
        # 检查目录是否存在
        if not os.path.exists(self.undefinedNetlist_dir):
            os.makedirs(self.undefinedNetlist_dir)   # 创建目录
        
        with open(self.undefinedNetlist_file_path) as f:
            self.netlistUndefined = f.read()
            #print("netlistUndefined:", self.netlistUndefined) 
        
        self.parameters=list(set(i[1] for i in Formatter().parse(self.netlistUndefined) if i[1] ))
        print("&&&test4", self.parameters)      
        # ['w1', 'l4', 'cr', 'l2', 'w3', 'w5', 'cc', 'w2', 'w4', 'l5', 'l3', 'ib', 'l1']  
        if self.parameters:
            # raise ValueError
            self.parameters.sort()
            
    def getNetlist(self, parameter_values, definedNetlistPath):
        cir_dir = definedNetlistPath['definedNetlist_dir']
        self.cir_file_path = definedNetlistPath['definedNetlist_dir'] + definedNetlistPath['definedNetlist_file']
        try:
            mapping=dict(zip(self.parameters, parameter_values))
            # raise ValueError
            netlist = self.netlistUndefined.format(**mapping)
            # 检查目录是否存在
            if not os.path.exists(cir_dir):
            # 创建目录
                os.makedirs(cir_dir)
            cir_file = open(self.cir_file_path, 'w')
            cir_file.write(netlist)
            cir_file.close()
            
        except:
            traceback.print_exc()
            raise ValueError("insufficient number of parameters.")

        
    def run_simulator(self, outfilepath):
        #print("outfilepath:", outfilepath) 
        infile=self.cir_file_path
        output_dir = os.path.dirname(outfilepath)
        #print("output_dir:", output_dir)
        output_filename = os.path.split(outfilepath)[-1]
        output_filename = output_filename.split('.')[0]
        #print("output_filename:", output_filename)
        logname=output_filename+r"_spectre.out"
        logfile= output_dir+r'/'+logname
        spectre_args = ["spectre -64",
                infile,
                "+escchars",
                "=log "  + logfile,
                "-format psfascii",
                "-raw "  + output_dir,
                "++aps=moderate",
                #"++aps ",
                "+mt=32",
                "+lqtimeout 900",
                "-maxw 5",
                "-maxn 5",
                "+logstatus"]
        
        run_string = ""
        for i in spectre_args:
            run_string = run_string + i + " "

        #print("run_string:", run_string)
        run_command = shlex.split(run_string)
        #try:
        print("Running simulation...", run_command)
        #subprocess.call(run_command)
        process=subprocess.Popen(run_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = process.communicate()
        #print("Done.")

        return 0
        #except:
         #   raise SimulationError("Spectre Simulation Error!!!")
            
    
    
    
    
    
    
    #
    
    
    
    
    
    
    
    
    
    
    
    # read the data written by the 'wrdata' command after an ac analysis
    # index_list = [[1,2], [4,5], ...] for the real and imaginary components
    # the indices 0, 3, 6, 9, ... are the values of freq_var
    def read_ac_analysis(self, ac_data_file, index_list):
        '''
        freq_var = []
        data_array = [ [] for i in range(len(index_list)) ]
        
        with open(ac_data_file, 'r') as f:
            for line in f:
                freq_var.append(float(line.split()[0]))
                
                for idx, val in enumerate(index_list):
                    data_array[idx].append(float(line.split()[val[0]]) + \
                        float(line.split()[val[1]]) * 1j)
        '''
        header = 1
        freq = []

        vout_mag = []
        vout_phase = []
        vout_complex = []
        
        with open(ac_data_file, 'r') as f:
           for line_terminated in f:
               # read simulation output line by line
               # assumed to be 'psfascii'
               line = line_terminated.rstrip('\n')
               
               if line == "VALUE":     # simulation data starts here
                   header = 0
                   
               if header == 0:
                   # remove the parenthesis in the data
                   line1 = line.replace('(', '')
                   line2 = line1.replace(')', '')
                   
                   # split the data into strings if a space is encountered
                   line_val = shlex.split(line2)
                   
                   # find frequency values
                   if line_val[0] == "freq":
                       freq.append(float(line_val[1]))
                       
                   # find the output voltage values
                   # this is the name you chose in the netlist
                   # simulation data is formatted as (real, imaginary)
                   if line_val[0] == "out":
                       vout = float(line_val[1]) + (1j * float(line_val[2]))
                       vout_complex.append(vout)
                       mag = np.absolute(vout)
                       phase = np.angle(vout)
                       vout_mag.append(mag)
                       vout_phase.append(phase)
        
        return freq, vout_complex

    # read the data written by the 'wrdata' command after a dc analysis
    # index_list = [1, 3, 5, ...] since the even indices are the sweep_var values
    def read_dc_analysis(self, dc_data_file, index_list):
        '''
        sweep_var = []
        data_array = [ [] for i in range(len(index_list)) ]
        
        with open(dc_data_file, 'r') as f:
            for line in f:
                sweep_var.append(float(line.split()[0]))
                
                for idx, val in enumerate(index_list):
                    data_array[idx].append(float(line.split()[val]))
                    
        return sweep_var, data_array
        '''
        header = 1
        v_in = []
        vout = []

        with open(dc_data_file, 'r') as f:
           for line_terminated in f:
               # read simulation output line by line
               # assumed to be 'psfascii'
               line = line_terminated.rstrip('\n')
               
               if line == "VALUE":     # simulation data starts here
                   header = 0
                   
               if header == 0:
                   # remove the parenthesis in the data
                   line1 = line.replace('(', '')
                   line2 = line1.replace(')', '')
                   
                   # split the data into strings if a space is encountered
                   line_val = shlex.split(line2)
                   
                   # find frequency values
                   if line_val[0] == "v_in":
                       v_in.append(float(line_val[1]))
                       
                   # find the output voltage values
                   # this is the name you chose in the netlist
                   # simulation data is formatted as (real, imaginary)
                   if line_val[0] == "out":
                       vout_value = float(line_val[1]) 
                       vout.append(vout_value)        
                       
        return v_in, vout
    
    # read the data written by the 'wrdata' command after a transient analysis
    # index_list = [1, 3, 5, ...] since the even indices are the time_var values
    def read_tran_analysis(self, tran_data_file, index_list, portname="out"):
        '''
        time_var = []
        data_array = [ [] for i in range(len(index_list)) ]
        
        with open(tran_data_file, 'r') as f:
            for line in f:
                time_var.append(float(line.split()[0]))
                
                for idx, val in enumerate(index_list):
                    data_array[idx].append(float(line.split()[val]))
                    
        return time_var, data_array
        '''
        header = 1
        time = []
        vout = []

        with open(tran_data_file, 'r') as f:
           for line_terminated in f:
               # read simulation output line by line
               # assumed to be 'psfascii'
               line = line_terminated.rstrip('\n')
               
               if line == "VALUE":     # simulation data starts here
                   header = 0
                   
               if header == 0:
                   # remove the parenthesis in the data
                   line1 = line.replace('(', '')
                   line2 = line1.replace(')', '')
                   
                   # split the data into strings if a space is encountered
                   line_val = shlex.split(line2)
                   
                   # find frequency values
                   if line_val[0] == "time":
                       time.append(float(line_val[1]))
                       
                   # find the output voltage values
                   # this is the name you chose in the netlist
                   # simulation data is formatted as (real, imaginary)
                   if line_val[0] == portname:
                       vout_value = float(line_val[1]) 
                       vout.append(vout_value)        
                       
        return time, vout
    
    def getDCData(self, dc_data_file, index_list=[1]):
        #sweep_var, [vout_dc] = self.read_dc_analysis(dc_data_file, index_list)
        sweep_var, vout_dc = self.read_dc_analysis(dc_data_file, index_list)
        return sweep_var, vout_dc
    
    def getACData(self, ac_data_file, index_list=[[1,2]]):
        #freq, [vout_ac] = self.read_ac_analysis(ac_data_file, index_list)
        freq, vout_ac = self.read_ac_analysis(ac_data_file, index_list)
        return freq, vout_ac
    
    def getTranData(self, tran_data_file, portname="out", index_list=[1]):
        #time_var, [vout_tran] = self.read_tran_analysis(tran_data_file, index_list)
        time_var, vout_tran = self.read_tran_analysis(tran_data_file, index_list, portname)
        return time_var, vout_tran
    
    # read the data written by the 'wrdata' command after an op analysis
    # extract data from even column
    #def read_op_analysis(self, op_data_file):
    def read_op_analysis(self, op_data_file):
        '''
        '''
        header = 1
        device_name_array = []
        vdsat_array = []
        vds_array = []

        with open(op_data_file, 'r') as f:
           for line_terminated in f:
               # read simulation output line by line
               # assumed to be 'psfascii'
               line = line_terminated.rstrip('\n')
               #print("line:", line)
               if line == "VALUE":     # simulation data starts here
                   header = 0
                   
               if header == 0:
                   # remove the parenthesis in the data
                   line1 = line.replace('(', '')
                   line2 = line1.replace(')', '')
                   #print("line2:", line2)
                   # split the data into strings if a space is encountered
                   line_val = shlex.split(line2)
                   #print("line_val:", line_val)
                   
                   # find device_name_array
                   if len(line_val):
                       if ":vds" in line_val[0]:
                           vds=line_val[2]
                           vdsat_array.append(vds)
                           
                       if ":vdsat" in line_val[0]:
                           device_name=line_val[0].split(":")
                           device_name=device_name[0]
                           #device_name=line_val[0]
                           vdsat=line_val[2]
                           #print("device_name:", device_name)
                           #print("vdsat:", vdsat)
                           device_name_array.append(device_name)
                           vdsat_array.append(vdsat)
        vds_array=np.array(vds_array)
        vdsat_array=np.array(vdsat_array)
        dvdsat_array=np.abs(vds_array)-np.abs(vdsat_array)
        return device_name_array, dvdsat_array
    
    def getOpData(self, op_data_file):
        device_name_array, vdsat_array = self.read_op_analysis(op_data_file)
        return device_name_array, vdsat_array

        