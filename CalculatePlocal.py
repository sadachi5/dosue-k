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
            verbose=0,
            save=False,
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

        null_path = f'{null_dir}/all_null_x.npy'
        if save:
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

            # Save data to 
            np.save(null_path, self.null_x)
            pass
        else:
            self.null_x = np.load(null_path, allow_pickle=True)
            pass

        pass # End of __init__
    
    def get_p_local(self, value):
        # Check value
        if value is None or value is np.nan:
            print(f'WARNING!: The input value is None or nan. {value}')
            return 0.

        # Convert value (x) to index of array
        #   - 1e-4 is bin-width in x of cum_null_hist
        #   - 80000 is offset in index ( x = (index - 80000)*1e-4
        try:
            index_floor = int( np.floor(value/1e-4) + 80000 )
        except ValueError:
            print('WARNING! ValueError')
            print(f'    value = {value}')
            print(f'    value/1e-4 = {value/1e-4}')
            return 0.

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
        return (self.N_fit - integral_total)/self.N_fit

# End of class CalculatePlocal()


