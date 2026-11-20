# Physical Switch, Juniper SRX300 Hardware Firewall, VLAN 10 & VLAN 20 Master Configuration Reference

This document and directory (`configs/switch_firewall_vlans/`) preserve the complete hardware switching, 802.1Q VLAN trunking (`VLAN 10` & `VLAN 20`), Juniper SRX300 security gateway (`10.0.0.1`), Mist Enterprise Wi-Fi AP43 (`VLAN 20`), Open vSwitch (`br-data`, `br-ex`, `br-int`), and OVN Geneve (`UDP 6081` + BFD) configurations for the testbed.

---

## 1. Dual-VLAN Architecture (`VLAN 10` Infrastructure vs. `VLAN 20` Operations)

| Parameter | `VLAN 10` (Undercloud / SDN / Control / PXE) | `VLAN 20` (Operations / External Provider / Wi-Fi) |
| :--- | :--- | :--- |
| **802.1Q VLAN ID** | `10` | `20` |
| **IPv4 Subnet / CIDR** | `10.10.10.0/24` | `10.0.0.0/24` (and OpenStack Provider `172.24.4.0/24`) |
| **Default Gateway** | `10.10.10.1` / `10.10.10.2` (Dell R760xs `br-data`) | `10.0.0.1` (Juniper SRX300 Hardware Firewall) |
| **Dell R760xs Interfaces** | `enp171s0f0np0` / `eno8303.10` $\rightarrow$ OVS/Linux Bridge `br-data` (`10.10.10.2/24`, `10.10.10.1/24`) | `eno8303` (`10.0.0.10/24`) & OVS Provider Bridge `br-ex` (`veth-br` $\leftrightarrow$ `veth-host` `172.24.4.254/24`) |
| **`compute-pc1` Interfaces** | `enp1s0` (`10.10.10.4/24`, MAC `00:e0:21:84:f3:5c`) | Routed via `10.10.10.2` / OVN Geneve tunnel `ovn-8cf746-0` |
| **`compute-pc2` Interfaces** | `enp1s0` (`10.10.10.5/24`, MAC `00:e0:21:84:f3:61`) | Dual-Homed Wireless NIC `wlp2s0` (`10.0.0.24/24`) connected to Mist AP43 on `VLAN 20` |
| **Windows Jump Host** | Routed via `10.0.0.10` / `10.0.0.1` | `10.0.0.21/24` (Wazuh Agent `004` + Ollama `qwen3:14b` `:11434`) |
| **Attached Control VMs & Containers** | `juju-ctrl` (`10.10.10.1`), `openstack-ctl` (`10.10.10.3`), `funny-stag` (`10.10.10.16`), `on-ram` (`10.10.10.19`), `netbox-server` (`10.10.10.220`), 23 Juju LXD containers (`10.10.10.6`–`10.10.10.210`) | Magnum Kubernetes Floating IPs: `master-0` (`10.0.0.215`), `node-0` (`10.0.0.206`), `node-1` (`10.0.0.232`) |
| **Encapsulation & Traffic Type** | OVN Geneve (`UDP 6081`) with BFD (`UDP 3784`), MySQL InnoDB replication, RabbitMQ, Juju, MAAS PXE | North-South HTTP/HTTPS Dashboards (Horizon `:80`, Wazuh `:443`, Grafana `:3000`, Prometheus `:9090`), Juniper SRX Syslog (`UDP 514`), Mist Wi-Fi client traffic |
| **Kernel Proxy-ARP Policy** | **`net.ipv4.conf.br-data.proxy_arp = 0`** (Strictly disabled on `br-data` to prevent L2 ARP hijacking between Juju LXD containers) | `net.ipv4.conf.eno8303.proxy_arp = 1` (Enabled on external uplink `eno8303` for Floating IP visibility) |

---

## 2. Managed L2/L3 802.1Q Switch Configuration (`switch_vlan10_vlan20.conf`)

```ios
! ==============================================================================
! ENTERPRISE L2/L3 MANAGED SWITCH — 802.1Q VLAN 10 & VLAN 20 CONFIGURATION
! ==============================================================================
vlan 10
 name INFRA_UNDERCLOUD_SDN_VLAN10
!
vlan 20
 name OPS_EXTERNAL_WIFI_VLAN20
!
! --- Port 1: Trunk Uplink to Juniper SRX300 Hardware Firewall (10.0.0.1) ---
interface GigabitEthernet1/0/1
 description "802.1Q Trunk to Juniper SRX300 Security Gateway (ge-0/0/1)"
 switchport mode trunk
 switchport trunk native vlan 20
 switchport trunk allowed vlan 10,20
 spanning-tree portfast trunk
 no shutdown
!
! --- Port 2: Trunk Uplink to Dell PowerEdge R760xs Primary NIC (eno8303) ---
interface GigabitEthernet1/0/2
 description "802.1Q Trunk to Dell PowerEdge R760xs eno8303 (10.0.0.10 / VLAN 20 + VLAN 10)"
 switchport mode trunk
 switchport trunk native vlan 20
 switchport trunk allowed vlan 10,20
 spanning-tree portfast trunk
 no shutdown
!
! --- Port 3: Dedicated VLAN 10 Data/Underlay Link to Dell R760xs (enp171s0f0np0 -> br-data) ---
interface GigabitEthernet1/0/3
 description "VLAN 10 Data Underlay to Dell PowerEdge R760xs br-data (10.10.10.2)"
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
!
! --- Port 4: VLAN 10 Access Port to Compute Node 1 (compute-pc1 10.10.10.4) ---
interface GigabitEthernet1/0/4
 description "VLAN 10 Underlay & OVN Geneve Endpoint — compute-pc1 (10.10.10.4)"
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
!
! --- Port 5: VLAN 10 Access Port to Compute Node 2 (compute-pc2 10.10.10.5) ---
interface GigabitEthernet1/0/5
 description "VLAN 10 Underlay & OVN Geneve Endpoint — compute-pc2 (10.10.10.5)"
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown
!
! --- Port 6: VLAN 20 Access Port to Mist AP43 Enterprise Wi-Fi 6 Access Point ---
interface GigabitEthernet1/0/6
 description "VLAN 20 Wireless Operations — Mist AP43 (SSID: 5G-AIOps-Lab, No DHCP on VLAN 20)"
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 no shutdown
!
! --- Port 7: VLAN 20 Access Port to Windows Jump Host & Ollama LLM Server (10.0.0.21) ---
interface GigabitEthernet1/0/7
 description "VLAN 20 Operations & Ollama Qwen3-14B Host (10.0.0.21)"
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 no shutdown
```

---

## 3. Juniper SRX300 Hardware Security Gateway Configuration (`juniper_srx300.conf`)

```junos
## =============================================================================
## JUNIPER SRX300 HARDWARE FIREWALL & SECURITY GATEWAY (10.0.0.1) — JUNOS CONFIG
## =============================================================================
system {
    host-name edge-juniper-srx300;
    syslog {
        /* Streams real-time RT_FLOW & security events over UDP 514 to Wazuh SIEM on Dell (10.0.0.10) */
        host 10.0.0.10 {
            any any;
            security info;
            interactive-commands info;
            match "RT_FLOW|RT_IDS|RT_SCREEN|UI_AUTH";
            port 514;
            structured-data;
        }
    }
}
interfaces {
    ge-0/0/0 {
        description "WAN Uplink (Untrust Zone)";
        unit 0 {
            family inet {
                dhcp;
            }
        }
    }
    ge-0/0/1 {
        description "802.1Q Trunk to Managed Switch (VLAN 10 & VLAN 20)";
        flexible-vlan-tagging;
        native-vlan-id 20;
        unit 10 {
            description "VLAN 10 Infrastructure / Undercloud Subnet (10.10.10.0/24)";
            vlan-id 10;
            family inet {
                address 10.10.10.254/24;
            }
        }
        unit 20 {
            description "VLAN 20 Operations / External Provider / Wi-Fi Subnet (10.0.0.0/24)";
            vlan-id 20;
            family inet {
                address 10.0.0.1/24;
            }
        }
    }
}
routing-options {
    static {
        /* Route OpenStack Provider (172.24.4.0/24) & Tenant K8s (192.168.100.0/24) via Dell R760xs (10.0.0.10) */
        route 172.24.4.0/24 next-hop 10.0.0.10;
        route 192.168.100.0/24 next-hop 10.0.0.10;
        route 10.45.0.0/16 next-hop 10.0.0.10;
    }
}
security {
    log {
        mode stream;
        format sd-syslog;
        source-address 10.0.0.1;
        stream wazuh-siem {
            category all;
            host {
                10.0.0.10;
                port 514;
            }
        }
    }
    nat {
        source {
            rule-set trust-to-untrust {
                from zone [ trust-vlan20 infra-vlan10 ];
                to zone untrust;
                rule snat-internet {
                    match {
                        source-address [ 10.0.0.0/24 10.10.10.0/24 172.24.4.0/24 192.168.100.0/24 ];
                    }
                    then {
                        source-nat {
                            interface;
                        }
                    }
                }
            }
        }
    }
    zones {
        security-zone trust-vlan20 {
            host-inbound-traffic {
                system-services { all; }
                protocols { all; }
            }
            interfaces {
                ge-0/0/1.20;
            }
        }
        security-zone infra-vlan10 {
            host-inbound-traffic {
                system-services { all; }
                protocols { all; }
            }
            interfaces {
                ge-0/0/1.10;
            }
        }
        security-zone untrust {
            screen untrust-screen;
            interfaces {
                ge-0/0/0.0 {
                    host-inbound-traffic {
                        system-services { dhcp; ping; }
                    }
                }
            }
        }
    }
    policies {
        from-zone trust-vlan20 to-zone infra-vlan10 {
            policy allow-ops-to-infra {
                match { source-address any; destination-address any; application any; }
                then { permit; log { session-init; session-close; } }
            }
        }
        from-zone infra-vlan10 to-zone trust-vlan20 {
            policy allow-infra-to-ops {
                match { source-address any; destination-address any; application any; }
                then { permit; log { session-init; session-close; } }
            }
        }
        from-zone trust-vlan20 to-zone untrust {
            policy allow-wan-egress {
                match { source-address any; destination-address any; application any; }
                then { permit; log { session-close; } }
            }
        }
        from-zone infra-vlan10 to-zone untrust {
            policy allow-infra-wan-egress {
                match { source-address any; destination-address any; application any; }
                then { permit; log { session-close; } }
            }
        }
    }
}
```

---

## 4. OVS / OVN Geneve SDN & BFD Encapsulation Fix (`VLAN 10` Underlay)

To ensure OVN Geneve tunnels (`UDP 6081`) and BFD health checks (`UDP 3784`) between the Dell Controller (`10.10.10.1` / `10.10.10.2`), `compute-pc1` (`10.10.10.4`), and `compute-pc2` (`10.10.10.5`) bind strictly to the `VLAN 10` underlay (`10.10.10.0/24`) rather than the `VLAN 20` interface (`10.0.0.10`):

```bash
# On Dell PowerEdge R760xs:
sudo ovs-vsctl set open . external-ids:ovn-encap-ip="10.10.10.1"
sudo ovs-vsctl set open . external-ids:ovn-encap-type="geneve"

# On compute-pc1 (10.10.10.4):
sudo ovs-vsctl set open . external-ids:ovn-encap-ip="10.10.10.4"
sudo ovs-vsctl set open . external-ids:ovn-encap-type="geneve"

# On compute-pc2 (10.10.10.5):
sudo ovs-vsctl set open . external-ids:ovn-encap-ip="10.10.10.5"
sudo ovs-vsctl set open . external-ids:ovn-encap-type="geneve"
```

