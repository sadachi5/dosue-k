#!/bin/bash

#mkdir output/get_original_signal_log_tmp
python3 get_original_signal.py -1 >&output/get_original_signal_log_tmp/start_checkdata.log &
python3 get_original_signal.py 18 20 >&output/get_original_signal_log_tmp/start_18GHz.log &
python3 get_original_signal.py 20 22 >&output/get_original_signal_log_tmp/start_20GHz.log &
python3 get_original_signal.py 22 24 >&output/get_original_signal_log_tmp/start_22GHz.log &
python3 get_original_signal.py 24 26 >&output/get_original_signal_log_tmp/start_24GHz.log &
python3 get_original_signal.py 26 27 >&output/get_original_signal_log_tmp/start_26GHz.log &
