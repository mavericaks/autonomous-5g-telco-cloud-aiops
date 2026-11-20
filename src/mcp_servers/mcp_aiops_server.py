#!/usr/bin/env python3
"""
MCP-AIOps Server - Experiential Intelligence & Causal Operations Endpoint
Integrates Neural Granger Causal Discovery DAG, Personalized PageRank RCA, ChromaDB Episodic Memory,
and real-time telco/cloud telemetry streaming.
Exposes tools: get_live_telemetry, query_causal_dag, perform_causal_rca, query_episodic_memory, get_healing_audit_log
"""
import sys
import os
import json
import logging
from pathlib import Path

# Add /home/hpe to sys.path for xie package imports
sys.path.append("/home/hpe")

from xie.causal_rca import PersonalizedPageRankRCA
from xie.episodic_memory import IncidentEpisodicMemory

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp-aiops")

TELEMETRY_JSONL = "/home/hpe/telemetry/dataset/5g_telco_metrics.jsonl"
CAUSAL_DAG_JSON = "/home/hpe/xie/models/causal_dag.json"
AUDIT_LOG_PATH = "/home/hpe/agent/logs/remediation_audit.log"

class AIOpsManager:
    def __init__(self):
        self.rca_engine = None
        self.memory = None
        self._init_models()

    def _init_models(self):
        try:
            if os.path.exists(CAUSAL_DAG_JSON):
                self.rca_engine = PersonalizedPageRankRCA(dag_path=CAUSAL_DAG_JSON)
            else:
                logger.warning(f"Causal DAG not found at {CAUSAL_DAG_JSON}")
        except Exception as e:
            logger.error(f"Failed to initialize RCA engine: {e}")

        try:
            self.memory = IncidentEpisodicMemory()
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB memory: {e}")

    def get_live_telemetry(self, limit: int = 5) -> list:
        """Fetch latest records from the live telemetry stream"""
        records = []
        if not os.path.exists(TELEMETRY_JSONL):
            return records
        try:
            with open(TELEMETRY_JSONL, "r", encoding="utf-8") as f:
                # Read last lines efficiently
                lines = f.readlines()
                for line in reversed(lines[-limit*2:]):
                    if not line.strip():
                        continue
                    try:
                        record = json.loads(line)
                        records.append(record)
                        if len(records) >= limit:
                            break
                    except Exception:
                        continue
        except Exception as e:
            logger.error(f"Error reading telemetry: {e}")
        return records

    def query_causal_dag(self) -> dict:
        """Return the active Granger Causal Discovery DAG"""
        if not os.path.exists(CAUSAL_DAG_JSON):
            return {"error": "Causal DAG file does not exist"}
        try:
            with open(CAUSAL_DAG_JSON, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            return {"error": str(e)}

    def perform_causal_rca(self, symptoms: dict = None) -> dict:
        """
        Run Personalized PageRank over the reversed Causal DAG.
        symptoms: dict of metric deviations, e.g. {"dropped_packets": 3.8, "latency_ms": 2.1}
        """
        if not self.rca_engine:
            return {"error": "RCA engine not initialized"}

        # If no symptoms provided, sample from the latest telemetry
        if not symptoms:
            latest = self.get_live_telemetry(limit=1)
            if latest:
                symptoms = {
                    "dropped_packets": latest[0].get("dropped_packets", 0),
                    "latency_ms": latest[0].get("latency_ms", 10.0),
                    "prach_sinr": latest[0].get("prach_sinr", 25.0)
                }
            else:
                symptoms = {"dropped_packets": 1.0}

        try:
            rca_result = self.rca_engine.analyze(symptoms)
            return {
                "input_symptoms": symptoms,
                "rca_result": rca_result
            }
        except Exception as e:
            return {"error": f"RCA computation failed: {e}"}

    def query_episodic_memory(self, symptom_text: str = "high packet drop on ovn geneve overlay", similarity_threshold: float = 0.5) -> dict:
        """Query ChromaDB episodic memory for past similar incidents and playbooks"""
        if not self.memory:
            return {"error": "Episodic memory not initialized"}
        try:
            match = self.memory.query_nearest_incident(symptom_text, similarity_threshold=similarity_threshold)
            return match if match else {"match": False, "message": "No episodes found"}
        except Exception as e:
            return {"error": f"Vector query failed: {e}"}

    def get_healing_audit_log(self, limit: int = 10) -> list:
        """Fetch the latest closed-loop self-healing events from audit log"""
        events = []
        if not os.path.exists(AUDIT_LOG_PATH):
            return events
        try:
            with open(AUDIT_LOG_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    line = line.strip()
                    if line:
                        events.append(line)
                    if len(events) >= limit:
                        break
        except Exception as e:
            logger.error(f"Error reading audit log: {e}")
        return events

def run_test():
    mgr = AIOpsManager()
    print("=" * 60)
    print("MCP-AIOps Self-Test & Diagnostic Audit")
    print("=" * 60)

    print("\n[*] Latest 5G Telco/Cloud Telemetry:")
    tel = mgr.get_live_telemetry(limit=2)
    for t in tel:
        print(f"  - [{t.get('timestamp')}] SNR: {t.get('prach_sinr')} dB, Loss: {t.get('dropped_packets')} pkts, Latency: {t.get('latency_ms')} ms, Fault: {t.get('fault_label', 'none')}")

    print("\n[*] Causal Discovery DAG Summary:")
    dag = mgr.query_causal_dag()
    print(f"Nodes ({len(dag.get('nodes', []))}): {dag.get('nodes')}")
    print(f"Directed Edges ({len(dag.get('edges', []))}): {dag.get('edges')[:4]}...")

    print("\n[*] Personalized PageRank Causal RCA (Test Injection: dropped_packets=4.2, latency_ms=3.1):")
    rca = mgr.perform_causal_rca(symptoms={"dropped_packets": 4.2, "latency_ms": 3.1})
    print(json.dumps(rca, indent=2))

    print("\n[*] ChromaDB Episodic Memory Query ('ovn geneve overlay packet loss'):")
    ep = mgr.query_episodic_memory("ovn geneve overlay packet loss", similarity_threshold=0.3)
    print(f"  - Match: {ep.get('match')}, Incident: {ep.get('incident_id')}, Similarity: {ep.get('similarity')}")
    print(f"    Root Cause: {ep.get('root_cause')}, Playbook: {ep.get('recommended_action')}")

    print("\n[*] Closed-Loop Self-Healing Audit Log:")
    audit = mgr.get_healing_audit_log(limit=3)
    for entry in audit:
        print(f"  - {entry}")

def run_stdio():
    mgr = AIOpsManager()
    logger.info("mcp-aiops JSON-RPC server listening on stdio...")
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {"name": "get_live_telemetry", "description": "Get latest live telco and cloud infrastructure telemetry metrics"},
                            {"name": "query_causal_dag", "description": "Get active Granger Causal Discovery DAG nodes and directed causal weights"},
                            {"name": "perform_causal_rca", "description": "Run Personalized PageRank Root Cause Analysis over causal graph for given symptoms"},
                            {"name": "query_episodic_memory", "description": "Query ChromaDB vector memory for past historical incidents and resolution playbooks"},
                            {"name": "get_healing_audit_log", "description": "Fetch closed-loop self-healing execution audit records and MTTR/MTTD metrics"}
                        ]
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})
                if tool_name == "get_live_telemetry":
                    res = mgr.get_live_telemetry(limit=args.get("limit", 5))
                elif tool_name == "query_causal_dag":
                    res = mgr.query_causal_dag()
                elif tool_name == "perform_causal_rca":
                    res = mgr.perform_causal_rca(symptoms=args.get("symptoms"))
                elif tool_name == "query_episodic_memory":
                    res = mgr.query_episodic_memory(symptom_text=args.get("symptom_text", "packet loss"), n_results=args.get("n_results", 3))
                elif tool_name == "get_healing_audit_log":
                    res = mgr.get_healing_audit_log(limit=args.get("limit", 10))
                else:
                    res = {"error": f"Unknown tool {tool_name}"}
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": req.get("id") if 'req' in locals() else None, "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        run_stdio()
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_test()
    else:
        if sys.stdin.isatty():
            run_test()
        else:
            run_stdio()
