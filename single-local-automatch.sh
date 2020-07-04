#!/bin/bash

bash master.sh &
MASTER=$!
sleep 3
python3 servant_auto_match.py &
SERVANT=$!


clean(){
    kill -9 $MASTER
    kill -9 $SERVANT
}


while [ 1 ];
do
    sleep 10
done

trap 'clean' INT
