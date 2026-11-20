#!/bin/bash
# ==============================================================================
# AUTONOMOUS 5G TELCO-CLOUD & AIOPS — ONE-CLICK GOLDEN STATE RESTORE ENGINE
# ==============================================================================
# Usage:
#   sudo restore-golden-state
# Restores code, models, ChromaDB memory, systemd unit files, kubeconfig,
# network bridges, proxy-ARP settings, Horizon FDB/ARP tables, and restarts all
# critical services from the immutable vault at /data_16tb/GOLDEN_STATE_VAULT.
# ==============================================================================

set -e
VAULT="/data_16tb/GOLDEN_STATE_VAULT"

if [[ ! -d "$VAULT" ]]; then
    echo "[ERROR] Golden State Vault not found at $VAULT"
    exit 1
fi

echo "===================================================================================="
echo "  RESTORING AUTONOMOUS 5G TELCO-CLOUD & AGENTIC AIOPS TO VERIFIED GOLDEN STATE..."
echo "===================================================================================="

echo "[1/6] Restoring XIE Core, ChromaDB Vector Memory, Trained ML Models & Agent Scripts..."
cp -rf "${VAULT}/05_aiops_xie_mcp_and_wazuh/xie" /home/hpe/
cp -rf "${VAULT}/05_aiops_xie_mcp_and_wazuh/agent" /home/hpe/
cp -rf "${VAULT}/05_aiops_xie_mcp_and_wazuh/mcp-dcops" /home/hpe/
cp -rf "${VAULT}/05_aiops_xie_mcp_and_wazuh/mcp-devops" /home/hpe/
cp -rf "${VAULT}/05_aiops_xie_mcp_and_wazuh/mcp-secops" /home/hpe/
cp -rf "${VAULT}/05_aiops_xie_mcp_and_wazuh/mcp-aiops" /home/hpe/
cp -rf "${VAULT}/05_aiops_xie_mcp_and_wazuh/central-agent" /home/hpe/
cp -f "${VAULT}/05_aiops_xie_mcp_and_wazuh/"*.py /home/hpe/ 2>/dev/null || true
chown -R hpe:hpe /home/hpe/xie /home/hpe/agent /home/hpe/mcp-* /home/hpe/central-agent

echo "[2/6] Restoring Dataset Harvester Scripts & Schema Governance..."
cp -rf "${VAULT}/06_golden_dataset_checkpoint/bin/"* /data/cross_layer_dataset/bin/ 2>/dev/null || true
cp -rf "${VAULT}/06_golden_dataset_checkpoint/04_schema_and_governance/"* /data/cross_layer_dataset/04_schema_and_governance/ 2>/dev/null || true
chown -R hpe:hpe /data/cross_layer_dataset/bin /data/cross_layer_dataset/04_schema_and_governance

echo "[3/6] Restoring Systemd Service Units & /usr/local/bin Utilities..."
cp -f "${VAULT}/05_aiops_xie_mcp_and_wazuh/systemd_units/"*.service /etc/systemd/system/ 2>/dev/null || true
cp -f "${VAULT}/05_aiops_xie_mcp_and_wazuh/usr_local_bin/"* /usr/local/bin/ 2>/dev/null || true
chmod +x /usr/local/bin/* 2>/dev/null || true
systemctl daemon-reload

echo "[4/6] Restoring Kubernetes kubeconfig & Verifying Open5GS / Online Boutique Deployments..."
mkdir -p /home/hpe/k8s-5g /home/hpe/.kube /root/.kube
cp -f "${VAULT}/04_kubernetes_5gcore_and_microservices/kubeconfig_golden.yaml" /home/hpe/k8s-5g/config
cp -f "${VAULT}/04_kubernetes_5gcore_and_microservices/kubeconfig_golden.yaml" /home/hpe/.kube/config
cp -f "${VAULT}/04_kubernetes_5gcore_and_microservices/kubeconfig_golden.yaml" /root/.kube/config
chown -R hpe:hpe /home/hpe/k8s-5g /home/hpe/.kube

echo "[5/6] Restoring Network Bridges, Proxy-ARP Guard, Iptables NAT, KVM VMs & All Services..."
/usr/local/bin/system-golden-guardian.sh --once

echo "[6/6] Running 24-Point Golden State Verification Scorecard..."
/usr/local/bin/verify-golden-state

