#!/bin/bash
echo "=========================================================="
echo " Starting 5G User Equipment (UE 3)"
echo " IMSI: 999700000000003"
echo "=========================================================="
sudo ip netns add ue3 2>/dev/null || true
sudo srsue /home/ubuntu/5g-ran/ue3.conf
