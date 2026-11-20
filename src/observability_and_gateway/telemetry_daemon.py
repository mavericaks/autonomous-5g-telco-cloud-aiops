#!/usr/bin/env python3
import time
import sys
import logging
from collector import collect_sample

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    logging.info("Starting Autonomous 5G Multi-Tier Telemetry Daemon...")
    sample_count = 0
    while True:
        try:
            # Nominal collection
            sample = collect_sample(fault_label="nominal", severity=0)
            sample_count += 1
            if sample_count % 12 == 0: # Every minute
                logging.info(f"Sample #{sample_count}: K8s={sample['k8s_open5gs_pods_ready']}/13 | AMF_gNB={sample['amf_gnb_connected']} | RSSI={sample['prach_rssi_db']}dB | SINR={sample['pusch_sinr_db']}dB")
            time.sleep(5)
        except Exception as e:
            logging.error(f"Error collecting sample: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
