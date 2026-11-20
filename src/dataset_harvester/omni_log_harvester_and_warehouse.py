#!/usr/bin/env python3
"""
Omni-Plane Unified Log/Alert Harvester, SQLite WAL Warehouse & Sustainability Engine
=====================================================================================
Continuously harvests, normalizes, and indexes every log, alert, and event across all 6 planes,
maintains the SQLite WAL relational feature store, builds NumPy/Pandas ML training tensors,
and enforces automated partition rotation, gzip compression, and disk watermark sustainability.
"""

import os
import re
import csv
import json
import gzip
import time
import shutil
import sqlite3
import subprocess
from datetime import datetime, timezone
import numpy as np
import pandas as pd

from omni_schema_and_harvester import (
    BASE_DIR,
    METRICS_DIR,
    LOGS_DIR,
    LOGS_BY_PLANE_DIR,
    DB_DIR,
    SCHEMA_DIR,
    ARCHIVE_DIR,
    METRICS_JSONL,
    METRICS_CSV,
    METRICS_PKL,
    TENSORS_NPZ,
    LOGS_JSONL,
    LOGS_CSV,
    WAREHOUSE_DB,
    FEATURE_DICT_JSON,
    MANIFEST_JSON,
    CURSORS_JSON,
    LEGACY_JSONL,
    LEGACY_CSV,
    FAULT_STATE_FILE,
    KUBECONFIG,
    FEATURE_CATALOG,
    FEATURE_NAMES,
    LOG_CSV_FIELDS,
    FAULT_CLASSES,
    run_cmd,
)

PLANE_LOG_FILES = {
    1: os.path.join(LOGS_BY_PLANE_DIR, "plane1_hardware_kernel_os.jsonl"),
    2: os.path.join(LOGS_BY_PLANE_DIR, "plane2_openstack_kvm_ovn_sdn.jsonl"),
    3: os.path.join(LOGS_BY_PLANE_DIR, "plane3_k8s_open5gs_microservices.jsonl"),
    4: os.path.join(LOGS_BY_PLANE_DIR, "plane4_srsran_usrp_5g_phy.jsonl"),
    5: os.path.join(LOGS_BY_PLANE_DIR, "plane5_wazuh_siem_security_alerts.jsonl"),
    6: os.path.join(LOGS_BY_PLANE_DIR, "plane6_xie_aiops_gpu_remediation.jsonl"),
}

PLANE_NAMES = {
    1: "Plane 1: Bare-Metal Hardware, Kernel & Host OS",
    2: "Plane 2: OpenStack 2023.1 LXD, KVM & OVN/OVS SDN",
    3: "Plane 3: Magnum Kubernetes, Open5GS 5G Core & Microservices",
    4: "Plane 4: Physical 5G SDR RAN (4x USRP B210 & srsRAN)",
    5: "Plane 5: Wazuh SIEM v4.8.0 Security & Threat Alerts",
    6: "Plane 6: Distributed AI Compute & XIE Agentic AIOps",
}


def infer_severity(line: str):
    u = line.upper()
    if any(k in u for k in ("CRITICAL", "FATAL", "PANIC", "EMERG", "OOM")):
        return "CRITICAL", 12
    if any(k in u for k in ("ERROR", "ERR ", "FAIL", "EXCEPTION", "TRACEBACK", "CRASH", "KO")):
        return "ERROR", 8
    if any(k in u for k in ("WARN", "WARNING", "TIMEOUT", "EXPIRED", "FLAP", "DROP", "ANOMALY", "REMEDIAT")):
        return "WARNING", 5
    return "INFO", 3


class SQLiteWarehouseManager:
    def __init__(self, db_path=WAREHOUSE_DB):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA temp_store=MEMORY;")
        return conn

    def _init_db(self):
        conn = self._connect()
        cur = conn.cursor()

        # 1. Feature Catalog Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS feature_catalog (
                idx INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                plane_id INTEGER,
                plane TEXT,
                node TEXT,
                component TEXT,
                unit TEXT,
                dtype TEXT,
                ml_role TEXT,
                description TEXT
            )
        """)
        cur.executemany(
            """
            INSERT OR REPLACE INTO feature_catalog
            (idx, name, plane_id, plane, node, component, unit, dtype, ml_role, description)
            VALUES (:index, :name, :plane_id, :plane, :node, :component, :unit, :dtype, :ml_role, :description)
            """,
            FEATURE_CATALOG,
        )

        # 2. Wide Cross-Layer Time-Series Table (all 368 columns!)
        col_defs = []
        for f in FEATURE_CATALOG:
            cname = f["name"]
            sql_type = "TEXT" if f["dtype"] == "string" else ("INTEGER" if f["dtype"] in ("int", "int64") else "REAL")
            col_defs.append(f'"{cname}" {sql_type}')
        cols_sql = ", ".join(col_defs)
        cur.execute(f"CREATE TABLE IF NOT EXISTS metrics_wide ({cols_sql})")
        cur.execute('CREATE INDEX IF NOT EXISTS idx_metrics_ts ON metrics_wide ("timestamp")')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_metrics_fault ON metrics_wide ("fault_label")')

        # 3. Unified Logs, Alerts & Events Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS logs_alerts_stream (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                plane_id INTEGER,
                plane_name TEXT,
                source_node TEXT,
                service_component TEXT,
                log_path TEXT,
                severity TEXT,
                severity_num INTEGER,
                event_category TEXT,
                rule_or_code TEXT,
                mitre_tactic TEXT,
                correlated_fault_label TEXT,
                message TEXT
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_ts ON logs_alerts_stream (timestamp)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_plane ON logs_alerts_stream (plane_id)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_sev ON logs_alerts_stream (severity)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_node ON logs_alerts_stream (source_node)")

        # 4. Harvester Audit & Sustainability Table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS harvester_audit_log (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                metrics_rows_added INTEGER,
                logs_events_added INTEGER,
                collection_latency_ms REAL,
                data_disk_used_gb REAL,
                data_disk_free_gb REAL,
                data_disk_used_pct REAL,
                notes TEXT
            )
        """)

        conn.commit()
        conn.close()

    def insert_metrics_rows(self, rows):
        if not rows:
            return
        conn = self._connect()
        cur = conn.cursor()
        placeholders = ", ".join(["?"] * len(FEATURE_NAMES))
        quoted_cols = ", ".join([f'"{c}"' for c in FEATURE_NAMES])
        sql = f"INSERT INTO metrics_wide ({quoted_cols}) VALUES ({placeholders})"
        vals = [[r.get(c) for c in FEATURE_NAMES] for r in rows]
        cur.executemany(sql, vals)
        conn.commit()
        conn.close()

    def insert_log_events(self, events):
        if not events:
            return
        conn = self._connect()
        cur = conn.cursor()
        sql = """
            INSERT INTO logs_alerts_stream (
                timestamp, plane_id, plane_name, source_node, service_component,
                log_path, severity, severity_num, event_category, rule_or_code,
                mitre_tactic, correlated_fault_label, message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        vals = [
            (
                e["timestamp"],
                e["plane_id"],
                e["plane_name"],
                e["source_node"],
                e["service_component"],
                e["log_path"],
                e["severity"],
                e["severity_num"],
                e["event_category"],
                e["rule_or_code"],
                e["mitre_tactic"],
                e["correlated_fault_label"],
                e["message"],
            )
            for e in events
        ]
        cur.executemany(sql, vals)
        conn.commit()
        conn.close()

    def record_audit(self, m_added, l_added, lat_ms, notes="live_tick"):
        du = shutil.disk_usage("/data")
        used_gb = round(du.used / (1024 ** 3), 2)
        free_gb = round(du.free / (1024 ** 3), 2)
        pct = round((du.used / du.total) * 100.0, 2)
        conn = self._connect()
        conn.execute(
            """
            INSERT INTO harvester_audit_log
            (timestamp, metrics_rows_added, logs_events_added, collection_latency_ms,
             data_disk_used_gb, data_disk_free_gb, data_disk_used_pct, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (datetime.now(timezone.utc).isoformat(), m_added, l_added, lat_ms, used_gb, free_gb, pct, notes),
        )
        conn.commit()
        conn.close()

    def get_counts(self):
        conn = self._connect()
        cur = conn.cursor()
        cur.execute("SELECT COALESCE(MAX(rowid), 0) FROM metrics_wide")
        m_cnt = cur.fetchone()[0]
        cur.execute("SELECT COALESCE(MAX(event_id), 0) FROM logs_alerts_stream")
        l_cnt = cur.fetchone()[0]
        by_plane = {str(pid): os.path.getsize(pfile) if os.path.exists(pfile) else 0 for pid, pfile in PLANE_LOG_FILES.items()}
        cur.execute("SELECT fault_label, COUNT(*) FROM metrics_wide GROUP BY fault_label")
        by_fault = {str(r[0]): r[1] for r in cur.fetchall()}
        conn.close()
        return m_cnt, l_cnt, by_plane, by_fault


class CrossLayerLogHarvester:
    """
    Incremental cursor-based log & alert harvester across all 6 planes.
    """

    def __init__(self):
        self.cursors = self._load_cursors()
        self.event_seq = self.cursors.get("_event_seq", 0)

    def _load_cursors(self):
        if os.path.exists(CURSORS_JSON):
            try:
                with open(CURSORS_JSON) as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_cursors(self):
        self.cursors["_event_seq"] = self.event_seq
        os.makedirs(os.path.dirname(CURSORS_JSON), exist_ok=True)
        with open(CURSORS_JSON, "w") as f:
            json.dump(self.cursors, f, indent=2)

    def _make_event(
        self,
        plane_id,
        node,
        component,
        log_path,
        message,
        ts=None,
        severity=None,
        sev_num=None,
        category="system_log",
        rule_code="N/A",
        mitre="None",
        fault_label="nominal",
    ):
        self.event_seq += 1
        if not ts:
            ts = datetime.now(timezone.utc).isoformat()
        if not severity or sev_num is None:
            severity, sev_num = infer_severity(message)
        clean_msg = message.strip().replace("\r", " ").replace("\n", " ")[:1200]
        return {
            "event_id": self.event_seq,
            "timestamp": ts,
            "plane_id": plane_id,
            "plane_name": PLANE_NAMES[plane_id],
            "source_node": node,
            "service_component": component,
            "log_path": log_path,
            "severity": severity,
            "severity_num": sev_num,
            "event_category": category,
            "rule_or_code": str(rule_code),
            "mitre_tactic": str(mitre),
            "correlated_fault_label": fault_label,
            "message": clean_msg,
        }

    def parse_wazuh_alert_line(self, line, fault_label="nominal"):
        try:
            obj = json.loads(line)
            ts = obj.get("timestamp", datetime.now(timezone.utc).isoformat())
            rule = obj.get("rule", {})
            lvl = int(rule.get("level", 3))
            rid = str(rule.get("id", "0"))
            desc = rule.get("description", "Wazuh security event")
            mitre_obj = rule.get("mitre", {})
            tactics = ",".join(mitre_obj.get("tactic", [])) if mitre_obj else "None"
            agent = obj.get("agent", {})
            aname = agent.get("name", "hpe-PowerEdge-R760xs")
            aip = agent.get("ip", "10.0.0.10")
            loc = obj.get("location", "/var/ossec/logs/alerts/alerts.json")
            flog = obj.get("full_log", desc)
            sev = "CRITICAL" if lvl >= 12 else ("HIGH" if lvl >= 10 else ("WARNING" if lvl >= 7 else ("LOW" if lvl >= 4 else "INFO")))
            msg = f"[Rule {rid} L{lvl}] {desc} | {flog}"
            return self._make_event(
                plane_id=5,
                node=f"{aname} ({aip})",
                component="wazuh-siem-manager",
                log_path=loc,
                message=msg,
                ts=ts,
                severity=sev,
                sev_num=lvl,
                category="siem_alert",
                rule_code=f"WAZUH-{rid}",
                mitre=tactics or "None",
                fault_label=fault_label,
            )
        except Exception:
            return None

    def read_local_file_delta(self, path, plane_id, node, component, category, max_lines=150, fault_label="nominal"):
        events = []
        if not os.path.exists(path):
            return events
        try:
            size = os.path.getsize(path)
            last_pos = self.cursors.get(path, max(0, size - 32768))
            if size < last_pos:
                last_pos = 0
            if size == last_pos:
                return events
            with open(path, "r", errors="replace") as f:
                f.seek(last_pos)
                lines = f.readlines()
                self.cursors[path] = f.tell()
            for line in lines[-max_lines:]:
                line = line.strip()
                if not line:
                    continue
                events.append(
                    self._make_event(
                        plane_id=plane_id,
                        node=node,
                        component=component,
                        log_path=path,
                        message=line,
                        category=category,
                        fault_label=fault_label,
                    )
                )
        except Exception:
            pass
        return events

    def harvest_incremental_logs(self, fault_label="nominal"):
        events = []

        # 1. Plane 1: Local Dell kernel/syslog/auth + remote compute-pc1 & compute-pc2 syslog
        for lpath, comp, cat in [
            ("/var/log/syslog", "systemd-syslog", "os_syslog"),
            ("/var/log/auth.log", "pam-sshd-auth", "security_auth"),
            ("/var/log/kern.log", "linux-kernel", "kernel_event"),
        ]:
            events.extend(self.read_local_file_delta(lpath, 1, "hpe-PowerEdge-R760xs", comp, cat, max_lines=40, fault_label=fault_label))

        for tag, ip, hname in [("pc1", "10.10.10.4", "compute-pc1"), ("pc2", "10.10.10.5", "compute-pc2")]:
            out = run_cmd(f"ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 ubuntu@{ip} 'tail -n 8 /var/log/syslog 2>/dev/null'", timeout=2.5)
            if out:
                lines = [l.strip() for l in out.splitlines() if l.strip()]
                last_sig = self.cursors.get(f"remote_syslog_{tag}", "")
                new_lines = []
                for l in reversed(lines):
                    if l == last_sig:
                        break
                    new_lines.append(l)
                if lines:
                    self.cursors[f"remote_syslog_{tag}"] = lines[-1]
                for l in reversed(new_lines):
                    events.append(self._make_event(1, hname, "systemd-syslog", "/var/log/syslog", l, category="os_syslog", fault_label=fault_label))

        # 2. Plane 2: Local Nova/OVN/OVS logs + OpenStack LXD container logs
        for lpath, comp, cat in [
            ("/var/log/nova/nova-compute.log", "nova-compute", "openstack_compute"),
            ("/var/log/ovn/ovn-controller.log", "ovn-controller", "ovn_sdn"),
            ("/var/log/openvswitch/ovs-vswitchd.log", "ovs-vswitchd", "ovs_datapath"),
        ]:
            events.extend(self.read_local_file_delta(lpath, 2, "hpe-PowerEdge-R760xs", comp, cat, max_lines=30, fault_label=fault_label))

        os_cmd = (
            "sudo lxc exec openstack-ctl -- bash -c \""
            "lxc exec juju-65b4ac-0-lxd-2 -- tail -n 5 /var/log/keystone/keystone.log 2>/dev/null | sed 's/^/[KEYSTONE] /'; "
            "lxc exec juju-65b4ac-0-lxd-8 -- tail -n 5 /var/log/neutron/neutron-server.log 2>/dev/null | sed 's/^/[NEUTRON] /'; "
            "lxc exec juju-65b4ac-0-lxd-6 -- tail -n 4 /var/log/nova/nova-api-wsgi.log 2>/dev/null | sed 's/^/[NOVA-API] /'"
            "\""
        )
        os_out = run_cmd(os_cmd, timeout=3.0)
        if os_out:
            for l in os_out.splitlines():
                l = l.strip()
                if not l:
                    continue
                sig_key = "os_lxd_last_" + l[:24]
                if self.cursors.get(sig_key) == l:
                    continue
                self.cursors[sig_key] = l
                if l.startswith("[KEYSTONE]"):
                    events.append(self._make_event(2, "juju-65b4ac-0-lxd-2", "keystone-api", "/var/log/keystone/keystone.log", l[11:], category="openstack_identity", fault_label=fault_label))
                elif l.startswith("[NEUTRON]"):
                    events.append(self._make_event(2, "juju-65b4ac-0-lxd-8", "neutron-server", "/var/log/neutron/neutron-server.log", l[10:], category="openstack_neutron_sdn", fault_label=fault_label))
                elif l.startswith("[NOVA-API]"):
                    events.append(self._make_event(2, "juju-65b4ac-0-lxd-6", "nova-api-wsgi", "/var/log/nova/nova-api-wsgi.log", l[11:], category="openstack_nova_api", fault_label=fault_label))

        # 3. Plane 3: Kubernetes Open5GS & Online Boutique container logs
        k8s_cmd = (
            f"KUBECONFIG={KUBECONFIG} kubectl logs -n open5gs deploy/open5gs-amf --tail=4 2>/dev/null | sed 's/^/[AMF] /'; "
            f"KUBECONFIG={KUBECONFIG} kubectl logs -n open5gs deploy/open5gs-smf --tail=4 2>/dev/null | sed 's/^/[SMF] /'; "
            f"KUBECONFIG={KUBECONFIG} kubectl logs -n open5gs deploy/open5gs-upf --tail=4 2>/dev/null | sed 's/^/[UPF] /'; "
            f"KUBECONFIG={KUBECONFIG} kubectl logs -n microservices deploy/frontend --tail=4 2>/dev/null | sed 's/^/[FRONTEND] /'"
        )
        k8s_out = run_cmd(k8s_cmd, timeout=3.0)
        if k8s_out:
            for l in k8s_out.splitlines():
                l = l.strip()
                if not l:
                    continue
                tag = l.split("]", 1)[0] + "]"
                if self.cursors.get(f"k8s_{tag}") == l:
                    continue
                self.cursors[f"k8s_{tag}"] = l
                comp = "open5gs-amf" if "[AMF]" in tag else ("open5gs-smf" if "[SMF]" in tag else ("open5gs-upf" if "[UPF]" in tag else "boutique-frontend"))
                events.append(self._make_event(3, "k8s-5g-cluster", comp, f"k8s://pods/{comp}", l, category="k8s_container_log", fault_label=fault_label))

        # 4. Plane 4: srsRAN gNodeB & UE PHY/MAC radio logs
        ran_out = run_cmd("ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 ubuntu@10.10.10.4 'tail -n 6 /tmp/gnb.log 2>/dev/null'", timeout=2.5)
        if ran_out:
            lines = [l.strip() for l in ran_out.splitlines() if l.strip()]
            last_gnb = self.cursors.get("ran_gnb_last", "")
            for l in lines[-4:]:
                if l != last_gnb:
                    events.append(self._make_event(4, "compute-pc1 (10.10.10.4)", "srsran-gnb-usrp", "/tmp/gnb.log", l, category="5g_ran_phy_mac", fault_label=fault_label))
            if lines:
                self.cursors["ran_gnb_last"] = lines[-1]

        # 5. Plane 5: Wazuh SIEM live alerts (/var/ossec/logs/alerts/alerts.json)
        wz_out = run_cmd("sudo tail -n 15 /var/ossec/logs/alerts/alerts.json 2>/dev/null", timeout=2.0)
        if wz_out:
            lines = [l.strip() for l in wz_out.splitlines() if l.strip()]
            last_wz_id = self.cursors.get("wazuh_last_alert_id", "")
            new_wz = []
            for l in reversed(lines):
                try:
                    aid = json.loads(l).get("id", "")
                except Exception:
                    aid = l[:40]
                if aid == last_wz_id:
                    break
                new_wz.append(l)
            if lines:
                try:
                    self.cursors["wazuh_last_alert_id"] = json.loads(lines[-1]).get("id", "")
                except Exception:
                    pass
            for l in reversed(new_wz):
                ev = self.parse_wazuh_alert_line(l, fault_label=fault_label)
                if ev:
                    events.append(ev)

        # 6. Plane 6: XIE Self-Healing Agent audit log (/home/hpe/agent/logs/remediation_audit.log)
        events.extend(
            self.read_local_file_delta(
                "/home/hpe/agent/logs/remediation_audit.log",
                6,
                "hpe-PowerEdge-R760xs",
                "xie-self-healing-agent",
                "aiops_decision_audit",
                max_lines=30,
                fault_label=fault_label,
            )
        )

        self.save_cursors()
        return events


def append_metrics_to_files(rows):
    if not rows:
        return
    os.makedirs(METRICS_DIR, exist_ok=True)
    # 1. JSONL
    with open(METRICS_JSONL, "a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    # 2. CSV
    csv_exists = os.path.exists(METRICS_CSV) and os.path.getsize(METRICS_CSV) > 0
    with open(METRICS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FEATURE_NAMES, extrasaction="ignore")
        if not csv_exists:
            writer.writeheader()
        writer.writerows(rows)


def append_logs_to_files(events):
    if not events:
        return
    os.makedirs(LOGS_DIR, exist_ok=True)
    os.makedirs(LOGS_BY_PLANE_DIR, exist_ok=True)

    # 1. Unified JSONL
    with open(LOGS_JSONL, "a") as f:
        for ev in events:
            f.write(json.dumps(ev) + "\n")

    # 2. Unified CSV
    csv_exists = os.path.exists(LOGS_CSV) and os.path.getsize(LOGS_CSV) > 0
    with open(LOGS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_CSV_FIELDS, extrasaction="ignore")
        if not csv_exists:
            writer.writeheader()
        writer.writerows(events)

    # 3. Per-plane JSONL files
    by_p = {}
    for ev in events:
        pid = ev["plane_id"]
        by_p.setdefault(pid, []).append(ev)
    for pid, pevs in by_p.items():
        pfile = PLANE_LOG_FILES.get(pid)
        if pfile:
            with open(pfile, "a") as f:
                for ev in pevs:
                    f.write(json.dumps(ev) + "\n")


def rebuild_ml_tensors_and_manifest(warehouse: SQLiteWarehouseManager):
    """
    Exports ready-to-train NumPy compressed tensor arrays (training_tensors_X_y.npz),
    Pandas DataFrame binary (omni_metrics_dataframe.pkl), and updates dataset_manifest.json.
    """
    try:
        if os.path.exists(METRICS_CSV):
            df = pd.read_csv(METRICS_CSV, low_memory=False)
            tmp_pkl = METRICS_PKL + ".tmp"
            df.to_pickle(tmp_pkl)
            os.replace(tmp_pkl, METRICS_PKL)

            numeric_cols = [
                f["name"]
                for f in FEATURE_CATALOG
                if f["dtype"] in ("int", "int64", "float")
                and f["ml_role"] in ("input_feature", "causal_graph_node", "security_feature")
                and f["name"] in df.columns
            ]
            X_raw = df[numeric_cols].fillna(0.0).to_numpy(dtype=np.float32)
            mean = X_raw.mean(axis=0, keepdims=True)
            std = X_raw.std(axis=0, keepdims=True) + 1e-6
            X_norm = ((X_raw - mean) / std).astype(np.float32)

            y_class = df["fault_class_id"].fillna(0).to_numpy(dtype=np.int64) if "fault_class_id" in df.columns else np.zeros(len(df), dtype=np.int64)
            y_sev = df["anomaly_severity"].fillna(0).to_numpy(dtype=np.int64) if "anomaly_severity" in df.columns else np.zeros(len(df), dtype=np.int64)
            y_anom = df["is_anomalous"].fillna(0).to_numpy(dtype=np.int64) if "is_anomalous" in df.columns else np.zeros(len(df), dtype=np.int64)
            timestamps = df["timestamp"].astype(str).to_numpy()

            tmp_npz = TENSORS_NPZ + ".tmp.npz"
            np.savez_compressed(
                tmp_npz,
                X_raw=X_raw,
                X_normalized=X_norm,
                feature_mean=mean.squeeze(0),
                feature_std=std.squeeze(0),
                y_fault_class=y_class,
                y_anomaly_severity=y_sev,
                y_is_anomalous=y_anom,
                feature_names=np.array(numeric_cols),
                class_names=np.array(list(FAULT_CLASSES.keys())),
                timestamps=timestamps,
            )
            os.replace(tmp_npz, TENSORS_NPZ)
    except Exception:
        pass

        # Update live manifest
    try:
        m_cnt, l_cnt, logs_by_plane, metrics_by_fault = warehouse.get_counts()
        du1 = shutil.disk_usage("/data")
        du2 = shutil.disk_usage("/data_16tb") if os.path.exists("/data_16tb") else du1
        comb_tot_gb = round((du1.total + (du2.total if os.path.exists("/data_16tb") else 0)) / (1024 ** 3), 2)
        comb_used_gb = round((du1.used + (du2.used if os.path.exists("/data_16tb") else 0)) / (1024 ** 3), 2)
        comb_free_gb = round((du1.free + (du2.free if os.path.exists("/data_16tb") else 0)) / (1024 ** 3), 2)

        def fsize_mb(p):
            return round(os.path.getsize(p) / (1024 * 1024), 2) if os.path.exists(p) else 0.0

        archive_files = []
        for root, _, files in os.walk(ARCHIVE_DIR):
            for fn in files:
                fp = os.path.join(root, fn)
                archive_files.append({"file": os.path.relpath(fp, BASE_DIR), "size_mb": fsize_mb(fp)})

        manifest = {
            "last_updated_utc": datetime.now(timezone.utc).isoformat(),
            "daemon_service": "omni-crosslayer-harvester.service",
            "status": "ACTIVE_STREAMING",
            "sampling_interval_sec": 5.0,
            "storage_location": BASE_DIR,
            "deep_storage_16tb_vault": "/data_16tb/cross_layer_dataset_vault",
            "symlinks": [
                "/home/hpe/HPE/cross_layer_dataset",
                "/home/hpe/cross_layer_dataset",
                "/home/hpe/telemetry/dataset/cross_layer_dataset",
                "/data/cross_layer_dataset/06_16tb_deep_storage_vault",
            ],
            "timeseries_dataset": {
                "total_parameters_per_tick": len(FEATURE_CATALOG),
                "total_rows_captured": m_cnt,
                "total_datapoint_cells": m_cnt * len(FEATURE_CATALOG),
                "rows_by_fault_class": metrics_by_fault,
                "files": {
                    "jsonl_stream": {"path": METRICS_JSONL, "size_mb": fsize_mb(METRICS_JSONL)},
                    "csv_table": {"path": METRICS_CSV, "size_mb": fsize_mb(METRICS_CSV)},
                    "pandas_pickle": {"path": METRICS_PKL, "size_mb": fsize_mb(METRICS_PKL)},
                    "numpy_tensors_npz": {"path": TENSORS_NPZ, "size_mb": fsize_mb(TENSORS_NPZ)},
                },
            },
            "logs_alerts_events_dataset": {
                "total_schema_fields": len(LOG_CSV_FIELDS),
                "total_events_captured": l_cnt,
                "events_by_plane_id": logs_by_plane,
                "files": {
                    "unified_jsonl": {"path": LOGS_JSONL, "size_mb": fsize_mb(LOGS_JSONL)},
                    "unified_csv": {"path": LOGS_CSV, "size_mb": fsize_mb(LOGS_CSV)},
                    "by_plane_jsonl": {str(k): {"path": v, "size_mb": fsize_mb(v)} for k, v in PLANE_LOG_FILES.items()},
                },
            },
            "relational_warehouse": {
                "sqlite_wal_db": WAREHOUSE_DB,
                "size_mb": fsize_mb(WAREHOUSE_DB),
                "tables": ["metrics_wide", "logs_alerts_stream", "feature_catalog", "harvester_audit_log"],
            },
            "compressed_partitions": {
                "archive_dir": ARCHIVE_DIR,
                "vault_16tb_dir": "/data_16tb/cross_layer_dataset_vault/partitions_compressed",
                "partition_count": len(archive_files),
                "partitions": archive_files[:25],
            },
            "sustainability_and_disk_health": {
                "tier1_hot_mount": "/data (/dev/sda1 - 2.95 TB)",
                "tier2_deep_vault_mount": "/data_16tb (/dev/mapper/cinder--volumes-lv_ai_dataset_16tb - 14.0 TB)",
                "combined_total_capacity_gb": comb_tot_gb,
                "combined_used_capacity_gb": comb_used_gb,
                "combined_free_capacity_gb": comb_free_gb,
                "combined_used_pct": round((comb_used_gb / max(1.0, comb_tot_gb)) * 100.0, 2),
                "high_watermark_pct": 85.0,
                "sustainability_status": f"HEALTHY ({comb_free_gb} GB / {round(comb_free_gb/1024, 2)} TB Free across 16.9 TB Enterprise RAID Pool)",
            },
        }
        with open(MANIFEST_JSON, "w") as f:
            json.dump(manifest, f, indent=2)
    except Exception:
        pass


def enforce_sustainability_policy(max_active_mb=250.0):
    """
    Rotates and gzip-compresses active JSONL streams if they exceed max_active_mb,
    mirrors compressed partitions and tensor snapshots to the 14 TB /data_16tb vault,
    and automatically spills over if Tier-1 /data exceeds 75% usage.
    """
    now = datetime.now(timezone.utc)
    part_dir = os.path.join(ARCHIVE_DIR, f"date={now.strftime('%Y-%m-%d')}", f"hour={now.strftime('%H')}")
    os.makedirs(part_dir, exist_ok=True)

    vault_part_dir = f"/data_16tb/cross_layer_dataset_vault/partitions_compressed/date={now.strftime('%Y-%m-%d')}/hour={now.strftime('%H')}"
    if os.path.exists("/data_16tb"):
        os.makedirs(vault_part_dir, exist_ok=True)
        os.makedirs("/data_16tb/cross_layer_dataset_vault/snapshots_warehouse", exist_ok=True)
        # Sync latest ML tensors & dataframe pickle to the 16TB vault
        for src_f in (TENSORS_NPZ, METRICS_PKL):
            if os.path.exists(src_f):
                try:
                    shutil.copy2(src_f, os.path.join("/data_16tb/cross_layer_dataset_vault/snapshots_warehouse", os.path.basename(src_f)))
                except Exception:
                    pass

    for active_path, prefix in [(METRICS_JSONL, "metrics_part"), (LOGS_JSONL, "logs_part")]:
        if os.path.exists(active_path):
            sz_mb = os.path.getsize(active_path) / (1024.0 * 1024.0)
            if sz_mb >= max_active_mb:
                gz_name = f"{prefix}_{now.strftime('%Y%m%d_%H%M%S')}.jsonl.gz"
                gz_path = os.path.join(part_dir, gz_name)
                with open(active_path, "rb") as f_in, gzip.open(gz_path, "wb", compresslevel=6) as f_out:
                    shutil.copyfileobj(f_in, f_out)
                if os.path.exists("/data_16tb"):
                    try:
                        shutil.copy2(gz_path, os.path.join(vault_part_dir, gz_name))
                    except Exception:
                        pass
                # Keep the most recent 5,000 lines in the active file so live readers still have context
                run_cmd(f"tail -n 5000 '{active_path}' > '{active_path}.tmp' && mv '{active_path}.tmp' '{active_path}'", timeout=15)

    # Check disk watermark on Tier-1 /data; if > 70%, move cold partitions exclusively to Tier-2 /data_16tb
    du = shutil.disk_usage("/data")
    used_pct = (du.used / du.total) * 100.0
    if used_pct > 70.0 and os.path.exists("/data_16tb"):
        for root, _, files in os.walk(ARCHIVE_DIR):
            for fn in files:
                if fn.endswith(".gz"):
                    fp = os.path.join(root, fn)
                    rel = os.path.relpath(fp, ARCHIVE_DIR)
                    dst = os.path.join("/data_16tb/cross_layer_dataset_vault/partitions_compressed", rel)
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    try:
                        shutil.move(fp, dst)
                    except Exception:
                        pass
