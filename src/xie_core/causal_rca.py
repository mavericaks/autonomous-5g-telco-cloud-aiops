#!/usr/bin/env python3
"""
Experiential Intelligence Engine (XIE Core) - Personalized PageRank Causal RCA
Propagates anomaly activations backwards through the Causal DAG using Personalized PageRank (PPR).
Attributes root causes by stationary distribution probability (SDP) and ranks top-3 root causes.
"""
import os
import json
import logging
import numpy as np
import networkx as nx
from typing import Dict, List, Tuple, Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("xie.causal_rca")

DAG_FILEPATH = "/home/hpe/xie/models/causal_dag.json"

ROOT_CAUSE_MAPPINGS = {
    "healthy_pod_count": {
        "fault_domain": "k8s_container",
        "description": "Kubernetes Open5GS container or pod termination failure",
        "recommended_action": "k8s_rollout_restart"
    },
    "pod_restart_count": {
        "fault_domain": "k8s_container",
        "description": "Kubernetes pod crashing / CrashLoopBackOff",
        "recommended_action": "k8s_rollout_restart"
    },
    "cpu_load_pct": {
        "fault_domain": "compute_resource",
        "description": "Compute node CPU resource exhaustion or starvation",
        "recommended_action": "throttle_traffic_and_isolate_core"
    },
    "prach_sinr": {
        "fault_domain": "rf_physical_layer",
        "description": "Physical RF path loss or RF gain attenuation on USRP B210",
        "recommended_action": "recalibrate_rf_attenuation_and_power"
    },
    "cqi": {
        "fault_domain": "ran_channel_quality",
        "description": "5G NR Radio Channel Quality Indicator degradation",
        "recommended_action": "recalibrate_rf_attenuation_and_power"
    },
    "dropped_packets": {
        "fault_domain": "sdn_overlay_network",
        "description": "OVN SDN overlay packet loss or Geneve tunnel degradation",
        "recommended_action": "tc_qdisc_del_reset"
    },
    "latency_ms": {
        "fault_domain": "sdn_overlay_network",
        "description": "OVN SDN transport delay or buffer queuing latency",
        "recommended_action": "tc_qdisc_del_reset"
    }
}

class PersonalizedPageRankRCA:
    def __init__(self, dag_path=DAG_FILEPATH):
        self.dag_path = dag_path
        self.dag = None
        self.rev_dag = None
        self.nodes = []
        self._load_dag()

    def _load_dag(self):
        if not os.path.exists(self.dag_path):
            raise FileNotFoundError(f"Causal DAG not found at {self.dag_path}")
        with open(self.dag_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.nodes = data.get("nodes", [])
        G = nx.DiGraph()
        for n in self.nodes:
            G.add_node(n)
        for e in data.get("edges", []):
            G.add_edge(e["source"], e["target"], weight=float(e.get("weight", 1.0)))

        self.dag = G
        # Reversed DAG: edges point from effect back to cause
        self.rev_dag = G.reverse()
        logger.info(f"Loaded Causal DAG with {len(self.nodes)} nodes and {G.number_of_edges()} edges.")

    def analyze(self, anomaly_dict: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Calculates Root Cause probabilities given metric anomaly activations.
        anomaly_dict: e.g. {"dropped_packets": 35.0, "latency_ms": 85.0} (severity/activation values)
        """
        # Build teleport personalization vector
        personalization = {}
        total_act = 0.0
        for node in self.nodes:
            val = abs(float(anomaly_dict.get(node, 0.0)))
            personalization[node] = val
            total_act += val

        if total_act <= 1e-6:
            # Uniform prior if no anomalous metric specified
            for node in self.nodes:
                personalization[node] = 1.0 / len(self.nodes)
        else:
            for node in self.nodes:
                personalization[node] = personalization[node] / total_act

        # Compute PageRank on reversed causal graph
        pagerank_scores = nx.pagerank(
            self.rev_dag,
            alpha=0.85,
            personalization=personalization,
            weight="weight",
            max_iter=200
        )

        ranked = sorted(pagerank_scores.items(), key=lambda x: x[1], reverse=True)
        results = []
        for metric, score in ranked[:3]:
            meta = ROOT_CAUSE_MAPPINGS.get(metric, {
                "fault_domain": "unknown",
                "description": f"Metric {metric} anomaly",
                "recommended_action": "diagnose_system"
            })
            results.append({
                "root_cause_metric": metric,
                "confidence_score": round(float(score), 4),
                "fault_domain": meta["fault_domain"],
                "description": meta["description"],
                "recommended_action": meta["recommended_action"]
            })

        return results

if __name__ == "__main__":
    rca = PersonalizedPageRankRCA()
    # Test case 1: SDN delay and packet drop
    test_sdn = {"latency_ms": 120.0, "dropped_packets": 45.0}
    print("\n--- Test RCA: SDN Overlay Latency & Drop ---")
    res1 = rca.analyze(test_sdn)
    for r in res1:
        print(f"  Confidence: {r['confidence_score']*100:.1f}% -> [{r['fault_domain']}] {r['root_cause_metric']} (Action: {r['recommended_action']})")

    # Test case 2: RF SINR drop
    test_rf = {"prach_sinr": 15.0, "cqi": 10.0}
    print("\n--- Test RCA: RF Channel Degradation ---")
    res2 = rca.analyze(test_rf)
    for r in res2:
        print(f"  Confidence: {r['confidence_score']*100:.1f}% -> [{r['fault_domain']}] {r['root_cause_metric']} (Action: {r['recommended_action']})")

    # Test case 3: Pod crash
    test_k8s = {"healthy_pod_count": 50.0, "pod_restart_count": 30.0}
    print("\n--- Test RCA: Kubernetes Pod Crash ---")
    res3 = rca.analyze(test_k8s)
    for r in res3:
        print(f"  Confidence: {r['confidence_score']*100:.1f}% -> [{r['fault_domain']}] {r['root_cause_metric']} (Action: {r['recommended_action']})")

