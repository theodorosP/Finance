#! /bin/bash

declare -a arr=("BTC-USD" "BCH-USD" "BSV-USD" "DOGE-USD" "ETH-USD" "ETC-USD" "LTC-USD")
for i in "${arr[@]}"
do
	mkdir $i
done
