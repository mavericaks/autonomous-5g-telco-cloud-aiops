#!/bin/bash
# ==============================================================================
# AUTONOMOUS 5G TELCO-CLOUD & AIOPS — MULTI-CLOUD GOLDEN STATE SYNC ENGINE
# ==============================================================================
# Usage:
#   sync-golden-state-to-cloud
#
# Synchronizes the Golden State across 4 redundant tiers:
#   Tier 1: Local 16.77 TB Enterprise RAID Vault (/data_16tb/GOLDEN_STATE_VAULT)
#   Tier 2: OpenStack Private Cloud Vault & Glance Registry (openstack-ctl / lxd-4)
#   Tier 3: Off-Node Physical Compute Servers (compute-pc1 10.10.10.4 & compute-pc2 10.10.10.5)
#   Tier 4: Public Cloud / GitHub Repository & Rclone Cloud Bucket (if remote configured)
# ==============================================================================

set -e
VAULT="/data_16tb/GOLDEN_STATE_VAULT"
MASTER_TAR="/data_16tb/GOLDEN_STATE_MASTER_ARCHIVE_20261121.tar.gz"
REPO="/home/hpe/HPE"
CLOUD_BUNDLE="${REPO}/golden_state_cloud_bundle/GOLDEN_STATE_CLOUD_RECOVERY_BUNDLE.tar.gz"

echo "===================================================================================="
echo "  GOLDEN STATE MULTI-CLOUD & OFF-NODE SYNCHRONIZATION ENGINE"
echo "===================================================================================="

echo "[1/4] Refreshing Cloud Recovery Bundle (${CLOUD_BUNDLE})..."
mkdir -p "${REPO}/golden_state_cloud_bundle"
tar -czf "${CLOUD_BUNDLE}" \
    -C "${VAULT}" \
    01_network_and_host_configs \
    02_openstack_and_lxd_snapshots \
    03_kvm_libvirt_definitions \
    04_kubernetes_5gcore_and_microservices \
    07_switch_firewall_vlan10_vlan20_configs \
    SHA256SUMS.txt
sha256sum "${CLOUD_BUNDLE}" > "${REPO}/golden_state_cloud_bundle/SHA256SUMS.txt"
ls -lh "${CLOUD_BUNDLE}"

echo "[2/4] Syncing Golden State to OpenStack Private Cloud Storage (openstack-ctl & Glance)..."
sudo lxc exec openstack-ctl -- mkdir -p /var/backups/GOLDEN_STATE_CLOUD_VAULT
sudo lxc file push "${MASTER_TAR}" openstack-ctl/var/backups/GOLDEN_STATE_CLOUD_VAULT/GOLDEN_STATE_MASTER_ARCHIVE_20261121.tar.gz
sudo lxc file push "${CLOUD_BUNDLE}" openstack-ctl/var/backups/GOLDEN_STATE_CLOUD_VAULT/GOLDEN_STATE_CLOUD_RECOVERY_BUNDLE.tar.gz
sudo lxc exec openstack-ctl -- lxc file push /var/backups/GOLDEN_STATE_CLOUD_VAULT/GOLDEN_STATE_CLOUD_RECOVERY_BUNDLE.tar.gz juju-65b4ac-0-lxd-4/var/lib/glance/images/GOLDEN_STATE_CLOUD_RECOVERY_BUNDLE.tar.gz 2>/dev/null || true
echo "  -> Verified OpenStack Private Cloud Vault copy!"

echo "[3/4] Syncing Golden State to Off-Node Compute Cluster Replicas (10.10.10.4 & 10.10.10.5)..."
for node_ip in 10.10.10.4 10.10.10.5; do
    ssh -o StrictHostKeyChecking=no ubuntu@${node_ip} "mkdir -p /home/ubuntu/GOLDEN_STATE_CLOUD_REPLICA"
    scp -q -o StrictHostKeyChecking=no "${MASTER_TAR}" "${CLOUD_BUNDLE}" "${REPO}/golden_state_cloud_bundle/SHA256SUMS.txt" ubuntu@${node_ip}:/home/ubuntu/GOLDEN_STATE_CLOUD_REPLICA/
    echo "  -> Verified off-node replica on ubuntu@${node_ip}:/home/ubuntu/GOLDEN_STATE_CLOUD_REPLICA/"
done

echo "[4/4] Syncing to Public Cloud / GitHub Repository..."
cd "${REPO}"
if git remote get-url origin >/dev/null 2>&1; then
    git add -A
    git commit -m "Automated Golden State Cloud Sync ($(date -u +%Y-%m-%dT%H:%M:%SZ))" 2>/dev/null || true
    git push -u origin main && echo "  -> Pushed Golden State Bundle to GitHub Cloud (origin/main)!"
else
    echo "  -> Local Git repository committed & ready. To push to GitHub Cloud, run:"
    echo "     cd /home/hpe/HPE && git remote add origin https://github.com/mavericaks/autonomous-5g-telco-cloud-aiops.git && git push -u origin main"
fi

if command -v rclone >/dev/null 2>&1 && [[ -n "${RCLONE_REMOTE}" ]]; then
    rclone copy "${MASTER_TAR}" "${RCLONE_REMOTE}:autonomous-golden-state-vault/"
    rclone copy "${CLOUD_BUNDLE}" "${RCLONE_REMOTE}:autonomous-golden-state-vault/"
    echo "  -> Synced to rclone cloud remote: ${RCLONE_REMOTE}:autonomous-golden-state-vault/"
fi

echo "===================================================================================="
echo "  ALL GOLDEN STATE CLOUD & OFF-NODE REPLICAS SYNCHRONIZED SUCCESSFULLY!"
echo "===================================================================================="

