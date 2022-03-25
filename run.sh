#! /bin/bash

cd /home/thodoris/Desktop/Finance/functions
for i in  rsi_bb_stochastic_ADX.py EMA_MACD.py cci_sar.py z_score.py limits.py fib.py
	do
		 python3 $i
	done 
