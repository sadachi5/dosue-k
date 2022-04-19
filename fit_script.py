import csv
import lmfit
import numpy as np
from scipy import special

# Constants
v_c = 220.e+3 # [m/sec] speed of solar system
v_E = v_c # [m/sec] speed of earth
c = 299792458. # [m/sec] speed of light from wikipedia
k_B = 1.380649e-23 # [J/K] boltzmann constant
rbw = 3.e+2 # [Hz]
binwidth = 2.e+3 # [Hz]
T_LN2 = 77 # [K]

def cummulative_velocity(v):
    C = v_c/(2.*np.sqrt(np.pi)*v_E) 
    exp_p = np.exp( -1. * np.power((v+v_E)/v_c, 2.) )
    exp_m = np.exp( -1. * np.power((v-v_E)/v_c, 2.) )
    erf_p = special.erf((v+v_E)/v_c)
    erf_m = special.erf((v-v_E)/v_c)

    f = C*(exp_p-exp_m) + 1./2. * (erf_p + erf_m)
    return f

def freq_to_velocity(freq, freq_0):
    ok = (freq>freq_0)
    v  = np.full(len(freq), 0.)
    v[ok] = c * np.sqrt( 1. - np.power(freq_0/freq[ok], 2.))
    return v

def integral_binwidth_velocity(freq, freq_0, binwidth):
    v_p = freq_to_velocity(freq+binwidth/2., freq_0)
    v_m = freq_to_velocity(freq-binwidth/2., freq_0)
    integral = cummulative_velocity(v_p) - cummulative_velocity(v_m)
    return integral

def fit_func(freq, a, b, P, freq_0):
    integral = integral_binwidth_velocity(freq, freq_0, binwidth)
    peak = P * integral
    power = peak + a*(freq-freq_0) + b
    return power

def residual(params, fit_freq, fit_Psig, yerr, freq_0):
    a = params['a']
    b = params['b']
    P = params['P']
    y_model = fit_func(fit_freq, a, b, P, freq_0)
    chi = (fit_Psig - y_model)/yerr
    o = np.isfinite(chi)
    return chi[o]

def fitting(path, start, start_freq, freq, signal, dfreq_0=0):
    # path       is a file name for saving the fit reuslt. If it is '', no result will be saved.
    # freq       is frequency array
    # signal     is spectrum array
    # start        is base fit frequency such as 17.999750, 18.001750, ... 2 MHz range
    # start_freq is base frequency such as 18.0, 18.1, 18.2, ... 100 MHz range   
    # dfreq_0 is variation on the peak frequency of freq_0 [Hz]

    if len(path) > 0:
        #print('path=', path)
        with open(path, "w") as f:
            writer = csv.writer(f)
            writer.writerow([
                "freq_0", 
                "a", 
                "b", 
                "P", 
                "a_err", 
                "b_err", 
                "P_err", 
                "redchi", 
                "success"
            ])
            pass
        pass

    params = lmfit.Parameters()
    params.add('a', value=1.)
    params.add('b', value=1.)
    params.add('P', value=1.)

    start_col = (int(float(start) * 1.e+6 + 250. - start_freq * 1.e+6) // 2000) * 2000 * 1.e+3
    # 1e+3: kHz --> Hz
    #print(f'start_col = {start_col}')
    step_points = int(2.e+6/binwidth)
    result_list = {'a':[], 'b':[], 'P':[], 'a_err':[], 'b_err':[], 'P_err':[], 'freq_0':[], 'redchi':[], 'success':[]}
    for step in range(step_points):
        freq_0 = start_freq * 1.e+9 + start_col + step * binwidth + dfreq_0
        #print(f'freq_0 = {freq_0}')

        fit_freq = []
        fit_Psig = []
        fit_left = []
        fit_right = []
        for _f, _s in zip(freq, signal):
            if _f >= freq_0 - 50.e+3 and _f <= freq_0 + 200.e+3:
                fit_freq.append(_f)
                fit_Psig.append(_s)
            if _f >= freq_0 - 300.e+3 and _f <= freq_0 - 50.e+3:
                fit_left.append(_s)
            if _f >= freq_0 + 200.e+3 and _f <= freq_0 + 450.e+3:
                fit_right.append(_s)

        fit_freq = np.array(fit_freq)
        fit_Psig = np.array(fit_Psig)
        Perr = (np.std(np.array(fit_left)) + np.std(np.array(fit_right)))/2

        result = lmfit.minimize(residual, params, args=(fit_freq, fit_Psig, Perr, freq_0))
        
        if len(path) > 0:
            with open(path, "a") as f:
                writer = csv.writer(f)
                writer.writerow([
                    freq_0, 
                    result.params["a"].value, 
                    result.params["b"].value, 
                    result.params["P"].value, 
                    result.params["a"].stderr,  
                    result.params["b"].stderr, 
                    result.params["P"].stderr, 
                    result.redchi, 
                    result.success
                ])
                pass
            pass
        result_list['freq_0'].append(freq_0)
        result_list['a'].append(result.params["a"].value) 
        result_list['b'].append(result.params["b"].value) 
        result_list['P'].append(result.params["P"].value)
        result_list['a_err'].append(result.params["a"].stderr)  
        result_list['b_err'].append(result.params["b"].stderr)
        result_list['P_err'].append(result.params["P"].stderr)
        result_list['redchi'].append(result.redchi)
        result_list['success'].append(result.success)
        pass
    return result_list
