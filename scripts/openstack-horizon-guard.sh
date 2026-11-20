#!/bin/bash
# 1. Keep proxy_arp disabled on br-data and all (enabled ONLY on eno8303)
sysctl -w net.ipv4.conf.all.proxy_arp=0 >/dev/null 2>&1
sysctl -w net.ipv4.conf.br-data.proxy_arp=0 >/dev/null 2>&1
sysctl -w net.ipv4.conf.eno8303.proxy_arp=1 >/dev/null 2>&1

# 2. Keep permanent FDB and ARP entries locked for Horizon (10.10.10.8), Keystone (10.10.10.9), and MySQL (10.10.10.6)
lxc exec openstack-ctl -- bash -c '
bridge fdb replace 00:16:3e:0f:f8:c3 dev vethfad74b35 master br-enp5s0 permanent 2>/dev/null || true
bridge fdb replace 00:16:3e:66:ba:cb dev veth6d5ce9aa master br-enp5s0 permanent 2>/dev/null || true
bridge fdb replace 00:16:3e:70:e3:3c dev veth34a192ac master br-enp5s0 permanent 2>/dev/null || true

lxc exec juju-65b4ac-0-lxd-3 -- ip neigh replace 10.10.10.9 lladdr 00:16:3e:66:ba:cb dev eth0 nud permanent 2>/dev/null || true
lxc exec juju-65b4ac-0-lxd-3 -- ip neigh replace 10.10.10.6 lladdr 00:16:3e:0f:f8:c3 dev eth0 nud permanent 2>/dev/null || true
lxc exec juju-65b4ac-0-lxd-3 -- ip neigh replace 10.10.10.2 lladdr 04:32:01:ca:9f:50 dev eth0 nud permanent 2>/dev/null || true

lxc exec juju-65b4ac-0-lxd-2 -- ip neigh replace 10.10.10.8 lladdr 00:16:3e:70:e3:3c dev eth0 nud permanent 2>/dev/null || true
lxc exec juju-65b4ac-0-lxd-2 -- ip neigh replace 10.10.10.6 lladdr 00:16:3e:0f:f8:c3 dev eth0 nud permanent 2>/dev/null || true
lxc exec juju-65b4ac-0-lxd-2 -- ip neigh replace 10.10.10.2 lladdr 04:32:01:ca:9f:50 dev eth0 nud permanent 2>/dev/null || true

# 3. Ensure MySQL primary 10.10.10.6 is writable
RO=$(lxc exec juju-65b4ac-0-lxd-0 -- mysql --defaults-file=/etc/mysql/debian.cnf -N -e "SELECT @@super_read_only;" 2>/dev/null)
if [ "$RO" = "1" ]; then
    lxc exec juju-65b4ac-0-lxd-0 -- mysql --defaults-file=/etc/mysql/debian.cnf -e "SET GLOBAL super_read_only=OFF; SET GLOBAL read_only=OFF;" 2>/dev/null || true
fi
'
