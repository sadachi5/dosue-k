#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import sys
import function as func


# Constants
v_c = 220.e+3 # [m/sec] speed of solar system
v_E = v_c # [m/sec] speed of earth
c = 299792458. # [m/sec] speed of light from wikipedia
k_B = 1.380649e-23 # [J/K] boltzmann constant
rbw = 3.e+2 # [Hz]
binwidth = 2.e+3 # [Hz]
TLN2 = 77 # [K]


# Get original signal ($P_\mathrm{in}$) (NEW IMPLEMENTATION)
def get_original_signal(start, yfactor, in_datadir, out_datadir, Pin_rbw, doRebin=False, rebinmethod=0, time_str='2.0'):
    Gain = 0
    Trx = 0
    Gain_err = 0
    Trx_err = 0
    for _f, freq in enumerate(yfactor["freq"]):
        if float(freq) * 1e+6 == float(start) * 1e+6:
            Gain = yfactor["Gain"][_f]
            Trx = yfactor["Trx"][_f]
            Gain_err = yfactor["Gain_err"][_f]
            Trx_err = yfactor["Trx_err"][_f]
            break

    W_twelve = []
    freq = np.array([])
    for j in range(12):
        path = f"{in_datadir}/scan_FFT_{start}GHz_span2.50MHz_rbw0.3kHz_{time_str}sec_1counts_12runs_{j}.dat"
        freq, W, tmp = func.dat_to_array(path, doRebin=doRebin, rebinmethod=rebinmethod)
        W_twelve.append(W/Gain - k_B*Trx*Pin_rbw)
        pass
    
    column = ["freq"] + ["W_{}".format(str(x)) for x in range(12)]
    outdir2 = f'{out_datadir}/signal_12_data'
    if not os.path.isdir(outdir2):
        os.makedirs(outdir2)
        pass
    with open(f"{outdir2}/start_{start}GHz.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(column)
        for j in range(len(freq)):
            writer.writerow([freq[j]] + [W_twelve[x][j] for x in range(12)])
            pass
        pass # End of opening output file
    
    return
        
def loop_get_original_signal_normaldata(
    in_yfactor="/data/ms2840a/result_data/yfactor_result_rebin2MHz.csv", 
    in_datadir="/data/ms2840a/signal_raw_data",
    out_datadir = "/data/ms2840a/result_data/",
    Pin_rbw = 300.,
    doRebin = False,
    rebinmethod = 0,
    freq_min = 18.0, # GHz
    freq_max = 26.5, # GHz
    verbose=1):
    
    yfactor = func.csv_to_array(in_yfactor)
    check_freq = func.check_freq

    
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
            print(start, start_Hz)
            get_original_signal(start=start, yfactor=yfactor, in_datadir=in_datadir, 
                                out_datadir=out_datadir, Pin_rbw=Pin_rbw, doRebin=doRebin, 
                                rebinmethod=rebinmethod, time_str='2.0')
            pass # End of loop over 2MHz steps
        
        pass # End of loop over 100MHz steps
    
    return
    
def loop_get_original_signal_checkdata(
    in_yfactor="/data/ms2840a/result_data/check_result/yfactor_check_result.csv", 
    in_datadir="/data/ms2840a/signal_data_check/2022-01-17/data",
    out_datadir = "/data/ms2840a/result_data/check_result",
    Pin_rbw = 300.,
    doRebin = False,
    rebinmethod = 0,
    verbose=1):
    
    yfactor = func.csv_to_array(in_yfactor)
    check_freq = func.check_freq

    for i in check_freq:
        word = list(str(i*1000 - 250))
        word.insert(2, ".")
        start = "".join(word)
        if verbose > 0: print(start)

        get_original_signal(start=start, yfactor=yfactor, in_datadir=in_datadir, 
                            out_datadir=out_datadir, Pin_rbw=Pin_rbw, doRebin=doRebin, 
                            rebinmethod=rebinmethod, time_str='20.0')
        pass # End of loop over check freqs
    
    return


if __name__ == '__main__':
    freq_min = 18. # GHz: Start freq of scan
    freq_max = 26.5  # GHz: End freq of scan
    doCheckData = False # if freq_min < 0., it will do only for check data.

    if len(sys.argv) > 1:
        freq_min = float(sys.argv[1])
        pass
    if len(sys.argv) > 2:
        freq_max = float(sys.argv[2])
        pass

    if freq_min < 0.:
        doCheckData = True
        pass
    
    # ## Old Implementation (No rebin)
    '''
    RBW=300.
    yfac_datadir="/data/ms2840a/result_data", 
    new_datadir="/data/ms2840a/signal_raw_data",
    rebinmethod = 2 # NOT affect on the result
    doRebin = False # rebin signal raw data
    '''
    
    # ## New implementation with rebinned raw data (rebinmethod=0)
    '''
    RBW=2.e+3
    yfac_datadir = './output/result_data_newrebin'
    new_datadir = './output/result_data_newrebin'
    rebinmethod = 0
    doRebin = True # rebin signal raw data
    '''
    
    # ## New implementation with rebinned raw data (rebinmethod=1)
    '''
    RBW=2.e+3
    yfac_datadir = './output/result_data_newrebin1'
    new_datadir = './output/result_data_newrebin1'
    rebinmethod = 1
    doRebin = True # rebin signal raw data
    '''
    
    # ## New implementation with original y-factor (rebinmethod=1)
    # Not rebin here. Rebinning is performed right before fitting on P_in
    RBW=300.
    yfac_datadir = '/data/ms2840a/result_data'
    new_datadir = './output/result_data_newrebin2'
    rebinmethod = 1 # NOT USED due to doRebin=False
    doRebin = False # rebin signal raw data
    
    if doCheckData:
        loop_get_original_signal_checkdata(
            in_yfactor=f"{yfac_datadir}/check_result/yfactor_check_result.csv", 
            in_datadir="/data/ms2840a/signal_data_check/2022-01-17/data",
            out_datadir=f"{new_datadir}/check_result",
            Pin_rbw=RBW, doRebin=doRebin, rebinmethod=rebinmethod)
    else:
        loop_get_original_signal_normaldata(
            in_yfactor=f"{yfac_datadir}/yfactor_result_rebin2MHz.csv", 
            in_datadir="/data/ms2840a/signal_raw_data",
            out_datadir=f"{new_datadir}/",
            Pin_rbw=RBW, doRebin=doRebin, rebinmethod=rebinmethod,
            freq_min=freq_min, freq_max=freq_max)
        pass
        
    pass
