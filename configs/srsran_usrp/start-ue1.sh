#!/bin/bash
echo "=========================================================="
echo " Starting 5G User Equipment (UE 1)"
echo " IMSI: 999700000000001"
echo "=========================================================="
sudo ip netns add ue1 2>/dev/null || true
sudo srsue /home/ubuntu/5g-ran/ue1.conf
