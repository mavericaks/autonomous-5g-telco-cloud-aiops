#!/usr/bin/env python3
import json
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

print("Loading telemetry dataset from JSONL...")
df = pd.read_json('/home/hpe/telemetry/dataset/5g_telco_metrics.jsonl', lines=True)

# Unify columns
df['cpu_load_pct'] = df['cpu_load_pct'].fillna(df['controller_cpu_pct'])
df['healthy_pod_count'] = df['healthy_pod_count'].fillna(df['k8s_open5gs_pods_ready'])
df['prach_sinr'] = df['prach_sinr'].fillna(df['pusch_sinr_db'])
df['dropped_packets'] = df['dropped_packets'].fillna(0)
df['ue2_service_active'] = df['ue2_service_active'].fillna(1.0)
df['pusch_crc_ok'] = (df['pusch_crc_status'] == 'OK').astype(int)

feature_cols = [
    'cpu_load_pct',
    'controller_mem_pct',
    'healthy_pod_count',
    'amf_gnb_connected',
    'gnb_service_active',
    'ue1_service_active',
    'ue2_service_active',
    'prach_rssi_db',
    'prach_snr_db',
    'prach_ta_us',
    'prach_sinr',
    'dropped_packets',
    'pusch_crc_ok'
]

# Ensure no NaNs in features
X = df[feature_cols].fillna(0)
y = df['fault_label']

print(f"Dataset samples: {len(X)}")
print("Class breakdown:\n", y.value_counts())

# Train/Test Split (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(f"Training set: {len(X_train)} | Test set: {len(X_test)}")

# Train Random Forest with balanced class weights
clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)
clf.fit(X_train, y_train)

# Evaluation
y_pred = clf.predict(X_test)
print("\n=== CLASSIFICATION REPORT ===")
print(classification_report(y_test, y_pred, zero_division=0))

print("\n=== FEATURE IMPORTANCES ===")
importances = pd.Series(clf.feature_importances_, index=feature_cols).sort_values(ascending=False)
print(importances)

# Save model and feature metadata
model_path = '/home/hpe/agent/models/anomaly_detector.pkl'
joblib.dump(clf, model_path)
print(f"\nModel saved to {model_path}")

meta_path = '/home/hpe/agent/models/feature_metadata.json'
with open(meta_path, 'w') as f:
    json.dump({
        "features": feature_cols,
        "classes": clf.classes_.tolist(),
        "trained_samples": len(X),
        "test_accuracy": float(clf.score(X_test, y_test))
    }, f, indent=2)
print(f"Metadata saved to {meta_path}")

