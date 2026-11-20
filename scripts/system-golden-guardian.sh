#!/bin/bash
# ==============================================================================
# AUTONOMOUS 5G TELCO-CLOUD & AIOPS — JUNIOR-PROOF GOLDEN STATE GUARDIAN
# ==============================================================================
# Runs continuously (every 60s) via system-golden-guardian.service and at boot.
# Automatically heals network bridges, proxy-ARP settings, iptables NAT rules,
# kubeconfig paths, KVM virtual machines, LXD containers, and systemd daemons
# if anyone accidentally stops or misconfigures a component.
# ==============================================================================

heal_iteration() {
    # 1. Ensure storage pools are mounted
    mount -a 2>/dev/null || true

    # 2. Ensure veth-host (172.24.4.254/24) <-> veth-br (OVS br-ex) floating IP router link is UP
    if ! ip link show veth-host >/dev/null 2>&1; then
        ip link add veth-host type veth peer name veth-br 2>/dev/null || true
    fi
    if ! ip addr show dev veth-host 2>/dev/null | grep -q "172.24.4.254/24"; then
        ip addr add 172.24.4.254/24 dev veth-host 2>/dev/null || true
    fi
    ip link set veth-host up 2>/dev/null || true
    ip link set veth-br up 2>/dev/null || true
    ovs-vsctl --may-exist add-br br-ex 2>/dev/null || true
    ovs-vsctl --may-exist add-port br-ex veth-br 2>/dev/null || true

    # 3. Ensure loopback aliases for gateway proxy endpoints
    for ip_cidr in "10.228.0.92/32" "10.0.0.215/32" "10.0.0.206/32" "10.0.0.232/32"; do
        if ! ip addr show dev lo | grep -q "${ip_cidr%/*}"; then
            ip addr add "$ip_cidr" dev lo 2>/dev/null || true
        fi
    done

    # 4. Enforce kernel sysctl & proxy_arp=0 on br-data (prevents Horizon ARP hijack)
    sysctl -w net.ipv4.ip_forward=1 >/dev/null 2>&1 || true
    sysctl -w net.ipv4.conf.br-data.proxy_arp=0 >/dev/null 2>&1 || true
    sysctl -w net.ipv4.conf.all.proxy_arp=0 >/dev/null 2>&1 || true
    sysctl -w net.ipv4.conf.default.proxy_arp=0 >/dev/null 2>&1 || true

    # 5. Enforce iptables NAT MASQUERADE for OpenStack provider & tenant networks
    if ! iptables -t nat -C POSTROUTING -s 172.24.4.0/24 ! -d 172.24.4.0/24 -j MASQUERADE 2>/dev/null; then
        iptables -t nat -A POSTROUTING -s 172.24.4.0/24 ! -d 172.24.4.0/24 -j MASQUERADE 2>/dev/null || true
    fi
    if ! iptables -t nat -C POSTROUTING -s 192.168.100.0/24 ! -d 192.168.100.0/24 -j MASQUERADE 2>/dev/null; then
        iptables -t nat -A POSTROUTING -s 192.168.100.0/24 ! -d 192.168.100.0/24 -j MASQUERADE 2>/dev/null || true
    fi

    # 6. Run OpenStack Horizon FDB/ARP Guard
    if [[ -x /usr/local/bin/openstack-horizon-guard.sh ]]; then
        /usr/local/bin/openstack-horizon-guard.sh >/dev/null 2>&1 || true
    fi

    # 7. Ensure kubeconfig is synced for user hpe and root
    if [[ -f /home/hpe/k8s-5g/config ]]; then
        mkdir -p /home/hpe/.kube /root/.kube
        cp -u /home/hpe/k8s-5g/config /home/hpe/.kube/config 2>/dev/null || true
        chown hpe:hpe /home/hpe/.kube/config 2>/dev/null || true
        cp -u /home/hpe/k8s-5g/config /root/.kube/config 2>/dev/null || true
    fi

    # 8. Ensure KVM virtual machines (Magnum K8s nodes) are running
    for dom in instance-00000006 instance-00000007 instance-00000008; do
        state=$(virsh domstate "$dom" 2>/dev/null | tr -d '[:space:]')
        if [[ "$state" == "shutoff" || "$state" == "paused" ]]; then
            virsh start "$dom" >/dev/null 2>&1 || true
        fi
    done

    # 9. Ensure critical systemd services on Dell R760xs are active
    for svc in omni-crosslayer-harvester.service \
               self-healing-agent.service \
               multi-domain-exporter.service \
               grafana-prometheus.service \
               5g-telemetry.service \
               mcp-dcops.service \
               mcp-devops.service \
               mcp-secops.service \
               mcp-aiops.service \
               wazuh-manager.service \
               wazuh-indexer.service \
               wazuh-dashboard.service \
               apache2.service \
               nova-compute.service \
               ovn-controller.service; do
        if ! systemctl is-active --quiet "$svc"; then
            systemctl start "$svc" 2>/dev/null || true
        fi
    done

    # 10. Ensure srsRAN and monitor dashboard services on compute-pc1 & compute-pc2 stay active
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 ubuntu@10.10.10.4 \
        "sudo systemctl is-active --quiet srsgnb || sudo systemctl start srsgnb; sudo systemctl is-active --quiet node-monitor-tty1 || sudo systemctl start node-monitor-tty1" >/dev/null 2>&1 || true
    ssh -o StrictHostKeyChecking=no -o ConnectTimeout=2 ubuntu@10.10.10.5 \
        "sudo systemctl is-active --quiet srsue1 || sudo systemctl start srsue1; sudo systemctl is-active --quiet srsue2 || sudo systemctl start srsue2; sudo systemctl is-active --quiet node-monitor-tty1 || sudo systemctl start node-monitor-tty1" >/dev/null 2>&1 || true
}

if [[ "$1" == "--once" ]]; then
    heal_iteration
    exit 0
fi

while true; do
    heal_iteration
    sleep 60
done

