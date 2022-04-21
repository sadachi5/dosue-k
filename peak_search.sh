#!/bin/bash

#mkdir output/peak_search_log_tmp
python3 peak_search.py 18 19 >&output/peak_search_log_tmp/start_18GHz.log &
python3 peak_search.py 19 20 >&output/peak_search_log_tmp/start_19GHz.log &
python3 peak_search.py 20 21 >&output/peak_search_log_tmp/start_20GHz.log &
python3 peak_search.py 21 22 >&output/peak_search_log_tmp/start_21GHz.log &
python3 peak_search.py 22 23 >&output/peak_search_log_tmp/start_22GHz.log &
python3 peak_search.py 23 24 >&output/peak_search_log_tmp/start_23GHz.log &
python3 peak_search.py 24 25 >&output/peak_search_log_tmp/start_24GHz.log &
python3 peak_search.py 25 26 >&output/peak_search_log_tmp/start_25GHz.log &
python3 peak_search.py 26 27 >&output/peak_search_log_tmp/start_26GHz.log &
