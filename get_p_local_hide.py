import os
import sys
import numpy as np
import function as func
import csv

from CalculatePlocal import CalculatePlocal

''' Old function
def get_p_local(value, pop, N_fit):
    num = int(np.floor((value+8)*1e+4))

    left0 = 0
    for i in range(18, 27, 1):
        left0 += np.sum(pop[str(i)][:num])
        pass

    left1 = 0
    #left2 = 0
    for start in range(18, 27, 1):
        path = "/data/ms2840a/other_data/Neff/null_pop/{}GHz_{}.csv".format(start, num)
        data = func.csv_to_array(path)
        null_value = data['value']
        islow = np.where(null_value < value)[0]
        left1 += len(islow)
        #for d in data["value"]:
        #    if d < value:
        #        left2 += 1
        #        pass
        #    pass
        pass
    #print(left1, left2)
    left = left0 + left1
    
    return (N_fit - left)/N_fit
'''


if __name__ == "__main__":
    # N_fit = 12_C_6 * 1/2 * 100MHz/2kHz * 10 freqs (18, 19, 20,..,27 GHz)
    #N_fit = 207900000
    N_fit = 207900000 + 1
    pop_null = func.csv_to_array("/data/ms2840a/other_data/Neff/null_pop_len.csv")
    save = False

    #indir     = '/data/ms2840a/result_data/fit_result'
    #indir_add = '/data/ms2840a/result_data/check_result/fit_result_mean_W'
    #outdir    = '/data/ms2840a/result_data/signal_p_local'
    #outdir_add= '/data/ms2840a/result_data/check_result/signal_p_local_mean_W'

    # Fit result with rebinned data (rebinmethod=0)
    #indir     = './output/result_data_newrebin/fit_result'
    #indir_add = ''
    #outdir    = './output/result_data_newrebin/signal_p_local'
    #outdir_add= ''

    # Fit result with rebinned data (rebinmethod=1)
    indir     = './output/result_data_newrebin1/fit_result2'
    indir_add = './output/result_data_newrebin1/fit_result2/after_add'
    outdir    = './output/result_data_newrebin1/signal_p_local2'
    outdir_add= './output/result_data_newrebin1/signal_p_local2/after_add'

    if not os.path.isdir(outdir):
        os.makedirs(outdir)
        pass
    if not os.path.isdir(outdir_add) and outdir_add != '':
        os.makedirs(outdir_add)
        pass

    # Initialize CalculatePlocal
    calcP = CalculatePlocal(N_fit = N_fit, verbose=0, save=save)

    # 100MHz span
    for i in range(180, 265, 1):
        if i%10 == 0: print(f'freq = {i*0.1} GHz')
        start_freq = (float)(i/10.) # GHz
        initial_MHz = int(start_freq * 1e+3) # MHz
        final_MHz = int(initial_MHz + 100) # MHz
        # 2MHz span
        for j in range(initial_MHz, final_MHz, 2): 
            freq0 = (int)(j*1e+6) # Hz
            #print(f'freq = {freq0} Hz')
            start_str, start_100MHz_str, is_add_data\
                = func.get_file_freq(freq0, verbose=0)
            data = func.csv_to_array(f'{indir}/start_{start_str}GHz.csv')
            outpath = f'{outdir}/start_{start_str}GHz.csv'
            pop = data['P']/data['P_err']
            if is_add_data and indir_add != '':
                data_add = func.csv_to_array(f'{indir_add}/start_{start_str}GHz.csv')
                outpath_add = f'{outdir_add}/start_{start_str}GHz.csv'
                pop_add = data_add['P']/data_add['P_err']
                pass
            pass

            # Save p-local for nominal data (including additional data)
            with open(outpath, "w") as f:
                writer = csv.writer(f)
                writer.writerow(["freq_0", "p_local"])
                for j in range(len(data["freq_0"])):
                    #print(f'freq = {data["freq_0"][j]} Hz')
                    #p_local = get_p_local(pop[j], pop_null, N_fit=N_fit)
                    p_local = calcP.get_p_local(pop[j])
                    writer.writerow([data["freq_0"][j], p_local])
                    pass
                pass
            
            # Save p-local for frequency span with additional data (after adding data)
            if is_add_data and indir_add != '':
                with open(outpath_add, "w") as f:
                    writer = csv.writer(f)
                    writer.writerow(["freq_0", "p_local"])
                    for j in range(len(data_add["freq_0"])):
                        #p_local = get_p_local(pop_add[j], pop_null, N_fit=N_fit)
                        p_local = calcP.get_p_local(pop_add[j])
                        writer.writerow([data_add["freq_0"][j], p_local])
                        pass
                    pass

            pass # End of loop over 100MHz frequency spans
        pass
    
    pass # End of __main__
