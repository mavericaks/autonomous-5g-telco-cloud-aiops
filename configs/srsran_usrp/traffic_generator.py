#!/usr/bin/env python3
import time
import subprocess
import socket
import threading
import os

CONTROLLER_IP = '10.10.10.1'
EXTERNAL_IP = '10.0.0.10'

def run_udp_saturation():
    """Continuous high-throughput UDP packet stream targeting 50-80 Mbps"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b'HPE_5G_AIOPS_HIGH_SATURATION_TELEMETRY_' * 35 # ~1365 bytes
    target_addr = (CONTROLLER_IP, 5201)
    batch_size = 50
    while True:
        try:
            for _ in range(batch_size):
                sock.sendto(payload, target_addr)
            time.sleep(0.005) # ~10,000 pkts/sec ~= ~100 Mbps burst capacity
        except Exception:
            time.sleep(0.1)

def run_iperf_bursts():
    """Periodic TCP bursts using iperf3 to exercise network buffers and TCP congestion"""
    while True:
        try:
            subprocess.run(
                ['iperf3', '-c', CONTROLLER_IP, '-t', '10', '-p', '5201', '-P', '2'],
                capture_output=True, timeout=15
            )
            time.sleep(5)
        except Exception:
            time.sleep(5)

def run_wifi_probes():
    """Dual-homed Wi-Fi telemetry ping probe on wlp2s0 (10.0.0.24) to VLAN 20"""
    while True:
        try:
            subprocess.run(
                ['ping', '-I', 'wlp2s0', '-c', '3', '-W', '1', EXTERNAL_IP],
                capture_output=True, timeout=5
            )
            time.sleep(2)
        except Exception:
            time.sleep(2)

if __name__ == '__main__':
    print('Starting Scaled 50-100 Mbps Multi-Stream Saturation Generator on compute-pc2...')
    threads = [
        threading.Thread(target=run_udp_saturation, daemon=True),
        threading.Thread(target=run_udp_saturation, daemon=True),
        threading.Thread(target=run_iperf_bursts, daemon=True),
        threading.Thread(target=run_wifi_probes, daemon=True)
    ]
    for t in threads:
        t.start()
    while True:
        time.sleep(1)
