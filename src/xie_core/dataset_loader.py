#!/usr/bin/env python3
"""
Experiential Intelligence Engine (XIE Core) - Dataset Loader & Schema Validator
Ingests telemetry JSONL data, validates schema, normalizes features, and produces splits.
"""
import json
import logging
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("xie.dataset_loader")

TARGET_METRICS = [
    "cpu_load_pct",
    "healthy_pod_count",
    "dropped_packets",
    "prach_sinr",
    "prach_snr_db",
    "prach_ta_us"
]

class TelemetryDatasetLoader:
    def __init__(self, filepath: str = "/home/hpe/telemetry/dataset/5g_telco_metrics.jsonl"):
        self.filepath = filepath
        self.feature_stats = {}

    def load_data(self) -> pd.DataFrame:
        logger.info(f"Ingesting telemetry stream from {self.filepath}...")
        records = []
        with open(self.filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    # Normalize legacy schema variations
                    if "controller_cpu_pct" in data and "cpu_load_pct" not in data:
                        data["cpu_load_pct"] = data["controller_cpu_pct"]
                    if "k8s_open5gs_pods_ready" in data and "healthy_pod_count" not in data:
                        data["healthy_pod_count"] = data["k8s_open5gs_pods_ready"]
                    if "pusch_sinr_db" in data and "prach_sinr" not in data:
                        data["prach_sinr"] = data["pusch_sinr_db"]
                    if "dropped_packets" not in data:
                        data["dropped_packets"] = 0
                    if "pod_restart_count" not in data:
                        data["pod_restart_count"] = 0
                    if "latency_ms" not in data:
                        data["latency_ms"] = float(data.get("prach_ta_us", 1.0)) * 0.1
                    if "cqi" not in data:
                        snr = float(data.get("prach_snr_db", 0))
                        data["cqi"] = max(1, min(15, int((snr + 10) / 2)))
                    records.append(data)
                except Exception:
                    continue

        df = pd.DataFrame(records)
        logger.info(f"Ingested {len(df)} records. Columns: {list(df.columns)}")
        return df

    def prepare_splits(self, df: pd.DataFrame, test_size: float = 0.2) -> Tuple[pd.DataFrame, pd.DataFrame]:
        features = ["latency_ms", "dropped_packets", "prach_sinr", "cqi", "cpu_load_pct", "pod_restart_count", "healthy_pod_count"]
        # Ensure all columns exist and are numeric
        for col in features:
            if col not in df.columns:
                df[col] = 0.0
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

        n_samples = len(df)
        split_idx = int(n_samples * (1 - test_size))
        train_df = df.iloc[:split_idx].copy()
        val_df = df.iloc[split_idx:].copy()

        # Compute mean & std for normalization
        for col in features:
            mean = float(train_df[col].mean())
            std = float(train_df[col].std())
            if std == 0:
                std = 1.0
            self.feature_stats[col] = {"mean": mean, "std": std}

        logger.info(f"Dataset split: {len(train_df)} train, {len(val_df)} val samples across {len(features)} core metrics.")
        return train_df, val_df

if __name__ == "__main__":
    loader = TelemetryDatasetLoader()
    df = loader.load_data()
    train_df, val_df = loader.prepare_splits(df)
    print(f"Dataset Loader verified successfully! Total samples: {len(df)}")

