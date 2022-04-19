import numpy as np
import csv
import pandas as pd

# Constants
v_c = 220.e+3 # [m/sec] speed of solar system
v_E = v_c # [m/sec] speed of earth
c = 299792458. # [m/sec] speed of light from wikipedia
k_B = 1.380649e-23 # [J/K] boltzmann constant
rbw = 3.e+2 # [Hz]
binwidth = 2.e+3 # [Hz]
TLN2 = 77 # [K]

check_freq = np.array([18190, 18336, 19120, 19186, 19440, 19478, 19766, 19794, 19818, 20006, 20296, 20302, 20490, 20540, 20892, 21442, 21808, 22522, 22672, 23306, 23808, 23934, 25328, 25352, 25860, 26274, 26346])

def dat_to_array(path, doRebin=False, rebinmethod=0):
    f = open(path, "r")
    data = f.read().split("\n")[3:-1]
    freq = np.array([float(val.split(" ")[0]) for val in data])
    dBm = np.array([float(val.split(" ")[1]) for val in data])
    W = 10 ** (dBm / 10) / 1000
    f.close()

    Werr = None
    if doRebin:
        freq, W, Werr = rebin_func_consider_rbw(
                    freq, W, rebin=binwidth, rbw=rbw, method=rebinmethod, verbose=0)
        pass

    return freq, W, Werr

def csv_to_array(path):
    result = {}
    df = pd.read_csv(path)
    for col in df.columns:
        result[str(col)] =  np.array(df[col])
    
    return result



def cut_data(x, y, yerr=None):
    freq = []
    W = []
    Werr = []
    for i, (a, b) in enumerate(zip(x, y)):
        if a >= x[0] + 250.e+3 and a < x[0] + 250.e+3 + 2.e+6:
            freq.append(a)
            W.append(b)
            if yerr is not None:
                Werr.append(yerr[i])
                pass
            pass
        pass
        
    return np.array(freq), np.array(W), np.array(Werr)

def yfactor_analysis(freq, Wamb, WLN2, Wamb_err, WLN2_err, Tamb, rbw=rbw):
    # ２点を通る直線　y = ax + b
    a = (Wamb - WLN2) / (Tamb - TLN2)
    b = Wamb - a * Tamb
    a_err = ((Wamb_err**2 + WLN2_err**2)/(Tamb - TLN2)**2)**0.5
    b_err = (Wamb_err**2 + (a_err*Tamb)**2)**0.5
    #print_list(a, 'a')
    #print_list(b, 'b')
    #print_list(a_err, 'a_err')
    #print_list(b_err, 'b_err')

    gain = a/k_B/rbw
    Trx = b/a
    gain_err = a_err/k_B/rbw
    Trx_err = ((b_err/a)**2 + (b*a_err/a**2)**2)**0.5

    return gain, Trx, gain_err, Trx_err

def rebin_func(freq, data):
    rebin = 2000 # [Hz]
    rebin_freq = []
    rebin_data = []
    rebin_data_std = []
    freq_0 = freq[0]
    save_data = []
    save_freq = []
    for x, y in zip(freq, data):
        if x < freq_0 + rebin:
            save_data.append(y)
            save_freq.append(x)
        else:
            rebin_data.append(np.mean(np.array(save_data)))
            rebin_freq.append(np.mean(np.array(save_freq)))
            rebin_data_std.append(np.std(np.array(save_data))/len(save_data)**0.5)
            freq_0 += rebin
            save_data = [y]
            save_freq = [x]

    return np.array(rebin_freq), np.array(rebin_data), np.array(rebin_data_std)

def print_list(var, varname=''):
    print(f'{varname} (size={len(var)}) = {var}')

def rebin_func_consider_rbw(freq, data, rebin=binwidth, rbw=rbw, method=0, verbose=0):
    '''
        freq: original freq array [Hz]
        data: original power array [W]
        rebin: rebinning width [Hz] = 2000 Hz
        rbw: RBW of taken data [Hz] = 300 Hz
        verbose: verbosity level (int)
    '''
    rebin_freq = []
    rebin_data = []
    rebin_data_err = []

    freq = np.array(freq)
    freq1 = np.array(freq - rbw/2.) # lower edge of each data
    freq2 = np.array(freq + rbw/2.) # upper edge of each data
    data = np.array(data)
    if verbose > 0:
        print(f'freq  = {freq}')
        print(f'freq1 = {freq1}')
        print(f'freq2 = {freq2}')
        print(f'dfreq = {freq2-freq1}')
        print(f'data = {data}')
        pass

    # Create rebinned freq
    rebin_freq = np.arange(freq[0]+rebin/2, freq[-1]+rebin/2, rebin)
    if verbose > 0: print_list(rebin_freq, 'rebin_freq')

    # Loop over new freq
    for i, rebin_x in enumerate(rebin_freq):
        rebin_x1 = rebin_x - rebin/2. # lower edeg
        rebin_x2 = rebin_x + rebin/2. # upper edge

        if   method == 0: 
            in_range = np.where((freq2 > rebin_x1) & (freq1 < rebin_x2)) # Check lower edge and upper edeg
        elif method == 1:
            in_range = np.where((freq >= rebin_x1) & (freq < rebin_x2)) # Check lower edge and upper edeg
            pass
        if verbose > 0: print_list(in_range, 'in_range')

        # Retrieve original data in the range
        x = freq[in_range]
        x1 = freq1[in_range]
        x2 = freq2[in_range]
        y = data[in_range]
        n = len(x)
        width = x[1]-x[0]
        if verbose > 0: print_list(x, 'x')

        # Weight considering width in range
        weight = np.full(n, 1.)
        if method == 0:
            # Considering lower edge
            weight[0] = (x2[0] - rebin_x1)/rbw
            # Considering upper edge
            weight[-1] = (rebin_x2 - x1[-1])/rbw
            pass
        
        total_y = np.sum(y*weight)
        total_weight = np.sum(weight)
        total_width = total_weight *rbw
        _rebin_data = total_y * rebin/total_width
        rebin_data.append( _rebin_data )
        rebin_data_err.append( np.sqrt( np.sum( np.power(y*rebin/rbw - _rebin_data, 2.)*weight )/total_weight ) )
        pass

    return np.array(rebin_freq), np.array(rebin_data), np.array(rebin_data_err)


def get_file_freq(freq0, verbose=0):
    '''
    Arguments:
        freq0: frequency to be used in analysis [Hz]
    
    Return:
        start_str, start_100MHz_str, is_add_data

        start_str: GHz frequency string for 2MHz span file name [ex. 17.999750]
        start_100MHz_str: GHz frequency string for 100MHz span file name [ex. 19.1]
        is_add_data: if this frequency is in additional data or not
    '''
    freq0_MHz = freq0*1e-6
    
    # additional data [MHz]
    check_freq = np.array(
        [18190, 18336, 19120, 19186, 19440, 19478, 19766, 19794, 19818, 20006, 
         20296, 20302, 20490, 20540, 20892, 21442, 21808, 22522, 22672, 23306, 
         23808, 23934, 25328, 25352, 25860, 26274, 26346])
    
    is_add_data = False
    for _check_freq in check_freq:
        # Check if freq0 is in 2MHz measured data span in additional datas
        if _check_freq <= freq0_MHz and freq0_MHz < _check_freq + 2.:
            is_add_data = True
            pass
        pass
    if verbose>0: 
        print('This frequency has an additional data? -->', is_add_data)
        pass 
    
    # Get start freq of 100MHz span
    start_100MHz = (freq0//100e+6)*100 # MHz (100MHz 毎にする)
    start_100MHz *= 1e-3 # GHz
    start_100MHz = round(start_100MHz, 6) # GHz で小数点以下6桁(kHz)までにする
    start_100MHz_str = f'{start_100MHz:.1f}'
    if verbose>0: print(f'start_100MHz = {start_100MHz} GHz')
    
    # Get start freq of 2MHz span
    start_2MHz = (freq0//2e+6)*2 # MHz (2MHz 毎にする)
    start_2MHz *= 1e-3 # GHz
    start_2MHz = round(start_2MHz, 6) # GHz で小数点以下6桁(kHz)までにする
    if verbose>0: print(f'start_2MHz = {start_2MHz} GHz')
    
    # Get start freq of data span (start_2MHz - 0.25 MHz)
    start = start_2MHz - 0.00025
    start = round(start, 6) # GHz で小数点以下6桁(kHz)までにする
    start_str = f'{start:.06f}'
    if verbose>0: print(f'start_str = {start_str}')

    return start_str, start_100MHz_str, is_add_data


def any_rebin_func(freq, data, rebin):
    rebin_freq = []
    rebin_data = []
    rebin_data_std = []
    freq_0 = freq[0]
    save_data = []
    save_freq = []
    for x, y in zip(freq, data):
        if x < freq_0 + rebin:
            save_data.append(y)
            save_freq.append(x)
        else:
            rebin_data.append(np.mean(np.array(save_data)))
            rebin_freq.append(np.mean(np.array(save_freq)))
            rebin_data_std.append(np.std(np.array(save_data))/len(save_data)**0.5)
            freq_0 += rebin
            save_data = [y]
            save_freq = [x]

    return np.array(rebin_freq), np.array(rebin_data), np.array(rebin_data_std)


