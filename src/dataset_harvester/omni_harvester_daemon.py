#!/usr/bin/env python3
"""
Continuous Production Daemon: Omni-Plane Cross-Layer Dataset & Log/Alert Harvester
==================================================================================
Managed by systemd (`omni-crosslayer-harvester.service`).
Runs continuously every 5.0 seconds, capturing 368 cross-layer telemetry parameters
and all incremental logs, Wazuh SIEM alerts, Kubernetes events, OpenStack LXD logs,
srsRAN USRP logs, and XIE AIOps decisions into the multi-format training warehouse.
"""

import os
import sys
import time
import json
import logging
from datetime import datetime, timezone

from omni_schema_and_harvester import (
    OmniPlaneCollector,
    save_schema_artifacts,
    FEATURE_CATALOG,
)
from omni_log_harvester_and_warehouse import (
    SQLiteWarehouseManager,
    CrossLayerLogHarvester,
    append_metrics_to_files,
    append_logs_to_files,
    rebuild_ml_tensors_and_manifest,
    enforce_sustainability_policy,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [OmniHarvester] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def main():
    logging.info("Starting Omni-Plane Cross-Layer Dataset & Log/Alert Harvester Daemon...")
    save_schema_artifacts()
    warehouse = SQLiteWarehouseManager()
    collector = OmniPlaneCollector()
    log_harvester = CrossLayerLogHarvester()

    try:
        m_cnt, l_cnt, _, _ = warehouse.get_counts()
        collector.seq_id = m_cnt
        logging.info(
            f"Initialized warehouse state: {m_cnt:,} existing time-series rows ({len(FEATURE_CATALOG)} features/row), "
            f"{l_cnt:,} existing log/alert events."
        )
    except Exception as e:
        logging.warning(f"Warehouse count check warning: {e}")

    tick_counter = 0
    while True:
        loop_start = time.time()
        try:
            # 1. Harvest 368 cross-layer parameters across all 6 planes
            row = collector.collect_full_cross_layer_tick()
            append_metrics_to_files([row])
            warehouse.insert_metrics_rows([row])

            # 2. Harvest incremental logs, Wazuh alerts, K8s events, OpenStack logs, RAN logs & XIE events
            new_events = log_harvester.harvest_incremental_logs(fault_label=row["fault_label"])
            if new_events:
                append_logs_to_files(new_events)
                warehouse.insert_log_events(new_events)

            tick_counter += 1

            # 3. Every 6 ticks (30 seconds), update manifest, audit log, and sustainability check
            if tick_counter % 6 == 0:
                warehouse.record_audit(
                    m_added=6,
                    l_added=len(new_events),
                    lat_ms=row["collection_latency_ms"],
                    notes="continuous_systemd_daemon",
                )
                enforce_sustainability_policy(max_active_mb=250.0)
                rebuild_ml_tensors_and_manifest(warehouse)
                m_tot, l_tot, _, _ = warehouse.get_counts()
                logging.info(
                    f"Tick #{collector.seq_id:,} | Features={len(FEATURE_CATALOG)} | "
                    f"Total Rows={m_tot:,} | Total Logs/Alerts={l_tot:,} (+{len(new_events)} this tick) | "
                    f"Fault={row['fault_label']} | HarvestLatency={row['collection_latency_ms']}ms"
                )
        except Exception as e:
            logging.error(f"Error in harvest cycle: {e}")

        elapsed = time.time() - loop_start
        sleep_s = max(1.0, 5.0 - elapsed)
        time.sleep(sleep_s)


if __name__ == "__main__":
    main()

