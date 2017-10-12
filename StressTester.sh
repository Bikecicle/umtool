#!/bin/bash
clear
top -n 46000 -b > StressTestResult.txt &
nohup sleep 5m
nohup stress -c 4 -t 7200s &
nohup sleep 125m
nohup stress -c 8 -t 7200s &
nohup sleep 125m
nohup stress -c 32 -t 7200s &
nohup sleep 125m
nohup stress -i 4 -t 7200s &
nohup sleep 125m
nohup stress -i 8 -t 7200s &
nohup sleep 125m
nohup stress -i 32 -t 7200s &
nohup sleep 125m
nohup stress -m 4 -t 7200s &
nohup sleep 125m
nohup stress -m 8 -t 7200s &
nohup sleep 125m
nohup stress -m 32 -t 7200s &
nohup sleep 125m
nohup stress -c 8 -i 8 -t 7200s &
nohup sleep 125m
nohup stress -c 8 -m 8 -t 7200s &
nohup sleep 125m
nohup stress -i 8 -m 8 -t 7200s &
nohup sleep 125m
nohup stress -c 32 -i 32 -t 7200s &
nohup sleep 125m
nohup stress -c 32 -m 32 -t 7200s &
nohup sleep 125m
nohup stress -i 32 -m 32 -t 7200s &
nohup sleep 125m
nohup stress -c 4 -i 4 -m 4 -t 7200s &
nohup sleep 125m
nohup stress -c 8 -i 8 -m 8 -t 7200s &
nohup sleep 125m
nohup stress -c 32 -i 32 -m 32 -t 7200s &
nohup sleep 125m