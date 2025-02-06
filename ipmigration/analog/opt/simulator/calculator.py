# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:31:12 2023

@author: shunqidai
add SchmittTriggerResult 27/08/2024
"""

import numpy as np
import scipy
import matplotlib.pyplot as plt

#------------------------

def find_x0_for_y0(x_var, y_var, y0, plot_flag=0):
    """
    Calculate x0 when y_var equal to y0

    Attributes
    ----------
    x_var : 1-D ndarray
        Frequency points in Hz
    y_var : 1-D ndarray
    initialGuess : float or int
        Initial guess `x0` for the root finder.
    y0 is firstly interpolated and then sent to a root finder.
    """
    
    x=x_var
    y=y_var-y0
    x=np.array(x)
    y=np.array(y)
    #print("x:", x)
    #print("y:", y)
    # 找到y值符号变化的位置
    ## np.sign() 如果数组值大于0则返回1，如果数组值小于0则返回-1，如果数组值为0则返回0
    ## np.diff() 差分
    sign_changes = np.where(np.diff(np.sign(y)))[0]  # eg: array([ 28, 185, 342, 499, 656, 813, 970], dtype=int64)
    sign_changes_up = sign_changes+1
    #print("sign_changes:", sign_changes)
    #print("sign_changes_up:", sign_changes_up)
    # 过零点的x坐标
    sign_changes_x = x[sign_changes] # array([-9.43943944, -6.2962963 , -3.15315315, -0.01001001,  3.13313313, 6.27627628,  9.41941942])
    sign_changes_y = y[sign_changes]
    #print("sign_changes_x:", sign_changes_x)
    #print("sign_changes_y:", sign_changes_y)
    # 由于过零点可能不会精确落在采样点上，我们可以通过线性插值来估计过零点的精确位置
    zero_crossings_x = []
    for i in sign_changes:
        # 线性插值
        zero_crossing= x[i] - y[i]/((y[i+1] - y[i]) / (x[i+1] - x[i]) )
        zero_crossings_x.append(zero_crossing)

    zero_crossings_y= np.zeros(len(zero_crossings_x))
    # 打印结果
    #print("过零点的x坐标:", zero_crossings_x)
    #print("过零点的y坐标 (应接近0):", zero_crossings_y)

    # 绘制曲线和过零点
    if plot_flag>0:
        plt.plot(x, y, label='Curve')
        plt.scatter(zero_crossings_x, zero_crossings_y, color='red', label='Zero Crossings')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.legend()
        plt.show()
    return zero_crossings_x

#--------------------------


# ---------------------------
# Specification calculation functions
# --------------------------

def dcGain_dB(freq_var, frequencyResponse):
    """
    freq_var: in Hz,  frequencyResponse: complex list
    Calculate the gain at 1 Hz, return as real number in dB
    """
    try:
        dc_gain = 20.0*np.log10(np.abs(np.interp(1.0, freq_var, frequencyResponse)))
        return float(dc_gain)    
    except:
        raise ValueError("cannot calculate the DC gain because the data does not contain gain at 1 Hz.")


def dcGain(freq_var, frequencyResponse):
    """
    freq_var: in Hz,  frequencyResponse: complex list
    Calculate the gain at 1 Hz, return as real number
    """
    try:
        dc_gain = np.abs(np.interp(1.0, freq_var, frequencyResponse))
        return float(dc_gain)    
    except:
        raise ValueError("cannot calculate the DC gain because the data does not contain gain at 1 Hz.")



def unityGainFrequency(freq_var, frequencyResponse):
    """
    Calculate the frequency when dcgain drops to 1.

    Attributes
    ----------

    freq_var : 1-D ndarray
        Frequency points in Hz
    frequencyResponse : 1-D ndarray
        Frequency response points, given as an array of complex numbers
    initialGuess : float or int
        Initial guess `x0` for the root finder.
    Frequency response is firstly interpolated and then sent to a root finder.
    """
    amplitudeResponse = np.abs(frequencyResponse)
    try:
        firstBelowUnityIndex = np.min(np.where(amplitudeResponse < 1))
        initialGuess = freq_var[firstBelowUnityIndex - 1]
        return scipy.optimize.root(lambda x: np.interp(x,
                                                       freq_var[firstBelowUnityIndex -
                                                                          1: firstBelowUnityIndex + 1],
                                                       amplitudeResponse[firstBelowUnityIndex -
                                                                         1: firstBelowUnityIndex + 1],
                                                       left=np.nan, right=np.nan) - 1, initialGuess).x[0]
    except:
        return 0.0
#        return -np.inf
#        raise ValueError("impossible to calculate the unity gain frequency, because the data contains no amplitude point that is less than or equals 1. Try simulating with wider frequency range, or this circuit does not reach unity gain at all.")


def bandwidth3dB(freq_var, frequencyResponse):
    """Calculate the frequency at which amplitude response drops to 1 / sqrt(2) of its value at 1 Hz.

    Attributes
    ----------

    freq_var : 1-D ndarray
        Frequency points in Hz
    frequencyResponse : 1-D ndarray
        Frequency response points, given as an array of complex numbers
    initialGuess : float or int
        Initial guess `x0` for the root finder. 
    Frequency response is firstly interpolated and then sent to a root finder.
    """
    amplitudeResponse = np.abs(frequencyResponse)
    amplitudeAt1Hz = np.interp(1, freq_var, amplitudeResponse, left=np.nan, right=np.nan) 
    amplitudeAtBandwidth = amplitudeAt1Hz / np.sqrt(2)
    try:
        firstOutsideBandwidthFrequency = np.min(np.where(amplitudeResponse < amplitudeAtBandwidth))
        slicedFrequencies = freq_var[firstOutsideBandwidthFrequency - 1: firstOutsideBandwidthFrequency + 1]
        slicedAmplitudeResponse = amplitudeResponse[firstOutsideBandwidthFrequency - 1: firstOutsideBandwidthFrequency + 1]
        initialGuess = freq_var[firstOutsideBandwidthFrequency - 1]
        return scipy.optimize.root(
            lambda x: np.interp(
                x,
                slicedFrequencies,
                slicedAmplitudeResponse,
                left=np.nan,
                right=np.nan
            ) - amplitudeAtBandwidth,
            initialGuess
        ).x[0]
    except:
        return 0.0
#        raise ValueError("impossible to calculate bandwidth, because the data contains no amplitude point that is below 1 / sqrt(2) times the amplitude at 1 Hz. Try simulating with wider frequency range, or this circuit does not have a bandwidth at all. Amplitude at 1 Hz is {}. Amplitude at {} Hz is {}".format(amplitudeAt1Hz, frequenciesInHertz[-1], amplitudeResponse[-1]))


def phaseMargin(freq_var, frequencyResponse):
    """
    freq_var: in Hz,  frequencyResponse: complex list
    Calculate the phase margin in degree
    """
    phaseResponse =  np.angle(np.array(frequencyResponse), deg=True)
    ugf = unityGainFrequency(freq_var, frequencyResponse)
    while np.sum(phaseResponse>0.0):
        phaseResponse[np.where(phaseResponse > 0.0)] -= 360.0
    try:
        phaseAtUnityGain = np.interp(ugf, freq_var, phaseResponse)
        pm = phaseAtUnityGain + 180.0
        return float(pm)
    except:
        raise ValueError("impossible to calculate the phase margin, either because this circuit never reaches unity gain (which means PM makes no sense) or your simulation data is insufficient. Try simulating with wider frequency range.")

def gainMargin(freq_var, frequencyResponse):
    """
    freq_var: in Hz,  frequencyResponse: complex list
    Calculate the gain margin in dB
    """
    amplitudeResponse = np.abs(frequencyResponse)
    phaseResponse =  np.angle(np.array(frequencyResponse), deg=True)
    try:
        firstIndexPhaseAtNegative180 = np.min(np.where(phaseResponse <= -179))
        slicedFrequencies = freq_var[firstIndexPhaseAtNegative180 - 1: firstIndexPhaseAtNegative180 + 1]
        slicedPhaseResponse = phaseResponse[firstIndexPhaseAtNegative180 - 1: firstIndexPhaseAtNegative180 + 1]
        initialGuess = freq_var[firstIndexPhaseAtNegative180 - 1]
        phaseCrossPoint = scipy.optimize.root(
                                              lambda x: np.interp(
                                                                  x,
                                                                  slicedFrequencies,
                                                                  slicedPhaseResponse,
                                                                  left=np.nan,
                                                                  right=np.nan
                                                                  ) + 180,
                                              initialGuess
                                              ).x[0]
        gainAtNegative180 = np.interp(phaseCrossPoint, freq_var, amplitudeResponse)
        gainMargin = 20*np.log10(1/gainAtNegative180)
        return gainMargin
    except:
        raise ValueError("impossible to calculate the gain margin, either because this circuit never reaches unity gain (which means PM makes no sense) or your simulation data is insufficient. Try simulating with wider frequency range.")

def CMRR_dB(freq_var, frequencyResponse):
    """
    freq_var: in Hz,  frequencyResponse: complex list
    Calculate the 1 / Amplitude Response at 1 kHz, return as real number in dB
    """
    amplitudeResponse = np.abs(frequencyResponse)
    try:
        oneOverVout = 1/np.abs(np.interp(1000, freq_var, amplitudeResponse))
        cmrr = 20*np.log10(oneOverVout)
        return cmrr    
    except:
        return 0.0
        #raise ValueError("cannot calculate the CMRR because the data does not contain gain at 1 Hz.")

def CMRR(freq_var, frequencyResponse):
    """
    freq_var: in Hz,  frequencyResponse: complex list
    Calculate the 1 / Amplitude Response at 1 kHz, return as real number in dB
    """
    amplitudeResponse = np.abs(frequencyResponse)
    try:
        oneOverVout = 1/np.abs(np.interp(1000, freq_var, amplitudeResponse))
        cmrr = oneOverVout
        return cmrr    
    except:
        return 0.0
        #raise ValueError("cannot calculate the CMRR because the data does not contain gain at 1 Hz.")

def slewRate(time_var, wave):
    """Calculate the slew rate 
    time_var: in second
    wave: in voltage
    Notes
    -------------------------------------------
    old method: 
    SR = \max\left|{dV_o \over dt}\right|
    
    new method:
    same as cadence calculator
    -------------------------------------------------
    """
    initialValue = np.min(wave)
    finalValue = np.max(wave)
    precentHigh = 0.6*(finalValue-initialValue)+initialValue
    precentLow = 0.1*(finalValue-initialValue)+initialValue
    firstIndexPrecentHgih = np.min(np.where(wave >= precentHigh))
    firstIndexPrecentLow = np.min(np.where(wave >= precentLow))
    if time_var[firstIndexPrecentHgih] <= time_var[firstIndexPrecentLow]:
        return 0.0
    else:
        slewRateInVPerSecond = (precentHigh-precentLow) / (time_var[firstIndexPrecentHgih]-time_var[firstIndexPrecentLow])
        #return np.max(np.abs(np.diff(wave) / np.diff(time_var)))
        return float(slewRateInVPerSecond)


def slewRateNeg(time_var, wave):
    """Calculate the Negative slew rate 
    time_var: in second
    wave: in voltage
    Notes
    -------------------------------------------
    old method: 
    SR = \max\left|{dV_o \over dt}\right|
    
    new method:
    same as cadence calculator
    -------------------------------------------------
    """
    initialValue = np.max(wave)
    finalValue = np.min(wave)
    precentHigh = -0.1*(initialValue-finalValue)+initialValue
    precentLow = -0.6*(initialValue-finalValue)+initialValue
    firstIndexPrecentHgih = np.min(np.where(wave <= precentHigh))
    firstIndexPrecentLow = np.min(np.where(wave <= precentLow))
    if time_var[firstIndexPrecentHgih] >= time_var[firstIndexPrecentLow]:
        return 0.0
    else:
        slewRateNegInVPerSecond = (precentHigh-precentLow) / (time_var[firstIndexPrecentLow]-time_var[firstIndexPrecentHgih])
        #return np.max(np.abs(np.diff(wave) / np.diff(time_var)))
        return float(slewRateNegInVPerSecond)    
        

def ICMR(sweep_var, vout_dc):
    """
    sweep_var: in V,  vout_dc: 1-D list
    Calculate the ICMR [V]
    """
    diff_vout_dc_list = []
    try:
        for i in range(len(sweep_var)-1):
            diff_vout = (vout_dc[i+1] - vout_dc[i]) / (sweep_var[i+1] - sweep_var[i])
            diff_vout_dc_list.append(diff_vout)
            
        #print(diff_vout_dc_list)
        firstIndexSlopeOne = np.min(np.where(np.array(diff_vout_dc_list) > 0.96))
        lastIndexSlopeOne = np.max(np.where(np.array(diff_vout_dc_list) > 0.96))
        #print('firstIndexSlopeOne, lastIndexSlopeOne:', firstIndexSlopeOne, lastIndexSlopeOne)
        icmr = sweep_var[lastIndexSlopeOne] - sweep_var[firstIndexSlopeOne]
        return icmr    
    except:
        return 0.0
        #raise ValueError("cannot calculate the ICMR.")
        

def OCMR(sweep_var, vout_dc):
    """
    sweep_var: in V,  vout_dc: 1-D list
    Calculate the OCMR [V]
    ideal gain of the testbench is -10X
    """
    diff_vout_dc_list = []
    try:
        for i in range(len(sweep_var)-1):
            diff_vout = (vout_dc[i+1] - vout_dc[i]) / (sweep_var[i+1] - sweep_var[i])
            diff_vout_dc_list.append(diff_vout)
            
        #print(diff_vout_dc_list)
        firstIndexSlopeNeg10 = np.min(np.where(np.array(diff_vout_dc_list) <= -9))
        lastIndexSlopeNeg10 = np.max(np.where(np.array(diff_vout_dc_list) <= -9))
        #print('firstIndexSlopeNeg10, lastIndexSlopeNeg10:', firstIndexSlopeNeg10, lastIndexSlopeNeg10)
        ocmr = vout_dc[lastIndexSlopeNeg10] - vout_dc[firstIndexSlopeNeg10]
        return abs(ocmr)    
    except:
        return 0.0
        #raise ValueError("cannot calculate the OCMR.")
        
def PSRR(freq_var, frequencyResponse):
    """
    freq_var: in Hz,  frequencyResponse: complex list
    Calculate the 1/Amplitude Response at 1 kHz, return as real number in dB
    """
    amplitudeResponse = np.abs(frequencyResponse)
    try:
        oneOverVout = 1/np.abs(np.interp(1000, freq_var, amplitudeResponse))
        psrr = oneOverVout
        return psrr    
    except:
        return 0.0
        #raise ValueError("cannot calculate the PSRR because the data does not contain gain at 1 Hz.")



def SchmittTriggerResult(time_var_in, v_in, time_var_out, v_out):
    """
    return:
        v_hl: [V]
        v_lh: [V]
        window [mv]
    """
    vdd = np.max(v_in)
    half_vdd=0.5*vdd
    #print("time_var_in:", time_var_in)
    try:
        VHL_index = np.min(np.where(v_out >= half_vdd))
        time_vhl=time_var_out[VHL_index]
        #print("VHL_index:", VHL_index)
        #print("time_vhl:", time_vhl)
        VLH_index = np.max(np.where(v_out >= half_vdd))
        time_vlh=time_var_out[VLH_index]
        v_ih=np.interp(time_vhl, time_var_in, v_in)
        v_il=np.interp(time_vlh, time_var_in, v_in)
        window = (v_ih-v_il)*1000
        return v_ih, v_il, window    
    except:
        return np.NaN, np.NaN, np.NaN
        
def LevelShifterResult(time_var_in, v_in, time_var_out, v_out, i_vddl, i_vddh):
    """
    return:
        rise_time [sec], fall_time [sec], delay [sec], avg_total_power [W]
    """
    vddl = np.max(v_in)
    vddh = np.max(v_out)
    half_vddl=0.5*vddl
    half_vddh=0.5*vddh

    time_max=np.max(time_var_out)
    for i in range(len(time_var_out)):
        if i==0:
            power_vddl=0
            power_vddh=0
        else:
            time_interval=time_var_out[i]-time_var_out[i-1]
            tmp_power_vddl=abs(time_interval*i_vddl[i])
            tmp_power_vddh=abs(time_interval*i_vddh[i])
            power_vddl=power_vddl+tmp_power_vddl
            power_vddh=power_vddh+tmp_power_vddh
    power_vddl_avg=power_vddl/time_max
    power_vddh_avg=power_vddh/time_max
    avg_total_power=power_vddl_avg+power_vddh_avg
    #print("time_var_in:", time_var_in)
    try:
        vin_index = np.min(np.where(v_in >= half_vddl))
        time_in=time_var_in[vin_index]
        
        vout_index = np.min(np.where(v_out >= half_vddh))
        time_out=time_var_out[vout_index]
        
        delay=time_out-time_in
        
        vout_index_rise1 = np.min(np.where(v_out >= 0.1*vddh))
        vout_index_rise2 = np.min(np.where(v_out >= 0.9*vddh))
        rise_time=time_var_out[vout_index_rise2]-time_var_out[vout_index_rise1]
        
        vout_index_fall1 = np.max(np.where(v_out >= 0.9*vddh))
        vout_index_fall2 = np.max(np.where(v_out >= 0.1*vddh))
        fall_time=time_var_out[vout_index_fall2]-time_var_out[vout_index_fall1]
        return rise_time, fall_time, delay, avg_total_power    
    except:
        return np.NaN, np.NaN, np.NaN, np.NaN



########## For Comparator Result ###################
def ComparatorOffset(time_var_inp, v_inp, \
                     time_var_inn, v_inn, \
                     time_var_outp, v_outp, \
                     time_var_vdd, vdd_tran):
    """
    return:
        vos[mV]
    """
    vdd = np.max(vdd_tran)
    half_vdd=0.5*vdd
    try:
        voutp_index = np.min(np.where(v_outp >= half_vdd)[0])
        v_inp_value=v_inp[voutp_index]
        v_inn_value=v_inn[voutp_index]
        vos=abs((v_inp_value-v_inn_value))*1000
        return vos
    except:
        return np.NaN

def ComparatorDelay(time_var_in, v_in, time_var_out, v_out, time_var_vdd, vdd_tran):
    """
    return:
        delay [ns]
    """
    vdd = np.max(vdd_tran)
    half_vdd=0.5*vdd
    
    
    
    try:
        '''
        vin_index = np.where(v_in >= half_vdd)[0]
        time_var_in=np.array(time_var_in)
        time_in=time_var_in[vin_index]
            
        vout_index = np.where(v_out >= half_vdd)[0]
        time_var_out=np.array(time_var_out)
        time_out=time_var_out[vout_index]
        '''
        time_in=find_x0_for_y0(time_var_in, v_in, half_vdd)
        time_out=find_x0_for_y0(time_var_out, v_out, half_vdd)
        
        
        #rise delay
        time_in_rise=time_in[0]
        #print("time_in_rise", time_in_rise)
        time_out_rise=time_out[0]
        #print("time_out_rise", time_out_rise)    
        delay_rise=time_out_rise-time_in_rise
        #print("delay_rise_list", delay_rise)
        #number_rise=float(len(delay_rise))
        #delay_rise=np.sum(delay_rise)/number_rise
        delay_rise=delay_rise*1.0e9
        #print("delay_rise[ns]", delay_rise)
        
        #fall delay
        time_in_fall=time_in[-1]
        #print("time_in_fall", time_in_fall)
        time_out_fall=time_out[-1]
        #print("time_out_fall", time_out_fall)    
        delay_fall=time_out_fall-time_in_fall
        #print("delay_fall_list", delay_fall)
        #number_fall=float(len(delay_fall))
        #delay_fall=np.sum(delay_fall)/number_fall
        delay_fall=delay_fall*1.0e9
        #print("delay_fall[ns]", delay_fall)    
        delay=(delay_rise+delay_fall)*0.5
        return delay_rise, delay_fall
    except:
        return np.NaN, np.NaN

    

def RisetimeFalltime(time_var_out, v_out, time_var_vdd, vdd_tran):
    """
    ###################
    # need to modified
    ##################
    return:
        rise_time [ns], fall_time [ns]
    """
    vdd = np.max(vdd_tran)
    

    try:
        #vout_index_rise1 = np.where(v_out >= 0.1*vdd)[0]
        #vout_index_rise2 = np.where(v_out >= 0.9*vdd)[0]
        
        time_high=find_x0_for_y0(time_var_out, v_out, 0.9*vdd)
        time_low=find_x0_for_y0(time_var_out, v_out, 0.1*vdd)
        
        #t2=time_var_out[vout_index_rise2[0]]
        #t1=time_var_out[vout_index_rise1[0]]
        t2=time_high[0]
        t1=time_low[0]
        #print("t2, t1:", t2*1e9, t1*1e9)
        rise_time=(t2-t1)*1.0e9
        #print("rise time:", rise_time)
        
        #vout_index_fall1 = np.where(v_out >= 0.1*vdd)[0]
        #vout_index_fall2 = np.where(v_out >= 0.9*vdd)[0]
        
        #t3=time_var_out[np.max(vout_index_fall1)]
        #t4=time_var_out[np.max(vout_index_fall2)]
        t3=time_low[-1]
        t4=time_high[-1]
        #print("t4, t3:", t4*1e9, t3*1e9)
        fall_time=(t3-t4)*1.0e9
        #print("fall_time:", fall_time)
        return rise_time, fall_time
    except:
        return np.NaN, np.NaN


def VOHandVOL(time_var_out, v_out):
    """
    ###################
    # need to modified
    ##################
    return:
        voh [V], vol [V]
    """
    vout_max = np.max(v_out)
    vout_max_80_precent = vout_max*0.8

    try:
        vout_index = np.min(np.where(v_out >= vout_max_80_precent)[0])
        vout_tmp = v_out[vout_index:] # extract signal after start delay
        
        voh=np.max(vout_tmp)
        vol=np.min(vout_tmp)
        return voh, vol
    except:
        return np.NaN, np.NaN
    
    
def PowerAverage(time_var_vdd, i_dd):
    """
    ###################
    # need to modified
    ##################
    return:
        i_power_avg [A]
    """
    power_sum=0
    
    for j in range(1, len(time_var_vdd)):
        if j<(len(time_var_vdd)-1):
            dt=time_var_vdd[j]-time_var_vdd[j-1]
            delta_power=np.abs((i_dd[j]+i_dd[j-1]))*0.5*dt
            power_sum=power_sum+delta_power
    
    i_power_avg=power_sum/time_var_vdd[-1]
    return i_power_avg
    
'''
    try:

    except:
        return np.NaN, np.NaN
'''


def AnalogComparatorOffset(time_var_inp, v_inp, \
                     time_var_inn, v_inn, \
                     time_var_outp, v_outp, \
                     time_var_vdd, vdd_tran):
    """
    for trangle waveform testbench
    return:
        vos[mV]
    """
    vdd = np.max(vdd_tran)
    half_vdd=0.5*vdd
    try:
        # vos rising edge
        voutp_index_rise = np.min(np.where(v_outp >= half_vdd)[0])
        v_inp_value_rise=v_inp[voutp_index_rise]
        v_inn_value_rise=v_inn[voutp_index_rise]
        vos_rise=abs((v_inp_value_rise-v_inn_value_rise))*1000
        # vos falling edge
        voutp_index_fall = np.max(np.where(v_outp >= half_vdd)[0])
        v_inp_value_fall=v_inp[voutp_index_fall]
        v_inn_value_fall=v_inn[voutp_index_fall]
        vos_fall=abs((v_inp_value_fall-v_inn_value_fall))*1000
        print("vos_rise: {0}, vos_fall: {1}".format(vos_rise, vos_fall))
        return vos_rise
    except:
        return np.NaN