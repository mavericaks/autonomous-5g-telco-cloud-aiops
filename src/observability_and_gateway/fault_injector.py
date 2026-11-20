#!/usr/bin/env python3
import time
import json
import subprocess
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
FAULT_STATE_FILE = "/home/hpe/telemetry/active_fault.json"
KUBECONFIG = "/home/hpe/k8s-5g/config"

def set_fault_state(label, severity):
    state = {
        "fault_label": label,
        "anomaly_severity": severity,
        "timestamp": time.time()
    }
    with open(FAULT_STATE_FILE, "w") as f:
        json.dump(state, f)
    logging.info(f">>> Active Fault State Set: {label} (severity={severity})")

def clear_fault_state():
    set_fault_state("nominal", 0)

def fault_1_ovn_network_impairment(duration=25):
    logging.info("[START] Fault 1: OVN Overlay Network Impairment on compute-pc1 (delay 80ms 20ms loss 7%)")
    set_fault_state("ovn_sdn_latency_loss", 2)
    try:
        subprocess.run("ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'sudo tc qdisc del dev enp1s0 root 2>/dev/null || true'", shell=True)
        subprocess.run("ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'sudo tc qdisc add dev enp1s0 root netem delay 80ms 20ms loss 7%'", shell=True, check=True)
        time.sleep(duration)
    finally:
        logging.info("[CLEANUP] Removing network impairment on enp1s0...")
        subprocess.run("ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'sudo tc qdisc del dev enp1s0 root 2>/dev/null || true'", shell=True)
        clear_fault_state()
        time.sleep(10)

def fault_2_k8s_upf_pod_termination(duration=25):
    logging.info("[START] Fault 2: Cloud 5G UPF Pod Crash Injection")
    set_fault_state("k8s_container_crash", 2)
    try:
        cmd = f"KUBECONFIG={KUBECONFIG} kubectl delete pod -n open5gs -l app.kubernetes.io/name=upf --grace-period=0 --force"
        subprocess.run(cmd, shell=True, capture_output=True)
        time.sleep(duration)
    finally:
        logging.info("[CLEANUP] Waiting for K8s deployment controller self-recovery...")
        time.sleep(10)
        clear_fault_state()

def fault_3_compute_cpu_starvation(duration=25):
    logging.info("[START] Fault 3: Compute Node 1 CPU & I/O Starvation")
    set_fault_state("compute_cpu_exhaustion", 2)
    try:
        cmd = f"ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'stress-ng --cpu 8 --io 4 --timeout {duration}s >/dev/null 2>&1 &'"
        subprocess.run(cmd, shell=True)
        time.sleep(duration)
    finally:
        logging.info("[CLEANUP] Ensuring stress-ng termination on compute-pc1...")
        subprocess.run("ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'sudo pkill -9 stress-ng 2>/dev/null || true'", shell=True)
        clear_fault_state()
        time.sleep(10)

def fault_4_rf_gain_attenuation(duration=25):
    logging.info("[START] Fault 4: Physical RF Gain Attenuation (Dropping TX power to 30dB)")
    set_fault_state("rf_path_loss_attenuation", 2)
    try:
        subprocess.run("ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 \"sudo sed -i 's/tx_gain: .*/tx_gain: 30/' /home/ubuntu/5g-ran/gnb_b210_srsue.yml && sudo systemctl restart srsgnb\"", shell=True)
        time.sleep(duration)
    finally:
        logging.info("[CLEANUP] Restoring nominal RF TX power to 85 dB...")
        subprocess.run("ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 \"sudo sed -i 's/tx_gain: .*/tx_gain: 85/' /home/ubuntu/5g-ran/gnb_b210_srsue.yml && sudo systemctl restart srsgnb\"", shell=True)
        clear_fault_state()
        time.sleep(10)

def run_all_scenarios():
    logging.info("Starting Automated Labeled Fault Injection Harness across 4 Scenarios...")
    clear_fault_state()
    time.sleep(5)
    
    fault_1_ovn_network_impairment(duration=20)
    fault_2_k8s_upf_pod_termination(duration=20)
    fault_3_compute_cpu_starvation(duration=20)
    fault_4_rf_gain_attenuation(duration=20)
    
    logging.info("All 4 Fault Injection Scenarios Successfully Executed and Labeled!")

if __name__ == "__main__":
    run_all_scenarios()
