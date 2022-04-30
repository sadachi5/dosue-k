import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os
import lmfit
from scipy import special
import function as func
import fit_script as fit


# freq0: Hz 
def fit_one(freq0, dfreq_0=0, rebinfunc=0, outdir='', outfile='', verbose=1,
           input_dir="/data/ms2840a/result_data", init_value_set = 0
           ):
    '''
        outdir = '' or outfile = '' # No save
    '''
    if outdir == '' or outfile == '':
        path = ''
    else:
        path = f'{outdir}/{outfile}'
        outdir_add = f'{outdir}/after_add'
        path_add = f'{outdir_add}/{outfile}'
        if not os.path.isdir(outdir_add):
            os.makedirs(outdir_add)
        #path_add = f'{outdir}/before_add/{outfile}'
        #if not os.path.isdir(outdir+'/before_add'):
        #    os.makedirs(f'{outdir}/before_add')
        pass
    
    print(f'*** Fit at frequency = {freq0*1.e-9} GHz ***')
    n_data = 12 # number of measurements
    data_time = 2. # [sec] time for nominal data
    data_time2 = 20. # [sec] time for additional data
    freq0_MHz = freq0*1e-6
    
    # additional data [MHz]
    check_freq = func.check_freq
    
    is_add_data = False
    for _check_freq in check_freq:
        # Check if freq0 is in 2MHz measured data span in additional datas
        if _check_freq <= freq0_MHz and freq0_MHz < _check_freq + 2.:
            is_add_data = True
            pass
        pass
    if verbose>0: print('This frequency has an additional data? -->', is_add_data)
    
    
    # Get start freq of 100MHz span
    start_100MHz = (freq0_MHz//100)*100 # MHz (100MHz 毎にする)
    start_100MHz *= 1e-3 # GHz
    start_100MHz = round(start_100MHz, 6) # GHz で小数点以下6桁(kHz)までにする
    if verbose>0: print(f'start_100MHz = {start_100MHz} GHz')
    
    # Get start freq of 2MHz span
    start_2MHz = (freq0_MHz//2)*2 # MHz (2MHz 毎にする)
    start_2MHz *= 1e-3 # GHz
    start_2MHz = round(start_2MHz, 6) # GHz で小数点以下6桁(kHz)までにする
    if verbose>0: print(f'start_2MHz = {start_2MHz} GHz')
    
    # Get start freq of data span (start_2MHz - 0.25 MHz)
    start = start_2MHz - 0.00025
    start = round(start, 6) # GHz で小数点以下6桁(kHz)までにする
    start_str = f'{start:.06f}'
    if verbose>0: 
        print(f'start     = {start}')
        print(f'start_str = {start_str}')
        pass

    signal = func.csv_to_array(f"{input_dir}/signal_12_data/start_{start_str}GHz.csv")
    freq = signal['freq']
    keys_W = [ f'W_{i}' for i in range(n_data) ]
    W_array = np.array([ signal[key] for key in keys_W ])
    W = np.average(W_array, axis=0) # mean of (W_0, W_1,... W_{n_data})
    if verbose > 0:
        print(f'data keys = {signal.keys()}')
        print(f'power keys = {keys_W}')
        print(f'freq (size={len(freq)}) = ',freq)
        print(f'W (nominal data, size={len(W)}) = ',W)
        pass

    # Add the additional data
    W_add = W
    if is_add_data:
        signal2 = func.csv_to_array(f"{input_dir}/check_result/signal_12_data/start_{start_str}GHz.csv")
        freq2 = signal2['freq']
        W2_array = np.array([ signal2[key] for key in keys_W ])
        W2 = np.average(W2_array, axis=0) # mean of (W_0, W_1,... W_{n_data})
        if verbose > 0: print(f'additional data keys = {signal.keys()}')
        print('W2 (additional data) = ', W2)
        
        # W2 is averaged 10 times more than W (W2 measurement time is 10 times more than W.)
        W_add = (W*data_time+W2*data_time2)/(data_time+data_time2)
        
        # Rebinning to 2kHz bins: W_add (nominal data + additional data)
        if   rebinfunc == 0: freq_rebin_add, W_rebin_add, W_rebin_err_add = func.rebin_func(freq2, W_add)
        elif rebinfunc == 1: freq_rebin_add, W_rebin_add, tmp = func.rebin_func_consider_rbw(freq2, W_add, method=0)
        elif rebinfunc == 2: freq_rebin_add, W_rebin_add = freq2, W_add
        elif rebinfunc == 3: freq_rebin_add, W_rebin_add, tmp = func.rebin_func_consider_rbw(freq2, W_add, method=1)
        else               : freq_rebin_add, W_rebin_add = freq2, W_add
        pass
    
    # Rebinning to 2kHz bins: W (nominal data)
    if   rebinfunc == 0: freq_rebin, W_rebin, W_rebin_err = func.rebin_func(freq, W)
    elif rebinfunc == 1: freq_rebin, W_rebin, tmp = func.rebin_func_consider_rbw(freq, W, method=0)
    elif rebinfunc == 2: freq_rebin, W_rebin = freq, W
    elif rebinfunc == 3: freq_rebin, W_rebin, tmp = func.rebin_func_consider_rbw(freq, W, method=1)
    else               : freq_rebin, W_rebin = freq, W
    if verbose > 0:
        print(f'freq_rebin (size:{len(freq_rebin)} = {freq_rebin}')
        print(f'W_rebin (size:{len(W_rebin)} = {W_rebin}')
        pass
    
    # Set initial values for fit
    if init_value_set == 1 or init_value_set == 2:
        init_values = [0., np.mean(W_rebin), 0.]
        if is_add_data:
            init_values_add = [0., np.mean(W_rebin_add), 0.]
            pass
    elif init_value_set == 3:
        init_values = None
        init_values_add = None
    else:
        init_values = [1., 1., 1.]
        init_values_add = [1., 1., 1.]
        pass
    
    # Fit with nominal data (before adding data)
    if verbose > 0:
        print('fit nominal data')
        pass
    result_list = fit.fitting(path, start=start, start_freq=start_100MHz, freq=freq_rebin, signal=W_rebin, dfreq_0=dfreq_0, verbose=verbose, init_values=init_values)
    # Check if there is NaN P_err (init_value_set == 2)
    if init_value_set == 2:
        result_P_err = np.array(result_list['P_err'])
        if verbose > 0:
            print(result_P_err)
            print(type(result_P_err))
            pass
        if func.isNoneAny_array(result_P_err) or np.any(np.isnan(result_P_err)):
            init_values = [1.,1.,1.]
            print(f'WARNING! The fitting results have NaN P_err!')
            print(f'WARNING! --> fit with a different initial value set ({init_values})')
            result_list = fit.fitting(path, start=start, start_freq=start_100MHz, freq=freq_rebin, signal=W_rebin, dfreq_0=dfreq_0, verbose=verbose, init_values=init_values)
            result_P_err = np.array(result_list['P_err'])
            print(f'retry P_err = {result_P_err}')
            isnan = np.nan(result_P_err)
            print(f'isnan = {isnan}')
            n_nan = np.sum(isnan)
            print(f'    # of nan in new fitting results = {n_nan}')
            pass
        pass
    
    # Fit with additional data for add_data
    if is_add_data:
        if verbose > 0:
            print('fit additional data')
            pass
        result_list_add = fit.fitting(path_add, start=start, start_freq=start_100MHz, freq=freq_rebin_add, signal=W_rebin_add, dfreq_0=dfreq_0, verbose=verbose, init_values=init_values_add)
        # Check if there is NaN P_err (init_value_set == 2)
        if init_value_set == 2:
            result_P_err_add = result_list_add['P_err']
            if func.isNoneAny_array(result_P_err_add) or np.any(np.isnan(result_P_err_add)):
                init_values_add = [1.,1.,1.]
                print(f'WARNING! The fitting results (add_data) have NaN P_err!')
                print(f'WARNING! --> fit with a different initial value set ({init_values_add})')
                result_list_add = fit.fitting(path_add, start=start, start_freq=start_100MHz, freq=freq_rebin_add, signal=W_rebin_add, dfreq_0=dfreq_0, verbose=verbose, init_values=init_values_add)
                result_P_err_add = np.array(result_list_add['P_err'])
                print(f'retry P_err = {result_P_err_add}')
                isnan_add = np.nan(result_P_err_add)
                print(f'isnan = {isnan_add}')
                n_nan_add = np.sum(isnan_add)
                print(f'    # of nan in new fitting results = {n_nan_add}')
                pass
            pass
        pass
        
    freq_0 = np.array(result_list['freq_0'])
    if verbose > 0:
        print(f'result keys = {result_list.keys()}')
        print(f'result freq_0 size:{len(freq_0)}')
        pass
    
    return result_list


if __name__=='__main__':
    init_value_set = 0 # 0=[1,1,1], 1=[0, mean(P), 0], 2=0 or 1, 3=3 times fit
    # Fit with a rebinned Pin
    # rebinned here before fit
    #input_dir = '/data/ms2840a/result_data'
    #outdatadir = './output/result_data/fit_result_newrebin'
    #rebinfunc = 1 # rebin here
    
    # Fit with a rebinned raw data (rebin method=0)
    # rebinned at raw data in get_original_signal
    #input_dir = './output/result_data_newrebin'
    #outdatadir = './output/result_data_newrebin/fit_result'
    #rebinfunc = 2 # No rebin
    
    # Fit with a rebinned (rebin method=1) raw data
    # rebinned at raw data in get_original_signal
    #input_dir = './output/result_data_newrebin1'
    #outdatadir = './output/result_data_newrebin1/fit_result'
    #rebinfunc = 2 # No rebin
    
    # Fit with a rebinned (rebin method=1) raw data
    # rebinned at raw data in get_original_signal
    # Initial value set in fit is #1
    #input_dir = './output/result_data_newrebin1'
    #init_value_set = 1
    #outdatadir = './output/result_data_newrebin1/fit_result2'
    #rebinfunc = 2 # No rebin
    
    # Fit with a rebinned (rebin method=1) raw data
    # rebinned at raw data in get_original_signal
    # Initial value set in fit is #2 (choose 1 of 2 sets) --> Failed in fit
    #input_dir = './output/result_data_newrebin1'
    #init_value_set = 2
    #outdatadir = './output/result_data_newrebin1/fit_result3'
    #rebinfunc = 2 # No rebin

    # Fit with a rebinned (rebin method=1) raw data
    # rebinned at raw data in get_original_signal
    # Initial values are optimized by using 3 times fits in func.fitting()
    #input_dir = './output/result_data_newrebin1'
    #init_value_set = 3
    #outdatadir = './output/result_data_newrebin1/fit_result4'
    #rebinfunc = 2 # No rebin

    # Fit with a rebinned (rebin method=1) data
    # rebinned at raw data in get_original_signal 
    # by using old y-factor results
    # Initial value set in fit is #2 (choose 1 of 2 sets)
    input_dir = './output/result_data_newrebin2'
    init_value_set = 3 # 3 times fit
    outdatadir = './output/result_data_newrebin2/fit_result'
    rebinfunc = 3 # rebin here by using rebin method=1


    freq_min = 18. # GHz
    freq_max = 26.5 # GHz

    if len(sys.argv) > 1:
        freq_min = float(sys.argv[1])
        pass
    if len(sys.argv) > 2:
        freq_max = float(sys.argv[2])
        pass
    
    if not os.path.isdir(outdatadir):
        os.makedirs(outdatadir)
        pass
    
    # start frequencies with 100MHz steps
    fmin = int(freq_min*10)
    fmax = int(freq_max*10)
    if fmin < 180: fmin = 180
    if fmax > 265: fmax = 265
    for i in range(fmin, fmax, 1):
        print(f'freq = {i*0.1} GHz')
        start_freq = i/10
        initial = int(start_freq * 1.e+6 - 250)
        final = int(initial + 1.e+5)
        for j in range(initial, final, 2000):
            word = list(str(j))
            word.insert(2, ".")
            start = "".join(word)
            start_Hz = (float)(start)*1e+9
            outfile = f'start_{start}GHz.csv'
            # Save
            fit_one(start_Hz+1e+6, rebinfunc=rebinfunc, init_value_set=init_value_set, 
                    outdir=outdatadir, outfile=outfile, verbose=0, input_dir=input_dir)
            # No Save
            #fit_one(start_Hz+1e+6, rebinfunc=rebinfunc, init_value_set=init_value_set, 
            #         outdir='', outfile='', verbose=1, input_dir=input_dir)
            pass
        pass 
