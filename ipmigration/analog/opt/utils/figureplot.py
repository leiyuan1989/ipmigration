# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:36:54 2023

@author: shunqidai

add plotSchmittTrigger 27/08/2024
"""
import time
import numpy as np
import matplotlib.pyplot as plt

def plot_result(cfg, optimizer,pareto_set):
    
    ############### Plot result ###################
        
    run_time = optimizer.run_time

    all_pareto_set_result=[]
    all_pareto_set_corner_list=[]
    for best_solution in pareto_set:
        for corner in cfg.corner_list:
            result=cfg.simulation_func(best_solution, cfg, mode="all", output=1, plot=1, corner=corner)
        
            all_pareto_set_result.append(result)
            all_pareto_set_corner_list.append(corner)
    
    time.sleep(1)
    print("\npareto set:")
    for j in pareto_set:
        print(j)
    
    print("Specification:\n", cfg.targets['all targets value'])
    print("pareto set simulation result:")
    for j in range(len(all_pareto_set_result)):
        print(all_pareto_set_corner_list[j], all_pareto_set_result[j])
    
    print("run_time:", run_time)  
    
    
    
# -------------------------
# Plotting helper functions
# -------------------------

# label a plot
def label_plot(plt_cfg, fig, ax):
    ax.grid(True)
    ax.grid(linestyle=plt_cfg['grid_linestyle'])
    ax.set_title(plt_cfg['title'])
    ax.set_xlabel(plt_cfg['xlabel'])
    ax.set_ylabel(plt_cfg['ylabel'])
    if plt_cfg['add_legend']:
        ax.legend(loc=plt_cfg['legend_loc'], title=plt_cfg['legend_title'])
    fig.set_tight_layout('True')
    
# add a vertical line with text annotation
def add_vline_text(ax, xd, ypos, txt_label):
    ax.axvline(x=xd, color='gray', linestyle='-.', linewidth=1)
    ax.text(xd, ypos, txt_label, \
        rotation=90, color='black', \
        horizontalalignment='right', verticalalignment='bottom')
    
# add a horizontal line with text annotation
def add_hline_text(ax, yd, xpos, txt_label):
    ax.axhline(y=yd, color='gray', linestyle='-.', linewidth=1)
    ax.text(xpos, yd, txt_label,\
        rotation=0, color='black', \
        horizontalalignment='left', verticalalignment='bottom')
    
# -----------------------
# Miscellaneous functions
# -----------------------

# calculate the index and closest value (in a list) to a given number
def find_in_data(data, value):
    index, closest = min(enumerate(data), key=lambda x: abs(x[1] - value))
    
    return index, closest
    
# scale a vector or list by f
def scale_vec(value, f):       
    return [v/f for v in value]


# -------------------------------------------------------------------
# plot AC FrequencyResponse function
#-------------------------------------------------------------------
def plotFrequencyResponse(freq, vout):    
    amplitude_vout = 20*np.log10((np.abs(np.array(vout)))) 
    phase_vout = np.angle(np.array(vout), deg=True)
    while np.sum(phase_vout > 0):
        phase_vout[np.where(phase_vout > 0)] -= 360
#    print(amplitude_vout)
#    print(phase_vout)
# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Opamp Amplitude Response',
            'xlabel' : r'$Frequency$ [MHz]',
            'ylabel' : r'$Magnitude$ [dB]',
            'legend_loc' : 'upper right',
            'add_legend' : False,
            'legend_title' : r'Magnitude'
                }

    plt_cfg2 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Opamp Phase Response',
            'xlabel' : r'$Frequency$ [MHz]',
            'ylabel' : r'$Phase$ [deg]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }
    
# plot the freq vs the frequency
    fig = plt.figure(figsize=(6,8))
    ax1 = fig.add_subplot(2, 1, 1)

    ax1.plot(scale_vec(freq, 1e6), scale_vec(amplitude_vout, 1), '-', linewidth=2)
    ax1.set_xscale('log') 

    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(scale_vec(freq, 1e6), scale_vec(phase_vout, 1), '-', linewidth=2)
    ax2.set_xscale('log') 
    
# label the plot
    label_plot(plt_cfg1, fig, ax1)
    label_plot(plt_cfg2, fig, ax2)
    
    return 'plot Frequency Response successfully!'


# -------------------------------------------------------------------
# plot AC CMRR function
#-------------------------------------------------------------------
def plotCMRRorPSRR(freq, vout, title='CMRR'):

    """
    Parameters
    ----------
    freq : TYPE
        DESCRIPTION.
    vout : TYPE
        DESCRIPTION.
    title : 'CMRR', 'PSRR+', 'PSRR-' 
        
    Returns
    -------
    None."""
    
    amplitude_vout = np.abs(np.array(vout))
    oneOverVout_dB = 20*np.log10(1/amplitude_vout)
#    print(amplitude_vout)
# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Opamp CMRR VS Frequency',
            'xlabel' : r'$Frequency$ [MHz]',
            'ylabel' : r'$CMRR$ [dB]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }
    
    if title ==  'PSRR+':
        plt_cfg1['title'] = r'Opamp PSRR+ VS Frequency'
        plt_cfg1['ylabel'] = r'$PSRR+$ [dB]'
    elif title == 'PSRR-':
        plt_cfg1['title'] = r'Opamp PSRR- VS Frequency'
        plt_cfg1['ylabel'] = r'$PSRR-$ [dB]'        
    
# plot the 1/amplitude_vout vs the frequency
    fig = plt.figure(figsize=(6,4))
    ax3 = fig.add_subplot(1, 1, 1)

    ax3.plot(scale_vec(freq, 1e6), scale_vec(oneOverVout_dB, 1), '-', linewidth=2)
    ax3.set_xscale('log') 
    
# label the plot
    label_plot(plt_cfg1, fig, ax3)
    
    return 'plot CMRR Frequency Response successfully!'

# -------------------------------------------------------------------
# plot Transient function
#-------------------------------------------------------------------
def plotTran(time_var, vout):    

# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Opamp Transient Output',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }

    
# plot the freq vs the frequency
    fig = plt.figure(figsize=(6,4))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(time_var, vout, '-', linewidth=2)
    ax1.set_xscale('linear') 

    
# label the plot
    label_plot(plt_cfg1, fig, ax1)
    
    return 'plot Tran successfully!'

# -------------------------------------------------------------------
# plot DC sweep function
#-------------------------------------------------------------------
def plotDC(sweep_var, vout_dc,  title='ICMR'):    

# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Opamp DC Output',
            'xlabel' : r'Input Voltage $V_{in}$ [V]',
            'ylabel' : r'Output Voltage $V_{out}$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }

    if title ==  'ICMR':
        plt_cfg1['title'] = r'Opamp DC Input Swing'
    elif title == 'OCMR':
        plt_cfg1['title'] = r'Opamp DC Output Swing'
    
# plot the freq vs the frequency
    fig = plt.figure(figsize=(6,4))
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(sweep_var, vout_dc, '-', linewidth=2)
    ax1.set_xscale('linear') 

    
# label the plot
    label_plot(plt_cfg1, fig, ax1)
    
    return 'plot DC successfully!'

# -------------------------------------------------------------------
# plot Schmitt Trigger function
#-------------------------------------------------------------------
def plotSchmittTrigger(time_var_in, vin, time_var_out, vout):    

# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Schmitt Trigger Output',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }

    
# plot the freq vs the frequency
    fig = plt.figure(figsize=(6,4))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(time_var_in, vin, '-', linewidth=2)
    ax1.plot(time_var_out, vout, '-', linewidth=2)
    ax1.set_xscale('linear') 
    
    
# label the plot
    label_plot(plt_cfg1, fig, ax1)
    
    return 'plot SchmittTrigger successfully!'


# -------------------------------------------------------------------
# plot dynamic comparator function
#-------------------------------------------------------------------
def plotDynamicComparatorOffset(time_var_clk, vclk_tran, \
                                time_var_inp, vinp_tran, time_var_inn,\
                                vinn_tran, time_var_outp, voutp_tran, \
                                time_var_outn, voutn_tran):    

# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Dynamic Comparator Offset: Input',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }

    plt_cfg2 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Dynamic Comparator Offset: Clock',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }
    
    plt_cfg3 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Dynamic Comparator Offset: Output positive',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }
    
    plt_cfg4 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Dynamic Comparator Offset: Output negat',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }
    
# plot the freq vs the frequency
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(4, 1, 1)
    ax1.plot(time_var_inp, vinp_tran, '-', linewidth=2)
    ax1.plot(time_var_inn, vinn_tran, '-', linewidth=2)
    ax1.set_xscale('linear') 
    
    ax2 = fig.add_subplot(4, 1, 2)
    ax2.plot(time_var_clk, vclk_tran, '-', linewidth=2)
    ax2.set_xscale('linear') 
    ax3 = fig.add_subplot(4, 1, 3)
    ax3.plot(time_var_outp, voutp_tran, '-', linewidth=2)
    ax3.set_xscale('linear') 
    ax4 = fig.add_subplot(4, 1, 4)
    ax4.plot(time_var_outn, voutn_tran, '-', linewidth=2)
    ax4.set_xscale('linear') 
# label the plot
    label_plot(plt_cfg1, fig, ax1)
    label_plot(plt_cfg2, fig, ax2)
    label_plot(plt_cfg3, fig, ax3)
    label_plot(plt_cfg4, fig, ax4)
    return 'plot Dynamic Comparator Offset successfully!'

def plotClockDelay(time_var_in, vin, time_var_out, vout):    
# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Delay Clock',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }
    
    plt_cfg2 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Delay Output',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }

    
# plot the freq vs the frequency
    fig = plt.figure(figsize=(9,6))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(time_var_in, vin, '-', linewidth=2)
    ax1.set_xscale('linear') 
    
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.plot(time_var_out, vout, '-', linewidth=2)
    ax2.set_xscale('linear') 
    
# label the plot
    label_plot(plt_cfg1, fig, ax1)
    label_plot(plt_cfg2, fig, ax2)
    return 'plot Clock Delay successfully!'





def plotComparatorOffset(time_var_inp, vinp_tran, time_var_inn,\
                         vinn_tran, time_var_out, vout_tran):    

# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Dynamic Comparator Offset: Input',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }

    
    plt_cfg3 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Dynamic Comparator Offset: Output positive',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$Voltage$ [V]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }
    

    
# plot the freq vs the frequency
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(2, 1, 1)
    ax1.plot(time_var_inp, vinp_tran, '-', linewidth=2)
    ax1.plot(time_var_inn, vinn_tran, '-', linewidth=2)
    ax1.set_xscale('linear') 
    
    ax3 = fig.add_subplot(2, 1, 2)
    ax3.plot(time_var_out, vout_tran, '-', linewidth=2)
    ax3.set_xscale('linear') 
# label the plot
    label_plot(plt_cfg1, fig, ax1)
    label_plot(plt_cfg3, fig, ax3)
    return 'plot Comparator Offset successfully!'


# -------------------------------------------------------------------
# plot power consumptionTransient function
#-------------------------------------------------------------------
def plotTranPower(time_var, i_vdd):    

# define the plot parameters
    plt_cfg1 = {
            'grid_linestyle' : 'dotted',
            'title' : r'Power Consumption Transient',
            'xlabel' : r'$Time$ [s]',
            'ylabel' : r'$I_vdd$ [A]',
            'legend_loc' : 'lower left',
            'add_legend' : False,
            'legend_title' : None
                }

    
# plot the freq vs the frequency
    fig = plt.figure(figsize=(6,4))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.plot(time_var, i_vdd, '-', linewidth=2)
    ax1.set_xscale('linear') 

    
# label the plot
    label_plot(plt_cfg1, fig, ax1)
    
    return 'plot Power Consumption Tran successfully!'