import numpy as np
import matplotlib.pyplot as plt
import function as func
import csv
import math
import itertools
from scipy import special
import lmfit
import sys
import datetime
import os
import fit_script as fit



def make_combination():
    result = []
    for num in range(2, 14, 2):
        if num != 12: continue
        t_list = list(itertools.combinations(range(12), num))
        for t in t_list:
            s_list = list(itertools.combinations(range(num), int(num/2)))
            for s in s_list:
                r = list(range(0,num))
                for cut in range(int(num/2)):
                    r.remove(s[cut])
                if 0 in r: continue
                result.append([[t[s[x]] for x in range(int(num/2))], [t[r[x]] for x in range(int(num/2))]])
            
    return result


if __name__ == "__main__":
    start_freq = float(sys.argv[1])          # 18.0, 18.1, 18.2, ... , 26.3
    num = int(sys.argv[2])                   # combination number
    initial = int(start_freq * 1.e+6 - 250)  # 18.0 GHz - 250 kHz
    final = int(initial + 1.e+5)             # 18.0 GHz + 100 MHz - 250 kHz

    combination = make_combination()
    
    
    for i in range(initial, final, 2000): 
        # フィットする2.0 MHzの幅　
        # 2000だと 2.0 MHz 50回で 100 MHz 隙間なくフィット　
        # 20000だと 2.0 MHz 5回で 100 MHz を 10分の1だけフィット
        word = list(str(i))
        word.insert(2, ".")
        start = "".join(word)
        
        out_path = "/data/ms2840a/result_data/null_sample_fit/start_{}GHz_{}.csv".format(start, num)
        #if os.path.exists(out_path): continue

        path = "/data/ms2840a/result_data/signal_12_data/start_{}GHz.csv".format(start)
        signal = func.csv_to_array(path)
        freq = signal["freq"]
            
        null = np.zeros(len(freq))
        for a in combination[num][0]:
            null += signal["W_" + str(a)]
        for b in combination[num][1]:
            null -= signal["W_" + str(b)]
            
        if num % 2 == 0:
            null = null / 12
        else:
            null = null / 12 * -1
            
        freq, null, null_err = func.rebin_func(freq, null)
        
        fit.fitting(out_path, start, start_freq, freq, null)
