import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
import os
import lmfit
from scipy import special
import function as func
import fit_script as fit

from peak_search import fit_one

if __name__=='__main__':
    init_value_set = 0
    # No save
    outdir = '.'
    outfile=''

    # Fit with a rebinned (rebin method=1) raw data
    # rebinned at raw data in get_original_signal
    # Initial value set in fit is #2 (choose 1 of 2 sets)
    input_dir = './output/result_data_newrebin1'
    init_value_set = 3
    rebinfunc = 2 # No rebin

    freq0 = 18.0
    if len(sys.argv) > 1:
        freq0 = float(sys.argv[1]) # GHz
        pass
    freq0_Hz = (int)(freq0*1e+9)
    print(f'freq0_Hz = {freq0_Hz}')

    start_str, start100MHz_str, is_add_data = func.get_file_freq(freq0*1e+9)
    result_list = fit_one(freq0_Hz, rebinfunc=rebinfunc, init_value_set=init_value_set,
            outdir=outdir, outfile=outfile, verbose=0, input_dir=input_dir)
    
    result_freq = np.array(result_list['freq_0']).astype(np.int64)
    print(result_freq)
    print(freq0_Hz)
    index_freq0 = np.where(result_freq == freq0_Hz)
    print(f'index at {freq0} GHz = {index_freq0}')
    print(f'a = {result_list["a"][index_freq0]}')
    print(f'b = {result_list["b"][index_freq0]}')
    print(f'P = {result_list["P"][index_freq0]}')
    print(f'a_err = {result_list["a_err"][index_freq0]}')
    print(f'b_err = {result_list["b_err"][index_freq0]}')
    print(f'P_err = {result_list["P_err"][index_freq0]}')
    print(f'redchi = {result_list["redchi"][index_freq0]}')
    print(f'success = {result_list["success"][index_freq0]}')
    pass
 
