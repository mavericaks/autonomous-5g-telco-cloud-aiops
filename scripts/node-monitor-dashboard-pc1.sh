#!/bin/bash
export TERM=linux
setterm --blank 0 --powersave off --powerdown 0 --cursor off </dev/tty1 >/dev/tty1 2>/dev/null || true
setterm --blank poke </dev/tty1 >/dev/tty1 2>/dev/null || true
chvt 1 2>/dev/null || true

C="\033[1;36m"
G="\033[1;32m"
Y="\033[1;33m"
W="\033[1;37m"
R="\033[0m"
CL="\033[K"

printf "\033[2J" >/dev/tty1
while true; do
    {
        printf "\033[H"
        echo -e "${C}==================================================================================================${R}${CL}"
        echo -e "${W} AUTONOMOUS 5G TELCO-CLOUD NODE 1: compute-pc1 (10.10.10.4) | Role: 5G gNodeB + Nova KVM + GPU0${R}${CL}"
        echo -e "${C}==================================================================================================${R}${CL}"
        echo -e "${Y}[1] HOST & USRP B210 SDR:${R} Ubuntu 22.04.5 LTS | i9-14900K (32T) | 62GiB RAM | $(date -u +"%H:%M:%S UTC")${CL}"
        lsusb | grep "2500:0020" | head -n 1 | awk "{print \"    \033[1;32m\" \$0 \"\033[0m\033[K\"}"
        echo -e "${Y}[2] ACTIVE SYSTEMD SERVICES (systemctl list-units --state=running):${R}${CL}"
        systemctl list-units --type=service --state=running --no-pager --no-legend | grep -E "srs|nova|ovn|wazuh|juju" | head -n 7 | awk "{printf \"    %-36s %-8s %-8s %s %s %s %s\033[K\n\", \$1, \$2, \$3, \$5, \$6, \$7, \$8}"
        echo -e "${Y}[3] OPENSTACK NOVA KVM INSTANCES (sudo virsh list --all):${R}${CL}"
        sudo virsh list --all | head -n 4 | sed "s/^/    /; s/$/\x1b[K/"
        echo -e "${Y}[4] OVS/OVN GENEVE SDN BRIDGE & BFD TUNNELS (sudo ovs-vsctl show):${R}${CL}"
        sudo ovs-vsctl show | grep -E "Bridge|Port|type: geneve|options:|bfd_status:|ovs_version" | head -n 10 | cut -c 1-94 | sed "s/^/  /; s/$/\x1b[K/"
        echo -e "${Y}[5] LIVE 5G NR BAND n78 gNodeB PHY/MAC STREAM (tail -n 4 /tmp/gnb.log):${R}${CL}"
        tail -n 4 /tmp/gnb.log 2>/dev/null | cut -c 1-94 | awk "{print \"  \033[1;36m\" \$0 \"\033[0m\033[K\"}"
        printf "\033[J"
    } >/dev/tty1
    sleep 2
done
