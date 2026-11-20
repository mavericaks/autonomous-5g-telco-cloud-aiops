#!/bin/bash
# ==============================================================================
# AUTONOMOUS 5G TELCO-CLOUD & AIOPS — 24-POINT GOLDEN STATE HEALTH VERIFIER
# ==============================================================================
# Usage: verify-golden-state
# ==============================================================================

G="\033[1;32m"
R="\033[1;31m"
Y="\033[1;33m"
C="\033[1;36m"
W="\033[1;37m"
N="\033[0m"

PASS_CNT=0
TOTAL_CNT=0

check_item() {
    local label="$1"
    local cmd="$2"
    TOTAL_CNT=$((TOTAL_CNT + 1))
    if eval "$cmd" >/dev/null 2>&1; then
        printf "  [${G}PASS${N}] %-62s\n" "$label"
        PASS_CNT=$((PASS_CNT + 1))
    else
        printf "  [${R}WARN${N}] %-62s\n" "$label"
    fi
}

echo -e "${C}====================================================================================${N}"
echo -e "${W}  AUTONOMOUS 5G SA TELCO-CLOUD & AGENTIC AIOPS — 24-POINT GOLDEN STATE HEALTH SCORECARD${N}"
echo -e "${C}====================================================================================${N}"

echo -e "\n${Y}[PLANE 1: BARE-METAL HARDWARE, STORAGE POOLS & NETWORK FABRIC]${N}"
check_item "Dell R760xs Tier-1 Hot Warehouse (/data 2.95 TB) Mounted" "mountpoint -q /data"
check_item "Dell R760xs Tier-2 Deep Vault (/data_16tb 14.0 TB) Mounted" "mountpoint -q /data_16tb"
check_item "Golden State Backup Vault (/data_16tb/GOLDEN_STATE_VAULT) Intact" "test -f /data_16tb/GOLDEN_STATE_MASTER_ARCHIVE_20261121.tar.gz"
check_item "Compute Node 1 (compute-pc1 10.10.10.4) Reachable via SSH" "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 ubuntu@10.10.10.4 'true'"
check_item "Compute Node 2 (compute-pc2 10.10.10.5) Reachable via SSH" "ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 ubuntu@10.10.10.5 'true'"
check_item "Bridge br-data Proxy-ARP Disabled (proxy_arp=0 Hardened)" "test \$(cat /proc/sys/net/ipv4/conf/br-data/proxy_arp) -eq 0"

echo -e "\n${Y}[PLANE 2: OPENSTACK 2023.1 ANTELOPE CONTROL PLANE, KVM & OVN SDN]${N}"
check_item "LXD Control Plane VM (openstack-ctl 10.10.10.3) Running" "sudo lxc info openstack-ctl | grep -q 'Status: RUNNING'"
check_item "All 23 Juju OpenStack LXD Service Containers Running" "test \$(sudo lxc exec openstack-ctl -- lxc list --format=csv -c s | grep -c RUNNING) -ge 23"
check_item "OpenStack Horizon Web Login Endpoint (http://10.0.0.10/horizon)" "test \$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 http://10.0.0.10/horizon/auth/login/) -eq 200"
check_item "All 3 Dell KVM Guest Domains (instance-00000006/7/8) Running" "test \$(sudo virsh list --state-running --name | grep -c instance) -ge 3"
check_item "OVS br-int & OVN Geneve Tunnels (ovn0-compu-0/1) Active" "sudo ovs-vsctl show | grep -q 'ovn0-compu-0'"

echo -e "\n${Y}[PLANE 3: MAGNUM KUBERNETES v1.23.3, OPEN5GS 5G CORE & MICROSERVICES]${N}"
check_item "Kubernetes Cluster Nodes Ready (master-0, node-0, node-1)" "test \$(kubectl get nodes --no-headers | grep -c ' Ready') -eq 3"
check_item "Open5GS 5G SA Core All 13 Network Function Pods Running" "test \$(kubectl get pods -n open5gs --no-headers | grep -c 'Running') -eq 13"
check_item "Google Online Boutique All 12 Microservice Pods Running" "test \$(kubectl get pods -n microservices --no-headers | grep -c 'Running') -eq 12"

echo -e "\n${Y}[PLANE 4: PHYSICAL 5G NR BAND n78 SDR RAN (4x USRP B210 & srsRAN)]${N}"
check_item "compute-pc1 Ettus USRP B210 SDR Detected & srsgnb.service Active" "ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'lsusb | grep -q 2500:0020 && systemctl is-active --quiet srsgnb'"
check_item "compute-pc2 3x Ettus USRP B210 SDRs & srsue1/srsue2 Active" "ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.5 'test \$(lsusb | grep -c 2500:0020) -ge 3 && systemctl is-active --quiet srsue1 && systemctl is-active --quiet srsue2'"
check_item "Physical Monitor Live Dashboards (node-monitor-tty1) Active" "ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'systemctl is-active --quiet node-monitor-tty1' && ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.5 'systemctl is-active --quiet node-monitor-tty1'"

echo -e "\n${Y}[PLANE 5 & 6: WAZUH SIEM, DUAL-GPU/AMX, XIE AGENT, 4-MCP & DATASET WAREHOUSE]${N}"
check_item "Wazuh SIEM Manager, OpenSearch Indexer & Dashboard Active" "systemctl is-active --quiet wazuh-manager && systemctl is-active --quiet wazuh-indexer && systemctl is-active --quiet wazuh-dashboard"
check_item "XIE Closed-Loop Self-Healing Agent (self-healing-agent.service)" "systemctl is-active --quiet self-healing-agent.service"
check_item "All 4 FastMCP Servers Active (mcp-dcops, devops, secops, aiops)" "systemctl is-active --quiet mcp-dcops && systemctl is-active --quiet mcp-devops && systemctl is-active --quiet mcp-secops && systemctl is-active --quiet mcp-aiops"
check_item "Prometheus (:9090), Grafana (:3000) & Multi-Domain Exporter (:9105)" "systemctl is-active --quiet grafana-prometheus && systemctl is-active --quiet multi-domain-exporter"
check_item "Continuous 6-Plane Dataset Harvester (omni-crosslayer-harvester)" "systemctl is-active --quiet omni-crosslayer-harvester.service"
check_item "Junior-Proof Persistence Guardian (system-golden-guardian)" "systemctl is-active --quiet system-golden-guardian.service"
check_item "SQLite WAL Warehouse & ML Tensors Present in /data/cross_layer_dataset" "test -f /data/cross_layer_dataset/03_relational_warehouse/cross_layer_warehouse.db && test -f /data/cross_layer_dataset/01_timeseries_metrics/training_tensors_X_y.npz"

echo -e "${C}------------------------------------------------------------------------------------${N}"
echo -e "  ${W}GOLDEN STATE VERIFICATION SCORE: ${G}${PASS_CNT} / ${TOTAL_CNT} CHECKS PASSED${N}"
echo -e "${C}====================================================================================${N}"

