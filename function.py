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

def dat_to_array(path):
    f = open(path, "r")
    data = f.read().split("\n")[3:-1]
    freq = np.array([float(val.split(" ")[0]) for val in data])
    dBm = np.array([float(val.split(" ")[1]) for val in data])
    W = 10 ** (dBm / 10) / 1000
    f.close()

    return freq, W

def csv_to_array(path):
    result = {}
    df = pd.read_csv(path)
    for col in df.columns:
        result[str(col)] =  np.array(df[col])
    
    return result



def cut_data(x, y):
    freq = []
    W = []
    for a, b in zip(x, y):
        if a >= x[0] + 250.e+3 and a < x[0] + 250.e+3 + 2.e+6:
            freq.append(a)
            W.append(b)
        
    return np.array(freq), np.array(W)

def yfactor_analysis(freq, Wamb, WLN2, Wamb_err, WLN2_err, Tamb):
    # ２点を通る直線　y = ax + b
    a = (Wamb - WLN2) / (Tamb - TLN2)
    b = Wamb - a * Tamb
    a_err = ((Wamb_err**2 + WLN2_err**2)/(Tamb - TLN2)**2)**0.5
    b_err = (Wamb_err**2 + (a_err*Tamb)**2)**0.5

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


