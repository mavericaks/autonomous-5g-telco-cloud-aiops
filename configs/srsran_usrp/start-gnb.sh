#!/bin/bash
echo "=========================================================="
echo " Starting srsRAN Project 5G Standalone (SA) gNodeB"
echo " AMF: 192.168.100.174 (via SCTP NodePort 31412)"
echo " Radio: USRP B210 (Serial: 34B18C8, Band 3 FDD, 10 MHz)"
echo " PLMN: 99970 | TAC: 1"
echo "=========================================================="
sudo rm -f /tmp/gnb.log /tmp/gnb*.pcap
exec sudo gnb -c /home/ubuntu/5g-ran/gnb_b210_srsue.yml
