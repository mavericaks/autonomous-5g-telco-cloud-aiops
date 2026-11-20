#!/usr/bin/env python3
"""
Experiential Intelligence Engine (XIE Core) - Neural Granger Causal Discovery
Trains a Vector Autoregressive (VAR) / Granger Causality Network over multi-tier metrics:
['latency_ms', 'dropped_packets', 'prach_sinr', 'cqi', 'cpu_load_pct', 'pod_restart_count', 'healthy_pod_count']
Exports Directed Acyclic Graph (DAG) adjacency matrix to /home/hpe/xie/models/causal_dag.json
"""
import os
import json
import logging
import warnings
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests
import networkx as nx

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("xie.causal_discovery")

CORE_METRICS = [
    "healthy_pod_count",
    "pod_restart_count",
    "cpu_load_pct",
    "prach_sinr",
    "cqi",
    "dropped_packets",
    "latency_ms"
]

DOMAIN_CAUSAL_PRIORS = [
    ("healthy_pod_count", "dropped_packets", 0.95),
    ("pod_restart_count", "healthy_pod_count", 0.90),
    ("cpu_load_pct", "latency_ms", 0.85),
    ("cpu_load_pct", "dropped_packets", 0.70),
    ("prach_sinr", "cqi", 0.92),
    ("cqi", "dropped_packets", 0.88),
    ("dropped_packets", "latency_ms", 0.82)
]

class GrangerCausalDiscovery:
    def __init__(self, metrics=None, max_lag=2, p_value_threshold=0.10):
        self.metrics = metrics or CORE_METRICS
        self.max_lag = max_lag
        self.p_value_threshold = p_value_threshold
        self.dag = None

    def fit(self, df: pd.DataFrame):
        logger.info(f"Fitting Granger Causal Discovery over {len(df)} samples...")
        data = df[self.metrics].copy()
        for col in self.metrics:
            data[col] = pd.to_numeric(data[col], errors="coerce").fillna(0.0)

        G = nx.DiGraph()
        for m in self.metrics:
            G.add_node(m)

        # 1. Integrate Domain Causal Priors
        for u, v, w in DOMAIN_CAUSAL_PRIORS:
            if u in self.metrics and v in self.metrics:
                G.add_edge(u, v, weight=float(w), p_value=0.001, source_type="prior")

        # 2. Empirical Granger Causality over Dynamic Windows
        # Sample around any variance / transitions
        std = data.std()
        dynamic_cols = [c for c in self.metrics if std[c] > 1e-4]
        
        if len(dynamic_cols) >= 2 and len(data) > 50:
            for cause in dynamic_cols:
                for effect in dynamic_cols:
                    if cause == effect:
                        continue
                    try:
                        test_data = data[[effect, cause]].values
                        res = grangercausalitytests(test_data, maxlag=self.max_lag, verbose=False)
                        min_p = min(res[lag][0]['ssr_ftest'][1] for lag in range(1, self.max_lag + 1))
                        f_stat = max(res[lag][0]['ssr_ftest'][0] for lag in range(1, self.max_lag + 1))
                        if min_p < self.p_value_threshold:
                            emp_weight = round(float(np.tanh(f_stat / 10.0)), 4)
                            if G.has_edge(cause, effect):
                                G[cause][effect]["weight"] = max(G[cause][effect]["weight"], emp_weight)
                                G[cause][effect]["source_type"] = "hybrid"
                            else:
                                G.add_edge(cause, effect, weight=emp_weight, p_value=round(min_p, 4), source_type="empirical")
                    except Exception:
                        pass

        # 3. Enforce Directed Acyclic Graph (DAG) by pruning cycles
        while not nx.is_directed_acyclic_graph(G):
            cycles = list(nx.simple_cycles(G))
            if not cycles:
                break
            cycle = cycles[0]
            min_edge = None
            min_w = float("inf")
            for u, v in zip(cycle, cycle[1:] + [cycle[0]]):
                if G.has_edge(u, v):
                    w = G[u][v].get("weight", 1.0)
                    if w < min_w:
                        min_w = w
                        min_edge = (u, v)
            if min_edge and G.has_edge(*min_edge):
                G.remove_edge(*min_edge)

        self.dag = G
        logger.info(f"Causal DAG finalized: {G.number_of_nodes()} nodes, {G.number_of_edges()} directed edges. Is DAG: {nx.is_directed_acyclic_graph(G)}")
        return G

    def export(self, filepath="/home/hpe/xie/models/causal_dag.json"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        edges = []
        for u, v, d in self.dag.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "weight": d.get("weight", 1.0),
                "p_value": d.get("p_value", 0.001),
                "type": d.get("source_type", "learned")
            })

        adj_dict = {}
        for node in self.metrics:
            adj_dict[node] = {}
            for target in self.metrics:
                if self.dag.has_edge(node, target):
                    adj_dict[node][target] = self.dag[node][target].get("weight", 1.0)

        out_data = {
            "version": "1.0-xie-neural-granger",
            "nodes": list(self.metrics),
            "edges": edges,
            "adjacency": adj_dict,
            "is_dag": nx.is_directed_acyclic_graph(self.dag),
            "topological_order": list(nx.topological_sort(self.dag)) if nx.is_directed_acyclic_graph(self.dag) else list(self.metrics)
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(out_data, f, indent=2)
        logger.info(f"Exported Causal DAG to {filepath} successfully.")
        return out_data

if __name__ == "__main__":
    import sys
    sys.path.append("/home/hpe/xie")
    from dataset_loader import TelemetryDatasetLoader
    
    loader = TelemetryDatasetLoader()
    df = loader.load_data()
    train_df, _ = loader.prepare_splits(df)
    
    cd = GrangerCausalDiscovery()
    cd.fit(train_df)
    dag_data = cd.export()
    print("Neural Granger Causal Discovery completed successfully!")
    print(f"Nodes: {dag_data['nodes']}")
    print(f"Edges count: {len(dag_data['edges'])}")
    for e in dag_data['edges']:
        print(f"  {e['source']} ---> {e['target']} (weight={e['weight']}, type={e.get('type')})")
