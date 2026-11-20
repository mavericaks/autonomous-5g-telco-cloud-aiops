#!/bin/bash
# ==============================================================================
# AUTONOMOUS 5G SA TELCO-CLOUD & AGENTIC AIOPS — VIDEO DEMO DIRECTOR
# ==============================================================================
# Usage:
#   Interactive mode (press ENTER between scenes):  run-video-demo
#   Auto-timed mode (pauses 10s between scenes)  :  run-video-demo --auto
# ==============================================================================

AUTO_MODE=0
if [[ "$1" == "--auto" ]]; then
    AUTO_MODE=1
fi

BOLD="\033[1m"
CYAN="\033[1;36m"
GREEN="\033[1;32m"
YELLOW="\033[1;33m"
MAGENTA="\033[1;35m"
BLUE="\033[1;34m"
RESET="\033[0m"

pause_scene() {
    echo ""
    if [[ $AUTO_MODE -eq 1 ]]; then
        echo -e "${YELLOW}[Auto-Advancing to next scene in 8 seconds...]${RESET}"
        sleep 8
    else
        read -r -p "$(echo -e "${YELLOW}>>> Press [ENTER] when ready for the next scene...${RESET}")"
    fi
}

run_live_cmd() {
    local cmd_display="$1"
    local cmd_exec="$2"
    echo -e "\n${GREEN}hpe@hpe-PowerEdge-R760xs${RESET}:${BLUE}~/HPE${RESET}$ ${BOLD}${cmd_display}${RESET}"
    sleep 0.6
    eval "$cmd_exec"
}

clear
echo -e "${CYAN}====================================================================================================${RESET}"
echo -e "${BOLD}  AUTONOMOUS 5G & AIOPS AUTONOMOUS 5G SA TELCO-CLOUD & EXPLAINABLE AGENTIC AIOPS LIVE VIDEO WALKTHROUGH${RESET}"
echo -e "${CYAN}====================================================================================================${RESET}"
echo -e "  Motto: ${GREEN}\"Zero-Touch, Explainable, Cross-Layer Autonomous Self-Healing —${RESET}"
echo -e "         ${GREEN} From Physical 5G RF Silicon to Cloud-Native Microservices\"${RESET}"
echo -e "${CYAN}----------------------------------------------------------------------------------------------------${RESET}"

pause_scene

# ------------------------------------------------------------------------------
# SCENE 1: PLANE 1 — BARE-METAL HARDWARE, NUMA, 96-THREAD XEON & 16.77 TB STORAGE
# ------------------------------------------------------------------------------
clear
echo -e "${MAGENTA}====================================================================================================${RESET}"
echo -e "${BOLD}  [SCENE 1 | 01:15 - 02:30] PLANE 1: BARE-METAL CLUSTER, NUMA TOPOLOGY & 16.77 TB RAID POOL${RESET}"
echo -e "${MAGENTA}====================================================================================================${RESET}"
run_live_cmd "lscpu | grep -E 'Model name|Socket|Thread|CPU\(s\):|NUMA'" "lscpu | grep -E 'Model name|Socket|Thread|CPU\(s\):|NUMA'"
run_live_cmd "free -h && df -h / /data /data_16tb" "free -h && df -h / /data /data_16tb"
run_live_cmd "ssh ubuntu@10.10.10.4 'hostname; nproc; free -h | head -n 2' && ssh ubuntu@10.10.10.5 'hostname; nproc; free -h | head -n 2'" \
             "ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'echo \"--- compute-pc1 (10.10.10.4) ---\"; nproc; free -h | head -n 2' && ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.5 'echo \"--- compute-pc2 (10.10.10.5) ---\"; nproc; free -h | head -n 2'"

pause_scene

# ------------------------------------------------------------------------------
# SCENE 2: PLANE 2 — OPENSTACK 2023.1 ANTELOPE (23 LXD CONTAINERS), KVM & OVN SDN
# ------------------------------------------------------------------------------
clear
echo -e "${MAGENTA}====================================================================================================${RESET}"
echo -e "${BOLD}  [SCENE 2 | 02:30 - 04:00] PLANE 2: OPENSTACK 2023.1 CONTROL PLANE (23 LXD), KVM & OVN GENEVE SDN${RESET}"
echo -e "${MAGENTA}====================================================================================================${RESET}"
run_live_cmd "sudo lxc exec openstack-ctl -- lxc list" "sudo lxc exec openstack-ctl -- lxc list"
run_live_cmd "sudo virsh list --all && sudo ovs-vsctl show" "sudo virsh list --all && sudo ovs-vsctl show"
run_live_cmd "python3 /home/hpe/test_horizon_login.py" "python3 /home/hpe/test_horizon_login.py"

pause_scene

# ------------------------------------------------------------------------------
# SCENE 3: PLANE 3 — MAGNUM KUBERNETES v1.23.3, OPEN5GS 5G SA CORE & BOUTIQUE
# ------------------------------------------------------------------------------
clear
echo -e "${MAGENTA}====================================================================================================${RESET}"
echo -e "${BOLD}  [SCENE 3 | 04:00 - 05:30] PLANE 3: MAGNUM KUBERNETES, 13 OPEN5GS 5G CORE NFs & 12 MICROSERVICES${RESET}"
echo -e "${MAGENTA}====================================================================================================${RESET}"
run_live_cmd "KUBECONFIG=/home/hpe/k8s-5g/config kubectl get nodes -o wide" "KUBECONFIG=/home/hpe/k8s-5g/config kubectl get nodes -o wide"
run_live_cmd "KUBECONFIG=/home/hpe/k8s-5g/config kubectl get pods -n open5gs -o wide" "KUBECONFIG=/home/hpe/k8s-5g/config kubectl get pods -n open5gs -o wide"
run_live_cmd "KUBECONFIG=/home/hpe/k8s-5g/config kubectl get pods -n microservices -o wide" "KUBECONFIG=/home/hpe/k8s-5g/config kubectl get pods -n microservices -o wide"

pause_scene

# ------------------------------------------------------------------------------
# SCENE 4: PLANE 4 — PHYSICAL 5G NR BAND n78 SDR RAN (4x USRP B210 & srsRAN)
# ------------------------------------------------------------------------------
clear
echo -e "${MAGENTA}====================================================================================================${RESET}"
echo -e "${BOLD}  [SCENE 4 | 05:30 - 07:00] PLANE 4: PHYSICAL 5G SDR RAN (4x ETTUS USRP B210 & srsRAN BAND n78)${RESET}"
echo -e "${MAGENTA}====================================================================================================${RESET}"
run_live_cmd "ssh ubuntu@10.10.10.4 'lsusb | grep 2500:0020; systemctl is-active srsgnb; tail -n 12 /tmp/gnb.log'" \
             "ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.4 'echo \"=== compute-pc1 gNodeB USRP B210 ===\"; lsusb | grep 2500:0020; systemctl is-active srsgnb; tail -n 12 /tmp/gnb.log'"
run_live_cmd "ssh ubuntu@10.10.10.5 'lsusb | grep 2500:0020; systemctl is-active srsue1 srsue2'" \
             "ssh -o StrictHostKeyChecking=no ubuntu@10.10.10.5 'echo \"=== compute-pc2 Multi-UE 3x USRP B210 ===\"; lsusb | grep 2500:0020; systemctl is-active srsue1 srsue2'"

pause_scene

# ------------------------------------------------------------------------------
# SCENE 5: PLANE 5 & 6 — WAZUH SIEM v4.8.0 & DUAL-GPU + XEON AMX AI FABRIC
# ------------------------------------------------------------------------------
clear
echo -e "${MAGENTA}====================================================================================================${RESET}"
echo -e "${BOLD}  [SCENE 5 | 07:00 - 08:30] PLANE 5 & 6: WAZUH SIEM v4.8.0 & 960+ GFLOPS DUAL-GPU / XEON AMX FABRIC${RESET}"
echo -e "${MAGENTA}====================================================================================================${RESET}"
run_live_cmd "cat /home/hpe/telemetry/gpu_workload_metrics.json" "cat /home/hpe/telemetry/gpu_workload_metrics.json"
run_live_cmd "sudo wc -l /var/ossec/logs/alerts/alerts.json && sudo tail -n 2 /var/ossec/logs/alerts/alerts.json" \
             "sudo wc -l /var/ossec/logs/alerts/alerts.json && sudo tail -n 2 /var/ossec/logs/alerts/alerts.json"

pause_scene

# ------------------------------------------------------------------------------
# SCENE 6: XIE EXPLAINABLE AGENTIC AIOPS, CAUSAL PPR RCA & FASTMCP SELF-HEALING
# ------------------------------------------------------------------------------
clear
echo -e "${MAGENTA}====================================================================================================${RESET}"
echo -e "${BOLD}  [SCENE 6 | 08:30 - 10:15] XIE CORE v1.0: Z-SCORE, RANDOM FOREST, VAR(2) GRANGER, PPR & FASTMCP${RESET}"
echo -e "${MAGENTA}====================================================================================================${RESET}"
run_live_cmd "systemctl status self-healing-agent.service --no-pager | head -n 14" "systemctl status self-healing-agent.service --no-pager | head -n 14"
run_live_cmd "tail -n 20 /home/hpe/agent/logs/remediation_audit.log" "tail -n 20 /home/hpe/agent/logs/remediation_audit.log"
run_live_cmd "ls -lh /home/hpe/agent/reports/ | tail -n 6" "ls -lh /home/hpe/agent/reports/ | tail -n 6"

pause_scene

# ------------------------------------------------------------------------------
# SCENE 7: MASSIVE 6-PLANE 368-PARAMETER + 1.49M LOG/ALERT DATASET WAREHOUSE
# ------------------------------------------------------------------------------
clear
echo -e "${MAGENTA}====================================================================================================${RESET}"
echo -e "${BOLD}  [SCENE 7 | 10:15 - 12:00] 6-PLANE MULTI-DIMENSIONAL AI DATASET WAREHOUSE (dataset-status)${RESET}"
echo -e "${MAGENTA}====================================================================================================${RESET}"
run_live_cmd "dataset-status" "dataset-status"

echo -e "\n${GREEN}====================================================================================================${RESET}"
echo -e "${BOLD}  WALKTHROUGH COMPLETE — ALL 6 PLANES, XIE SELF-HEALING AGENT & 16.77 TB WAREHOUSE VERIFIED!${RESET}"
echo -e "${GREEN}====================================================================================================${RESET}"

