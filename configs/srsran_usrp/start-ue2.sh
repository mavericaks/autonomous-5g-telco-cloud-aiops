#!/bin/bash
echo "=========================================================="
echo " Starting 5G User Equipment (UE 2)"
echo " IMSI: 999700000000002"
echo "=========================================================="
sudo ip netns add ue2 2>/dev/null || true
sudo srsue /home/ubuntu/5g-ran/ue2.conf
