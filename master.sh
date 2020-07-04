#!/bin/bash

CFGFN=params.yaml
if [ -e master_auto_match.py ]; then
    uvicorn master_auto_match:app --host $(cat $CFGFN |shyaml get-value masterHost) --port $(cat $CFGFN |shyaml get-value masterPort) &
fi

while [ 1 ]
do
    sleep 10
done

trap "kill -9 $! && echo killed PID[$!]" INT
