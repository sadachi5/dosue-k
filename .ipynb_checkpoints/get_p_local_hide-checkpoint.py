import sys
import numpy as np
import function as func
import csv

def get_p_local(value, pop):
    num = int(np.floor((value+8)*1e+4))

    left = 0
    for i in range(18, 27, 1):
        left += np.sum(pop[str(i)][:num])

    for start in range(18, 27, 1):
        path = "/data/ms2840a/other_data/Neff/null_pop/{}GHz_{}.csv".format(start, num)
        data = func.csv_to_array(path)
        for d in data["value"]:
            if d < value:
                left += 1
    
    return (N_fit - left)/N_fit

if __name__ == "__main__":
    N_fit = 207900000
    pop = func.csv_to_array("/data/ms2840a/other_data/Neff/null_pop_len.csv")
    #start_freq = float(sys.argv[1])
    #initial = int(start_freq * 1.e+6 - 250)
    #final = int(initial + 1.e+5)

    check_freq = np.array([18190, 18336, 19120, 19186, 19440, 19478, 19766, 19794, 19818, 20006, 20296, 20302, 20490, 20540, 20892, 21442, 21808, 22522, 22672, 23306, 23808, 23934, 25328, 25352, 25860, 26274, 26346])
    
    check_freq = np.array([25860, 26274, 26346])

    for i in check_freq:
        word = list(str(i*1000 - 250))
        word.insert(2, ".")
        start = "".join(word)
        
        data1 = func.csv_to_array("/data/ms2840a/result_data/check_result/fit_result_mean_W/start_{}GHz.csv".format(start))
        pop1 = data1["P"]/data1["P_err"]
        path = "/data/ms2840a/result_data/check_result/signal_p_local_mean_W/start_{}GHz.csv".format(start)
        
        with open(path, "w") as f:
            writer = csv.writer(f)
            writer.writerow(["freq_0", "p_local"])
            for j in range(len(data1["freq_0"])):
                writer.writerow([data1["freq_0"][j], get_p_local(pop1[j], pop)])