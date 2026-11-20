#!/usr/bin/env python3
import time
import json
import csv
import os
import subprocess
import re
from datetime import datetime

OUTPUT_JSONL = "/home/hpe/telemetry/dataset/5g_telco_metrics.jsonl"
OUTPUT_CSV = "/home/hpe/telemetry/dataset/5g_telco_metrics.csv"
FAULT_STATE_FILE = "/home/hpe/telemetry/active_fault.json"
KUBECONFIG = "/home/hpe/k8s-5g/config"

CSV_FIELDS = [
    "timestamp",
    "fault_label",
    "anomaly_severity",
    "cpu_load_pct",
    "controller_mem_pct",
    "healthy_pod_count",
    "amf_gnb_connected",
    "gnb_service_active",
    "ue1_service_active",
    "ue2_service_active",
    "prach_rssi_db",
    "prach_snr_db",
    "prach_ta_us",
    "prach_sinr",
    "dropped_packets",
    "pusch_crc_status"
]

def get_controller_metrics():
    try:
        with open("/proc/loadavg", "r") as f:
            load = float(f.read().split()[0])
        with open("/proc/meminfo", "r") as f:
            mem = {}
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    mem[parts[0].strip()] = int(parts[1].split()[0])
        total = mem.get("MemTotal", 1)
        avail = mem.get("MemAvailable", 0)
        mem_pct = round((1.0 - (avail / total)) * 100, 2)
        return load, mem_pct
    except Exception:
        return 0.0, 0.0

def get_network_drops():
    try:
        with open("/proc/net/dev", "r") as f:
            for line in f:
                if "enp1s0" in line or "vlan10" in line or "eno1" in line:
                    cols = line.split(":")[1].split()
                    rx_drop = int(cols[2])
                    tx_drop = int(cols[10])
                    return rx_drop + tx_drop
        return 0
    except Exception:
        return 0

def get_k8s_metrics():
    try:
        cmd = f"KUBECONFIG={KUBECONFIG} kubectl get pods -n open5gs --no-headers"
        out = subprocess.check_output(cmd, shell=True, text=True, timeout=3)
        lines = [l for l in out.strip().split("\n") if l]
        ready = sum(1 for l in lines if "1/1" in l and "Running" in l)
        return ready
    except Exception:
        return 0

def get_amf_gnb_count():
    try:
        cmd = f"KUBECONFIG={KUBECONFIG} kubectl logs -n open5gs deploy/open5gs-amf --tail=10"
        out = subprocess.check_output(cmd, shell=True, text=True, timeout=3)
        matches = re.findall(r"Number of gNBs is now (\d+)", out)
        if matches:
            return int(matches[-1])
        return 0
    except Exception:
        return 0

def get_service_status(host, service):
    try:
        cmd = f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 ubuntu@{host} 'systemctl is-active {service}'"
        out = subprocess.check_output(cmd, shell=True, text=True, timeout=4).strip()
        return 1 if out == "active" else 0
    except Exception:
        return 0

def parse_gnb_rf_metrics():
    try:
        cmd = "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 ubuntu@10.10.10.4 'tail -n 30 /tmp/gnb.log'"
        out = subprocess.check_output(cmd, shell=True, text=True, timeout=4)
        
        prach_m = re.findall(r"PRACH:\s+rssi=([-\d\.]+)dB.*ta=([-\d\.]+)us.*snr=([-\d\.]+)dB", out)
        pusch_m = re.findall(r"PUSCH:.*crc=(\w+).*sinr=([-\d\.]+)dB", out)
        
        rssi, ta, snr = (-26.7, 23.4, -8.0)
        if prach_m:
            rssi = float(prach_m[-1][0])
            ta = float(prach_m[-1][1])
            snr = float(prach_m[-1][2])
            
        crc_status, sinr = ("KO", -22.0)
        if pusch_m:
            crc_status = pusch_m[-1][0]
            sinr = float(pusch_m[-1][1])
            
        return rssi, snr, ta, sinr, crc_status
    except Exception:
        return -999.0, -999.0, 0.0, -999.0, "NONE"

def collect_sample(fault_label="nominal", severity=0):
    if os.path.exists(FAULT_STATE_FILE):
        try:
            with open(FAULT_STATE_FILE, "r") as f:
                fdata = json.load(f)
                fault_label = fdata.get("fault_label", fault_label)
                severity = fdata.get("anomaly_severity", severity)
        except Exception:
            pass

    now = datetime.utcnow().isoformat() + "Z"
    cpu_load, mem_pct = get_controller_metrics()
    k8s_pods = get_k8s_metrics()
    amf_gnbs = get_amf_gnb_count()
    gnb_active = get_service_status("10.10.10.4", "srsgnb")
    ue1_active = get_service_status("10.10.10.5", "srsue1")
    ue2_active = get_service_status("10.10.10.5", "srsue2")
    rssi, snr, ta, sinr, crc = parse_gnb_rf_metrics()
    drops = get_network_drops()
    
    sample = {
        "timestamp": now,
        "fault_label": fault_label,
        "anomaly_severity": severity,
        "cpu_load_pct": cpu_load,
        "controller_mem_pct": mem_pct,
        "healthy_pod_count": k8s_pods,
        "amf_gnb_connected": amf_gnbs,
        "gnb_service_active": gnb_active,
        "ue1_service_active": ue1_active,
        "ue2_service_active": ue2_active,
        "prach_rssi_db": rssi,
        "prach_snr_db": snr,
        "prach_ta_us": ta,
        "prach_sinr": sinr,
        "dropped_packets": drops,
        "pusch_crc_status": crc
    }
    
    # Append to JSONL
    with open(OUTPUT_JSONL, "a") as f:
        f.write(json.dumps(sample) + "\n")
        
    # Append to CSV
    file_exists = os.path.exists(OUTPUT_CSV)
    with open(OUTPUT_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS, extrasaction='ignore')
        if not file_exists:
            writer.writeheader()
        writer.writerow(sample)
        
    return sample

if __name__ == "__main__":
    s = collect_sample()
    print("Collected live sample:")
    print(json.dumps(s, indent=2))
