#!/bin/bash
clear
top -n 46000 -b > StressTestResult.txt &
sleep 5m
stress -c 4 -t 7200s
sleep 5m
stress -c 8 -t 7200s
sleep 5m
stress -c 32 -t 7200s
sleep 5m
stress -i 4 -t 7200s
sleep 5m
stress -i 8 -t 7200s
sleep 5m
stress -i 32 -t 7200s
sleep 5m
stress -m 4 -t 7200s
sleep 5m
stress -m 8 -t 7200s
sleep 5m
stress -m 32 -t 7200s
sleep 5m
stress -c 8 -i 8 -t 7200s
sleep 5m
stress -c 8 -m 8 -t 7200s
sleep 5m
stress -i 8 -m 8 -t 7200s
sleep 5m
stress -c 32 -i 32 -t 7200s
sleep 5m
stress -c 32 -m 32 -t 7200s
sleep 5m
stress -i 32 -m 32 -t 7200s
sleep 5m
stress -c 4 -i 4 -m 4 -t 7200s
sleep 5m
stress -c 8 -i 8 -m 8 -t 7200s
sleep 5m
stress -c 32 -i 32 -m 32 -t 7200s
sleep 5m
