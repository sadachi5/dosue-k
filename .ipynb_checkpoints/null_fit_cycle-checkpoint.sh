#!/bin/bash

for i in {180..263}; do
    int=$((i / 10))
    shousu=$((i % 10))

    if [ ${shousu} -eq 9 ]; then
        python3 -u get_p_local_hide.py ${int}.${shousu} ${j}
    else
        python3 -u get_p_local_hide.py ${int}.${shousu} ${j} &
    fi

done
