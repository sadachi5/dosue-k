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
    init_value_set = 2
    rebinfunc = 2 # No rebin

    freq_0 = 18.0
    if len(sys.argv) > 1:
        freq_0 = float(sys.argv[1]) # GHz
        pass

    start_str, start100MHz_str, is_add_data = func.get_file_freq(freq_0*1e+9)
    start_Hz = (float)(start_str)*1.e+9
    fit_one(start_Hz, rebinfunc=rebinfunc, init_value_set=init_value_set,
            outdir=outdir, outfile=outfile, verbose=1, input_dir=input_dir)
    
    pass
 
