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
        echo -e "${W} AUTONOMOUS 5G TELCO-CLOUD NODE 2: compute-pc2 (10.10.10.5) | Role: 3x USRP 5G UEs + Nova KVM + GPU1${R}${CL}"
        echo -e "${C}==================================================================================================${R}${CL}"
        echo -e "${Y}[1] 3x ETTUS USRP B210 SDRs & NETWORK NAMESPACES:${R} netns=[ue1, ue2, ovnmeta] | $(date -u +"%H:%M:%S UTC")${CL}"
        lsusb | grep "2500:0020" | head -n 3 | awk "{print \"    \033[1;32m\" \$0 \"\033[0m\033[K\"}"
        echo -e "${Y}[2] ACTIVE SYSTEMD SERVICES (systemctl list-units --state=running):${R}${CL}"
        systemctl list-units --type=service --state=running --no-pager --no-legend | grep -E "srs|nova|ovn|wazuh|juju" | head -n 8 | awk "{printf \"    %-36s %-8s %-8s %s %s %s %s\033[K\n\", \$1, \$2, \$3, \$5, \$6, \$7, \$8}"
        echo -e "${Y}[3] OPENSTACK NOVA KVM INSTANCES (sudo virsh list --all):${R}${CL}"
        sudo virsh list --all | head -n 4 | sed "s/^/    /; s/$/\x1b[K/"
        echo -e "${Y}[4] OVS/OVN GENEVE SDN BRIDGE & BFD TUNNELS (sudo ovs-vsctl show):${R}${CL}"
        sudo ovs-vsctl show | grep -E "Bridge|Port|type: geneve|options:|bfd_status:|ovs_version" | head -n 11 | cut -c 1-94 | sed "s/^/  /; s/$/\x1b[K/"
        printf "\033[J"
    } >/dev/tty1
    sleep 2
done
