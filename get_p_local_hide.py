import os
import sys
import numpy as np
import function as func
import csv

class CalculatePlocal:
    '''
        Take time to initialize
        because this will open many files 
        to read null sample results
    '''
    def __init__(
            self,
            null_hist_file="/data/ms2840a/other_data/Neff/null_pop_len.csv",
            N_fit = 207900000,
            null_dir = "/data/ms2840a/other_data/Neff/null_pop",
            verbose=0
            ):  
        self.N_fit = N_fit

        # Retrieve cumulative histogram of # of null samples
        data = func.csv_to_array(null_hist_file)
        freq_list = np.array([ str(i) for i in range(18, 27, 1) ])

        # array of (freq x hist)
        null_hist_array = np.array([ data[key] for key in freq_list ])
        # sum over freqs
        null_hist_sum = np.sum(null_hist_array, axis=0)
        # index array for x-axis
        self.max_index = len(null_hist_sum)
        if verbose > 0: print(f'max_index = {self.max_index}')
        index_array = np.arange(self.max_index)
        # x = P/Perr array
        x = (index_array-80000.)*1.e-4 # 1 bin-width = 1e-4 in x

        # cumulative of # of null samples from -inf to x
        self.cum_null_hist = np.cumsum(null_hist_sum)
        # shift the hist to left by 1 bin
        self.cum_null_hist = np.concatenate([[0.], self.cum_null_hist])

        # Retrieve all null sample P/Perr results
        null_x_list = [ [] for i in range(self.max_index) ]
        for _freq in freq_list:
            print(f'input null freq = {_freq} GHz')
            for _index in range(self.max_index):
                _path = f'{null_dir}/{_freq}GHz_{_index}.csv'
                _data = func.csv_to_array(_path)
                if verbose > 0: 
                    print(f'input null file = {_path}')
                    print(f'keys = {_data.keys()}')
                    pass
                null_x_list[_index] += _data['value'].tolist()
                pass
            pass
        pass
        # Convert list to array
        self.null_x = [ np.array(_list) for _list in null_x_list ]
        pass
    
    def get_p_local(self, value):
        # Convert value (x) to index of array
        #   - 1e-4 is bin-width in x of cum_null_hist
        #   - 80000 is offset in index ( x = (index - 80000)*1e-4
        index_floor = int( np.floor(value/1e-4) + 80000 )
        if index_floor >= self.max_index:
            index_floor = -1
            pass
        # cumulative of # of null samples from -inf to floor(x)
        integral_floor = self.cum_null_hist[index_floor]

        # calculate # of null samples from floor(x) to x
        integral_edge = 0.
        if index_floor > 0:
            islow = np.where(self.null_x[index_floor] < value)
            if len(islow) > 0:
                integral_edge = float(len(islow))
                pass
            pass

        integral_total = integral_floor + integral_edge
        return (self.N_fit - integral_total)/self.N_fitkk

# End of class CalculatePlocal()


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


if __name__ == "__main__":
    # N_fit = 12_C_6 * 1/2 * 100MHz/2kHz * 10 freqs (18, 19, 20,..,27 GHz)
    #N_fit = 207900000
    N_fit = 207900000 + 1
    pop_null = func.csv_to_array("/data/ms2840a/other_data/Neff/null_pop_len.csv")

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
    indir     = './output/result_data_newrebin1/fit_result'
    indir_add = './output/result_data_newrebin1/fit_result/before_add'
    outdir    = './output/result_data_newrebin1/signal_p_local'
    outdir_add= './output/result_data_newrebin1/signal_p_local/before_add'

    if not os.path.isdir(outdir):
        os.makedirs(outdir)
        pass
    if not os.path.isdir(outdir_add) and outdir_add != '':
        os.makedirs(outdir_add)
        pass

    # Initialize CalculatePlocal
    calcP = CalculatePlocal(N_fit = N_fit, verbose=0)

    # 100MHz span
    for i in range(180, 265, 1):
        if i%10 == 0: print(f'freq = {i*0.1} GHz')
        start_freq = (float)(i/10.) # GHz
        initial_MHz = int(start_freq * 1e+3) # MHz
        final_MHz = int(initial_MHz + 100) # MHz
        # 2MHz span
        for j in range(initial_MHz, final_MHz, 2): 
            freq0 = (int)(j*1e+6) # Hz
            print(f'freq = {freq0} Hz')
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
                    print(f'freq = {data["freq_0"][j]} Hz')
                    #p_local = get_p_local(pop[j], pop_null, N_fit=N_fit)
                    p_local = calcP.get_p_local(pop[j])
                    writer.writerow([data["freq_0"][j], p_local])
                    pass
                pass
            
            # Save p-local for frequency span with additional data (before adding data)
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
