#!/usr/bin/env bash
wget http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz -P /tmp/
tar xzvf /tmp/coinbaseUSD.csv.gz -C /tmp/