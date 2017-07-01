#!/usr/bin/env bash
wget http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz -P /tmp/
gunzip /tmp/coinbaseUSD.csv.gz