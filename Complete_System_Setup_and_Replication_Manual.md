# Complete System Setup, Architecture & Step-by-Step Replication Manual
## Autonomous Cross-Layer 5G SA Telco-Cloud, Distributed Dual-GPU/AMX Compute, Wazuh SIEM & Explainable Agentic AIOps Testbed

---

## 1. Executive Vision, Motto, Purpose & Strategic Use Cases

### 1.1 Project Motto
> ***"Zero-Touch, Explainable, Cross-Layer Autonomous Self-Healing — From Physical 5G RF Silicon to Cloud-Native Microservices."***

### 1.2 Vision & Purpose
Modern 5G Standalone (SA) Telco-Cloud infrastructures are no longer monolithic hardware appliances; they are deeply layered, disaggregated cyber-physical systems spanning **six interdependent operational planes**:
1. **Plane 1 — Bare-Metal Hardware, NUMA & Linux Kernel Fabric** (Dual-socket Xeon servers, edge compute nodes, NVMe/enterprise storage, and multi-homing NICs).
2. **Plane 2 — OpenStack Cloud Control Plane, KVM Hypervisors & OVN/OVS Geneve SDN** (23 containerized OpenStack services, libvirt/KVM virtual machines, and encapsulated Geneve overlay tunnels).
3. **Plane 3 — Cloud-Native Kubernetes, 5G SA Core & Microservices** (Magnum Fedora CoreOS nodes, 13 Open5GS 3GPP Release-17 5G Core Network Functions, and 12 cloud-native e-commerce microservices).
4. **Plane 4 — Physical 5G SDR Radio Access Network (RAN) & Enterprise Wireless** (4x Ettus Research USRP B210 Software-Defined Radios operating on 5G NR Band n78 TDD at 3879.42 MHz with `srsRAN` gNodeB and UEs, plus Mist Enterprise Wi-Fi and Juniper SRX300 WAN routing).
5. **Plane 5 — Cyber-Physical Security Operations (SecOps) & Compliance** (Wazuh SIEM v4.8.0 Manager, OpenSearch Indexer, multi-node endpoint agents, File Integrity Monitoring, CIS benchmarks, and MITRE ATT&CK threat detection).
6. **Plane 6 — Distributed AI Compute & Explainable Agentic AIOps** (Dual Intel UHD Graphics 770 GPUs + Dual Intel Xeon Gold 5418Y AVX-512/AMX engines, Ollama `qwen3:14b` LLM, and the **Experiential Intelligence Engine [XIE]**).

#### Why This System Was Built (The Core Industry Problem)
In production telco clouds, a single physical or virtual fault—such as an OVN Geneve tunnel packet-loss spike on `br-int` or an RF path-loss attenuation event on a USRP B210 antenna—propagates vertically and horizontally within milliseconds. It triggers a **cascading alarm storm** across Kubernetes probes, 5G AMF/UPF SCTP/GTP-U tunnels, and application frontends.
- **Legacy Rule/Threshold Systems** fail because they treat every downstream symptom as an independent fault, triggering conflicting remediations.
- **Black-Box Deep Learning Models** fail in mission-critical telco operations because network engineers cannot trust or audit unexplainable neural activations before executing destructive control-plane actions.

#### Our Solution
We engineered a **complete, end-to-end physical 5G SA Telco-Cloud testbed** paired with a **mathematically explainable, closed-loop Agentic AIOps architecture (XIE Core v1.0)** that:
1. Continuously harvests **368 cross-layer telemetry parameters** and **all logs, alerts, and events** across all 6 planes every 5.0 seconds (`omni-crosslayer-harvester.service`).
2. Detects anomalies in real time using **Rolling Z-Score Statistical Filters + 100-Tree Random Forest Ensembles** ($99.97\%$ classification accuracy).
3. Resolves recurring incidents in **$< 100\text{ ms}$** via **Zero-Shot Episodic Vector Memory (ChromaDB HNSW cosine similarity $\ge 0.92$)**.
4. Disentangles novel multi-layer cascading alarm storms using **Time-Lagged VAR(2) Granger Causal Discovery** and **Reversed-DAG Personalized PageRank ($\boldsymbol{\pi}$)** ($98.33\%$ root-cause localization accuracy).
5. Executes deterministic, guardrailed self-healing actions via **4 Domain-Specific Model Context Protocol (FastMCP) Servers**, achieving an overall **Mean Time To Remediate (MTTR) of $0.354\text{ seconds}$** (a **$99.97\%$ reduction** compared to manual NOC workflows).
6. Synthesizes human-readable executive post-mortem reports asynchronously via **Ollama `qwen3:14b`**.

---

### 1.3 Core Use Cases Implemented & Validated

| Use Case ID | Use Case Title | Problem Addressed | How Our Setup Solves It | Quantified Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **UC-1** | **Autonomous 5G RAN RF Attenuation Recovery** | Physical obstruction, interference, or gain drift degrades PUSCH/PDSCH SINR and causes UE RRC drops. | `XIE-Agent` detects `p4_ran_pusch_sinr_db` drop, localizes root cause to USRP RF plane via PPR, and invokes `RAN-MCP` to recalibrate USRP B210 TX/RX gains (`+6 dB`). | **MTTR = 0.435 s** (100% UE session retention) |
| **UC-2** | **OVN/OVS Geneve SDN Impairment Remediation** | Overlay tunnel packet loss/jitter on `br-int` degrades K8s pod-to-pod and 5G N2/N3 traffic, masquerading as a 5G Core failure. | VAR(2) Granger + Reversed-DAG PPR traces downstream AMF/UPF symptoms back to `ovn0-compu-*` tunnel drops and resets Linux `tc qdisc` / OVS flows via `Cloud-MCP`. | **MTTR = 0.382 s** ($98.33\%$ cascading RCA accuracy) |
| **UC-3** | **5G Core & Cloud-Native Pod Crash Recovery** | Container OOM/crash in Open5GS (`upf`/`amf`/`smf`) or Online Boutique (`frontend`/`checkoutservice`) breaks user sessions. | Detects `p3_open5gs_pods_ready < 13`, isolates failing deployment, executes `kubectl rollout restart` via `K8s-MCP`, and verifies readiness probes. | **MTTR = 0.091 s** (Zero manual intervention) |
| **UC-4** | **Compute Node CPU Starvation Mitigation** | Runaway compute threads or noisy-neighbor workloads saturate host cores on `compute-pc1`/`pc2` or Dell hypervisor. | Identifies `p1_dell_load_1m` / `p1_pc1_cpu_util_pct` excursion, isolates offending processes, and rebalances CPU affinity/cgroups. | **MTTR = 0.371 s** |
| **UC-5** | **Cyber-Physical SecOps & SIEM Active Response** | Unauthorized SSH brute-force, privilege escalation (`sudo`), or configuration tampering across cloud/RAN nodes. | Wazuh SIEM v4.8.0 correlates logs across agents `000`–`004` against MITRE ATT&CK tactics (`T1078`) and triggers automated active response & alert indexing. | **412,000+ alerts** indexed & correlated in real time |
| **UC-6** | **Massive 6-Plane Multi-Dimensional AI Dataset Factory** | Researchers and ML models lack synchronized cross-layer datasets combining RF PHY, 5G Core, K8s, OpenStack SDN, OS kernel, and SIEM logs. | `omni-crosslayer-harvester.service` streams **368 parameters** + **all 6 planes of logs/alerts** every 5s into JSONL, CSV, Pandas `.pkl`, NumPy `.npz`, and SQLite WAL on a 2.9 TB volume. | **10,030+ instances** (`3.69M+` cells) & **42,500+ log/alert events** |

---

## 2. Complete Hardware, Network & Software Bill of Materials (BoM)

### 2.1 Physical Cluster Nodes & Hardware Inventory

| Node Hostname | Management IP | Data / VLAN 10 IP | Hardware Specifications | Operating System | Assigned Architectural Roles |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`hpe-PowerEdge-R760xs`** | `10.0.0.10` (`eno8303`) | `10.10.10.2` (`br-data`) | Dual Intel Xeon Gold 5418Y (48C/96T, AVX-512 & AMX), **503 GiB DDR5 ECC RAM** (2 NUMA nodes), `438 GB` OS SSD (`/dev/sdb2`) + **`2.9 TB` Enterprise Data Array** (`/dev/sda1` mounted at `/data`) | Ubuntu 22.04.5 LTS (Kernel `6.8.0-87-generic`) | OpenStack Control Plane Host (`openstack-ctl`), Primary KVM Hypervisor (3 K8s VMs), OVN/OVS SDN Hub, Wazuh SIEM Manager (`000`), Prometheus/Grafana Server, Xeon AMX Worker (544.7 GFLOPS), XIE Self-Healing Agent, Omni Dataset Warehouse |
| **`compute-pc1.maas`** | `10.0.0.x` | `10.10.10.4` | Intel Core i7-13700 (16C/24T), **64 GiB RAM**, **Intel UHD Graphics 770 GPU (`GPU0` `/dev/dri/renderD128`, PCI `8086:a780`)**, USB 3.0 Controller | Ubuntu 22.04 LTS | OpenStack Nova KVM Compute Node 1, **5G srsRAN gNodeB Host**, **1x Ettus USRP B210 SDR (`serial=34B18C8`)**, Distributed AI Tensor Worker (`GPU0`, 204.6 GFLOPS), Wazuh Agent `002` |
| **`compute-pc2.maas`** | `10.0.0.x` | `10.10.10.5` | Intel Core i7-13700 (16C/24T), **64 GiB RAM**, **Intel UHD Graphics 770 GPU (`GPU1` `/dev/dri/renderD128`, PCI `8086:a780`)**, USB 3.0 Controller | Ubuntu 22.04 LTS | OpenStack Nova KVM Compute Node 2, **5G srsRAN Multi-UE Host (`ue1`, `ue2`, `ue3`)**, **3x Ettus USRP B210 SDRs (`34B18A2`, `34B1905`, USRP #3)**, Distributed AI Tensor Worker (`GPU1`, 204.6 GFLOPS), Wazuh Agent `003` |
| **`windows-jump-host`** | `10.0.0.21` | Routed via `10.0.0.10` | Dedicated Workstation with Discrete GPU Acceleration | Windows 11 Pro | **Ollama `qwen3:14b` LLM Inference Server (`:11434`)**, Wazuh SIEM Agent `004`, Operator Administration Console |
| **Ettus USRP B210 (x4)** | USB 3.0 Bus (`2500:0020`) | RF Band n78 (`3879.42 MHz`) | Analog Devices AD9361 2x2 MIMO RFIC (`70 MHz–6 GHz`, up to `56 MHz` BW, Dual Channels RF-A & RF-B) | UHD v4.x FPGA Firmware | 1x 5G NR gNodeB Base Station (`compute-pc1`) + 3x 5G NR User Equipment Terminals (`compute-pc2`), **8 Active RF Chains Total** |
| **Juniper SRX300 & Mist AP43** | `10.0.0.1` | VLAN 10 / VLAN 20 | Enterprise Security Gateway & Wi-Fi 6 Cloud-Managed Access Point | Junos OS / Mist Firmware | L3 Inter-VLAN Routing, WAN Gateway, and Enterprise Wireless Telemetry (`SSID: 5G-AIOps-Lab`) |

---

### 2.2 Multi-Layer Network Subnets, Bridges & Routing Topology

| Network Plane | Subnet / CIDR | Bridge / Interface | Gateway / Key IPs | Purpose & Encapsulation |
| :--- | :--- | :--- | :--- | :--- |
| **Management & Campus LAN** | `10.0.0.0/24` | `eno8303` (Dell) | Gateway `10.0.0.1` (Juniper SRX300), Dell `10.0.0.10`, Jump Host `10.0.0.21` | External dashboard access (Horizon `:80`, Grafana `:3000`, Prometheus `:9090`, Wazuh `:5601`, Ollama `:11434`) |
| **OpenStack Data & SDN Underlay (VLAN 10)** | `10.10.10.0/24` | `br-data` (`eno8303` / `enp171s0f0np0`) | `10.10.10.2` (Dell), `10.10.10.3` (`openstack-ctl`), `10.10.10.4` (`compute-pc1`), `10.10.10.5` (`compute-pc2`), `10.10.10.6`–`210` (23 Juju LXD containers) | Juju OpenStack control plane communication, OVN Geneve tunnel endpoints (`ovn0-compu-0`, `ovn0-compu-1`), SSH management |
| **OpenStack External Provider Floating IP Network** | `172.24.4.0/24` | `br-ex` $\leftrightarrow$ `veth-br` / `veth-host` | `172.24.4.254` (Dell host router), `172.24.4.1` (OVN router gateway), `172.24.4.20`–`232` (VM Floating IPs) | North-South NAT connectivity between physical hosts and OpenStack tenant VMs |
| **OpenStack Tenant Private Network (`k8s-net`)** | `192.168.100.0/24` | OVS `br-int` (Geneve VNI) | `192.168.100.72` (`k8s-master-0`), `192.168.100.131` (`k8s-node-0`), `192.168.100.174` (`k8s-node-1`) | Internal East-West network for Magnum Kubernetes nodes and Open5GS N2 NGAP (`:38412`) / N3 GTP-U (`:2152`) |
| **Kubernetes Pod Overlay (Flannel VXLAN)** | `10.100.0.0/16` | `flannel.1` / `cni0` | `10.100.0.0/24` (`master-0`), `10.100.1.0/24` (`node-0`), `10.100.2.0/24` (`node-1`) | Pod-to-pod communication across all 13 Open5GS NFs and 12 Online Boutique microservices |
| **5G UE PDU Session Pool (`ogstun`)** | `10.45.0.0/16` | `ogstun` (inside `open5gs-upf`) | `10.45.0.1` (UPF Gateway), `10.45.0.2` (`srsue1`), `10.45.0.3` (`srsue2`), `10.45.0.4` (`srsue3`) | End-to-end 3GPP 5G User Plane IP tunnel for attached USRP B210 User Equipment |

---

### 2.3 OpenStack 2023.1 Antelope Control Plane Inventory (23 Juju LXD Containers in `openstack-ctl`)

All 23 OpenStack control-plane microservices run as isolated LXD containers inside the `openstack-ctl` VM (`10.10.10.3`):

| Container Name | Service Role | IP Address | Key Ports | Description |
| :--- | :--- | :--- | :--- | :--- |
| `juju-65b4ac-0-lxd-0` | `mysql-innodb-cluster/1` | `10.10.10.17` | `3306`, `33060` | MySQL 8.0 InnoDB Cluster Secondary Read-Replica |
| `juju-65b4ac-0-lxd-1` | `rabbitmq-server/0` | `10.10.10.22` | `5672`, `15672` | AMQP Message Broker for Nova, Neutron, Heat, Octavia, Magnum |
| `juju-65b4ac-0-lxd-2` | `keystone/0` | `10.10.10.9` | `5000` | OpenStack Identity Service v3 (Fernet Tokens) |
| `juju-65b4ac-0-lxd-3` | `openstack-dashboard/0` | `10.10.10.8` | `80`, `443` | OpenStack Horizon Web Dashboard (Proxied at `http://10.0.0.10/horizon/auth/login/`) |
| `juju-65b4ac-0-lxd-4` | `glance/0` | `10.10.10.19` | `9292` | Cloud Image Registry (Ubuntu 22.04, Fedora CoreOS 35) |
| `juju-65b4ac-0-lxd-5` | `placement/0` | `10.10.10.18` | `8778` | Resource Provider Inventory & Scheduling Placement API |
| `juju-65b4ac-0-lxd-6` | `nova-cloud-controller/0` | `10.10.10.13` | `8774`, `8775` | Nova Compute API, Scheduler & Conductor |
| `juju-65b4ac-0-lxd-7` | `vault/0` | `10.10.10.7` | `8200` | HashiCorp Vault PKI & Secret Management |
| `juju-65b4ac-0-lxd-8` | `neutron-api/0` | `10.10.10.11` | `9696` | Neutron SDN API Server (ML2/OVN Driver) |
| `juju-65b4ac-0-lxd-9` | `ovn-chassis/0` | `10.10.10.3` | `6640` | Local OVN Controller & Open vSwitch Chassis |
| `juju-65b4ac-0-lxd-10` | `mysql-innodb-cluster/0` | `10.10.10.6` | `3306`, `33060` | **MySQL 8.0 InnoDB Cluster PRIMARY R/W Node** |
| `juju-65b4ac-0-lxd-11` | `ovn-central/0` | `10.10.10.12` | `6641`, `6642` | OVN Northbound & Southbound Databases + `ovn-northd` |
| `juju-65b4ac-0-lxd-12` | `heat/0` | `10.10.10.14` | `8004` | Heat Cloud Orchestration Engine (Used by Magnum) |
| `juju-65b4ac-0-lxd-13` | `barbican/0` | `10.10.10.15` | `9311` | Barbican Key & Certificate Manager |
| `juju-65b4ac-0-lxd-14` | `octavia/0` | `10.10.10.16` | `9876` | Octavia Amphora Load Balancer as a Service |
| `juju-65b4ac-0-lxd-15` | `magnum/0` | `10.10.10.10` | `9511` | Magnum Container Infrastructure Management (Kubernetes v1.23.3) |
| `juju-65b4ac-0-lxd-16` | `manila/0` | `10.10.10.20` | `8786` | Manila Shared File Systems Service |
| `juju-65b4ac-0-lxd-17` | `designate-bind/0` | `10.10.10.27` | `53` | BIND9 Authoritative DNS Backend |
| `juju-65b4ac-0-lxd-18` | `designate/0` | `10.10.10.21` | `9001` | Designate DNS as a Service API |
| `juju-65b4ac-0-lxd-19` | `gnocchi/0` | `10.10.10.23` | `8041` | Gnocchi Time-Series Metric Storage |
| `juju-65b4ac-0-lxd-20` | `ceilometer/0` | `10.10.10.24` | Internal | Ceilometer Cloud Telemetry Polling Agent |
| `juju-65b4ac-0-lxd-21` | `aodh/0` | `10.10.10.25` | `8042` | Aodh Cloud Alarming Engine |
| `juju-65b4ac-0-lxd-22` | `memcached/0` | `10.10.10.26` | `11211` | Distributed In-Memory Session Cache |

---

## 3. Step-by-Step End-to-End Implementation & Replication Guide

Anyone replicating this exact setup from scratch should execute the following **9 sequential phases**.

---

### Phase 1: Bare-Metal OS Provisioning, Network Bridges & Proxy-ARP Hardening

#### Step 1.1: Configure Linux Network Bridges & VLAN 10 on the Primary Server (`hpe-PowerEdge-R760xs`)
1. Install Ubuntu 22.04 LTS (`6.8.0-87-generic`) on the Dell PowerEdge R760xs (`96 threads`, `503 GiB RAM`) and mount the 2.9 TB enterprise storage array (`/dev/sda1`) at `/data`:
   ```bash
   sudo mkdir -p /data
   echo "/dev/sda1 /data ext4 defaults 0 2" | sudo tee -a /etc/fstab
   sudo mount -a
   ```
2. Configure `br-data` (`10.10.10.2/24`) for the OpenStack VLAN 10 underlay and `veth-host`/`veth-br` (`172.24.4.254/24`) for the OpenStack provider floating IP network (`br-ex`):
   ```bash
   sudo ip link add veth-host type veth peer name veth-br
   sudo ip addr add 172.24.4.254/24 dev veth-host
   sudo ip link set veth-host up
   sudo ip link set veth-br up
   sudo ovs-vsctl --may-exist add-br br-ex
   sudo ovs-vsctl --may-exist add-port br-ex veth-br
   ```
3. Enable IPv4 forwarding and configure NAT masquerading so OpenStack VMs and Kubernetes nodes have external network reachability:
   ```bash
   sudo sysctl -w net.ipv4.ip_forward=1
   sudo iptables -t nat -A POSTROUTING -s 172.24.4.0/24 ! -d 172.24.4.0/24 -j MASQUERADE
   sudo iptables -t nat -A POSTROUTING -s 192.168.100.0/24 ! -d 192.168.100.0/24 -j MASQUERADE
   ```
4. Configure passwordless SSH from `hpe@10.10.10.2` to `ubuntu@10.10.10.4` (`compute-pc1`) and `ubuntu@10.10.10.5` (`compute-pc2`):
   ```bash
   ssh-keygen -t ed25519 -N "" -f ~/.ssh/id_ed25519
   ssh-copy-id ubuntu@10.10.10.4
   ssh-copy-id ubuntu@10.10.10.5
   ```

---

### Phase 2: OpenStack 2023.1 Antelope Control Plane, KVM Compute & Horizon Hardening

#### Step 2.1: Deploy Juju & OpenStack Control Plane Inside `openstack-ctl`
1. Provision the LXD virtual machine `openstack-ctl` (`10.10.10.3`, 16 vCPUs, 64 GiB RAM) on the Dell host and deploy the 23 Juju OpenStack 2023.1 Antelope charms into LXD containers `juju-65b4ac-0-lxd-0` through `juju-65b4ac-0-lxd-22`.
2. Register the three KVM hypervisors (`hpe-PowerEdge-R760xs`, `compute-pc1.maas`, `compute-pc2.maas`) with `nova-compute` and `ovn-chassis` so OVS `br-int` establishes bidirectional Geneve tunnels (`ovn0-compu-0` to `10.10.10.5` and `ovn0-compu-1` to `10.10.10.4`) with BFD health monitoring enabled.

#### Step 2.2: Harden OpenStack Horizon & Prevent Bridge Proxy-ARP MAC Flapping
> **Critical Engineering Lesson**: On a multi-bridge host where `br-data` (`10.10.10.2`) and `eno8303` (`10.0.0.10`) coexist, enabling kernel `proxy_arp=1` on `br-data` causes the host kernel to reply to ARP requests inside `openstack-ctl` (`br-enp5s0`) with the host's MAC address (`e4:54:e8:92:16:08`), hijacking L2 traffic between Horizon (`10.10.10.8`) and Keystone (`10.10.10.9`) and causing `[Errno 113] No route to host`.

To permanently prevent this:
1. Disable `proxy_arp` on `br-data` and `all` in `/etc/sysctl.conf`:
   ```bash
   sudo sysctl -w net.ipv4.conf.br-data.proxy_arp=0
   sudo sysctl -w net.ipv4.conf.all.proxy_arp=0
   sudo sysctl -w net.ipv4.conf.default.proxy_arp=0
   ```
2. Point Horizon (`juju-65b4ac-0-lxd-3`) `/etc/openstack-dashboard/local_settings.py` `DATABASES['default']['HOST']` to the writable MySQL InnoDB Primary (`10.10.10.6`, `lxd-10`) rather than the read-only replica (`10.10.10.17`, `lxd-0`), and set `SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"`.
3. Install the automated minute-by-minute cron guard script [`/usr/local/bin/openstack-horizon-guard.sh`](file:///usr/local/bin/openstack-horizon-guard.sh) in `root`'s crontab (`* * * * * /usr/local/bin/openstack-horizon-guard.sh >/dev/null 2>&1`), which locks permanent bridge FDB (`bridge fdb replace ... permanent`) and permanent neighbor ARP (`ip neigh replace ... nud permanent`) entries across all 23 LXD containers.
4. Expose Horizon externally on `http://10.0.0.10/horizon/auth/login/` using the credentials:
   - **Username**: `admin`
   - **Password**: `ahseiweeNgaik8uX`
   - **Domain**: `admin_domain`

---

### Phase 3: Magnum Kubernetes v1.23.3, Open5GS 5G SA Core & Online Boutique Microservices

#### Step 3.1: Provision the 3-Node Kubernetes Cluster via OpenStack Magnum
1. Upload the Fedora CoreOS 35 image to Glance and create the Magnum cluster template (`k8s-5g-template`, flavor `m1.5g.control`: 4 vCPUs, 16 GiB RAM, Flannel CNI):
   ```bash
   openstack coe cluster template create k8s-5g-template \
     --image fedora-coreos-35 \
     --external-network ext-net \
     --dns-nameserver 8.8.8.8 \
     --master-flavor m1.5g.control \
     --flavor m1.5g.control \
     --coe kubernetes \
     --network-driver flannel
   openstack coe cluster create k8s-5g-cluster \
     --cluster-template k8s-5g-template \
     --master-count 1 \
     --node-count 2
   ```
2. Export the cluster `kubeconfig` to `/home/hpe/k8s-5g/config`:
   ```bash
   KUBECONFIG=/home/hpe/k8s-5g/config kubectl get nodes -o wide
   ```
   - `k8s-5g-cluster-j3ldsouiexj3-master-0`: `192.168.100.72` (Floating IP `10.0.0.215`, KVM `instance-00000008`)
   - `k8s-5g-cluster-j3ldsouiexj3-node-0`: `192.168.100.131` (Floating IP `10.0.0.206`, KVM `instance-00000007`)
   - `k8s-5g-cluster-j3ldsouiexj3-node-1`: `192.168.100.174` (Floating IP `10.0.0.232`, KVM `instance-00000006`)

#### Step 3.2: Deploy Open5GS 5G Standalone (SA) Core (`open5gs` Namespace)
1. Create the `open5gs` namespace and deploy all **13 3GPP Release-17 5G Core Network Functions**:
   - **Control Plane SBA**: `nrf`, `scp`, `ausf`, `udm`, `udr`, `pcf`, `nssf`, `bsf`, `amf`, `smf`, `webui`, and `mongodb-0` (subscriber database provisioned with IMSI `001010123456780`–`782`, Key `465B5CE8B199B49FAA5F0A2EE238A6BC`, OPc `E8ED289DEBA952E4283B54E88E6183CA`, APN `internet`, SST `1`).
   - **User Plane (`open5gs-upf`)**: Privileged pod with `NET_ADMIN` capability and `/dev/net/tun`, configuring `ogstun` (`10.45.0.1/16`) and `iptables` NAT masquerading.
   - **External N2/N3 Exposure**: Expose `open5gs-amf` SCTP port `38412` (N2 NGAP) and `open5gs-upf` UDP port `2152` (N3 GTP-U) on `192.168.100.131` so physical gNodeBs on `compute-pc1` (`10.10.10.4`) connect directly to the Kubernetes 5G Core.

#### Step 3.3: Deploy Google Online Boutique Cloud-Native Microservices (`microservices` Namespace)
1. Deploy the 12-microservice cloud-native benchmark (`frontend`, `cartservice`, `checkoutservice`, `currencyservice`, `emailservice`, `paymentservice`, `productcatalogservice`, `recommendationservice`, `shippingservice`, `adservice`, `redis-cart`, `loadgenerator`) into the `microservices` namespace:
   ```bash
   KUBECONFIG=/home/hpe/k8s-5g/config kubectl get pods -n microservices
   ```

---

### Phase 4: Physical 5G SDR Radio Access Network (4x Ettus USRP B210 & srsRAN Project)

#### Step 4.1: Hardware Topology & USRP LED Status Interpretation
- **`compute-pc1` (`10.10.10.4`)**: Hosts **1x Ettus USRP B210 (`serial=34B18C8`)** acting as the **5G NR Band n78 TDD gNodeB** (`3879.42 MHz`, ARFCN `658628`, `20 MHz` bandwidth, `30 kHz` subcarrier spacing).
- **`compute-pc2` (`10.10.10.5`)**: Hosts **3x Ettus USRP B210 SDRs (`serial=34B18A2`, `serial=34B1905`, and USRP #3)** acting as **3 physical 5G NR UEs (`srsue1`, `srsue2`, `srsue3`)**.
- **USRP LED Indicator Reference**:
  - **Red/Amber LED on RF-A (`TX/RX`)**: Indicates active **Transmission (TX) + Reception (RX)** TDD switching on the gNodeB (`compute-pc1`).
  - **Blue/Green LED on RF-A (`RX2`)**: Indicates active **Reception (RX)** synchronization on the UEs (`compute-pc2`).
  - **Activating Both RF-A and RF-B Channels (8 Total RF Chains Across 4 USRPs)**: By configuring `tx_ant = 2` / `rx_ant = 2` (`nof_antennas = 2` MIMO or dual-cell subdev `A:A A:B`), all 8 AD9361 transceivers across the 4 USRP B210 boards are energized simultaneously.

#### Step 4.2: Configure & Enable `srsgnb` and `srsue1`..`srsue3` Systemd Services
1. On `compute-pc1` (`10.10.10.4`), configure `/etc/srsran/gnb.yml` to bind to `amf.addr: 192.168.100.131`, `device_driver: uhd`, `device_args: "type=b200,serial=34B18C8,num_recv_frames=512,num_send_frames=512"`, `band: 78`, `dl_arfcn: 658628`, `tx_gain: 60`, `rx_gain: 40`, logging to `/tmp/gnb.log`, and enable `srsgnb.service`:
   ```bash
   ssh ubuntu@10.10.10.4 "sudo systemctl enable --now srsgnb.service"
   ```
2. On `compute-pc2` (`10.10.10.5`), create network namespaces `ue1`, `ue2`, `ue3` and enable `srsue1.service`, `srsue2.service`, `srsue3.service` pinned to each USRP B210 serial number:
   ```bash
   ssh ubuntu@10.10.10.5 "sudo systemctl enable --now srsue1.service srsue2.service"
   ```

---

### Phase 5: Wazuh SIEM v4.8.0 Security Operations & Multi-Node Threat Monitoring

1. On `hpe-PowerEdge-R760xs` (`10.0.0.10` / `10.10.10.2`), deploy and enable:
   - `wazuh-manager.service` (Port `1514` agent event ingestion, `1515` enrollment, `55000` API)
   - `wazuh-indexer.service` (`127.0.0.1:9200` OpenSearch index)
   - `wazuh-dashboard.service` (HTTPS Web UI)
2. Enroll all cluster endpoints with `wazuh-manager`:
   - **Agent `000`**: `hpe-PowerEdge-R760xs` (Local Manager & Hypervisor)
   - **Agent `002`**: `compute-pc1` (`10.10.10.4`)
   - **Agent `003`**: `compute-pc2` (`10.10.10.5`)
   - **Agent `004`**: `windows-jump-host` (`10.0.0.21`)
3. Enable real-time JSON alert streaming at `/var/ossec/logs/alerts/alerts.json` and Active Response logging at `/var/ossec/logs/active-responses.log`.

---

### Phase 6: Distributed Dual-GPU + Xeon AMX Compute & Ollama Qwen3-14B LLM Setup

1. **Distributed AI Workload Engine ([`/home/hpe/gpu_and_cpu_workload.py`](file:///home/hpe/gpu_and_cpu_workload.py))**:
   - Dispatches continuous matrix/tensor compute across:
     - **Dell PowerEdge R760xs**: 32 parallel worker processes leveraging Dual Intel Xeon Gold 5418Y AVX-512/AMX (`~545 GFLOPS`).
     - **`compute-pc1` (`10.10.10.4`)**: `GPU0` Intel UHD Graphics 770 (`/dev/dri/renderD128`, `1450 MHz`, `~204.6 GFLOPS`).
     - **`compute-pc2` (`10.10.10.5`)**: `GPU1` Intel UHD Graphics 770 (`/dev/dri/renderD128`, `1450 MHz`, `~204.6 GFLOPS`).
   - Streams real-time cluster GFLOPS (`~954–961 GFLOPS` combined) and VRAM telemetry to [`/home/hpe/telemetry/gpu_workload_metrics.json`](file:///home/hpe/telemetry/gpu_workload_metrics.json).
2. **Ollama `qwen3:14b` LLM Server (`10.0.0.21:11434`)**:
   - Run `ollama serve` with `qwen3:14b` on the Windows Jump Host (`10.0.0.21:11434`) so the XIE agent can asynchronously generate Markdown root-cause post-mortem reports in [`/home/hpe/agent/reports/`](file:///home/hpe/agent/reports).

---

### Phase 7: Experiential Intelligence Engine (XIE Core), 4-Domain MCP Servers & Self-Healing Agent

The autonomous intelligence core is implemented in [`/home/hpe/xie/`](file:///home/hpe/xie) and [`/home/hpe/agent/self_healing_agent.py`](file:///home/hpe/agent/self_healing_agent.py):

1. **Tier-1 Anomaly Detection (`self_healing_agent.py` + `/home/hpe/agent/models/anomaly_detector.pkl`)**:
   - Computes rolling Z-scores ($z_t^{(i)} = \frac{x_t^{(i)} - \mu_t^{(i)}}{\sigma_t^{(i)} + \epsilon}$) over a sliding window $W=20$ and evaluates a 100-tree Random Forest classifier across all 5 operational classes (`nominal`, `compute_cpu_exhaustion`, `k8s_container_crash`, `ovn_sdn_latency_loss`, `rf_path_loss_attenuation`).
2. **Tier-2 ChromaDB HNSW Episodic Vector Memory ([`/home/hpe/xie/episodic_memory.py`](file:///home/hpe/xie/episodic_memory.py))**:
   - Embeds anomaly telemetry signatures into a persistent HNSW index (`/home/hpe/xie/chroma_db`, `1,161` verified historical episodes). If top-1 cosine similarity $\ge 0.92$, executes **Zero-Shot Instant Remediation** bypassing heavy causal search.
3. **Tier-3 VAR(2) Granger Causal Discovery & Reversed-DAG Personalized PageRank ([`/home/hpe/xie/causal_discovery.py`](file:///home/hpe/xie/causal_discovery.py), [`/home/hpe/xie/causal_rca.py`](file:///home/hpe/xie/causal_rca.py))**:
   - Fits a lag-2 Vector Autoregressive model ($\mathbf{x}_t = \mathbf{c} + A^{(1)}\mathbf{x}_{t-1} + A^{(2)}\mathbf{x}_{t-2} + \boldsymbol{\varepsilon}_t$), constructs a directed causal graph $G=(V,E)$ from F-test edge weights, reverses edge directions ($G_{\text{rev}}$) so probability mass flows upstream from downstream symptoms to physical root causes, and solves Personalized PageRank:
     $$\boldsymbol{\pi} = (1 - \alpha)\mathbf{v} + \alpha P_{\text{rev}}^{\top}\boldsymbol{\pi}, \quad \alpha = 0.85$$
4. **Tier-4 Multi-Domain FastMCP Closed-Loop Actuation**:
   - Executes guardrailed remediations across the 4 operational domains (`RAN-MCP`, `K8s-MCP`, `Cloud-MCP`, `SecOps-MCP`) with a 45-second per-domain cooldown guard and logs every step to [`/home/hpe/agent/logs/remediation_audit.log`](file:///home/hpe/agent/logs/remediation_audit.log).
5. **Enable the Permanent Systemd Service**:
   ```bash
   sudo systemctl enable --now self-healing-agent.service
   ```

---

### Phase 8: Observability Stack & Continuous 6-Plane Multi-Dimensional Dataset Warehouse

#### Step 8.1: Unified Prometheus & Grafana Observability Server
- [`/home/hpe/multi_domain_exporter.py`](file:///home/hpe/multi_domain_exporter.py) (`multi-domain-exporter.service` on `:9105`) + OVS Exporter (`:9475`) + [`/home/hpe/grafana_and_prometheus_server.py`](file:///home/hpe/grafana_and_prometheus_server.py) (`:9090` Prometheus UI & `:3000` Grafana Enterprise Dashboards).

#### Step 8.2: Continuous 6-Plane Multi-Dimensional Dataset Harvester (`omni-crosslayer-harvester.service`)
- Installed in [`/data/cross_layer_dataset/bin/`](file:///data/cross_layer_dataset/bin) and symlinked at [`/home/hpe/HPE/cross_layer_dataset`](file:///home/hpe/HPE/cross_layer_dataset):
  - [`omni_schema_and_harvester.py`](file:///home/hpe/HPE/cross_layer_dataset/bin/omni_schema_and_harvester.py): Collects **368 cross-layer parameters** in parallel across all 6 planes every 5.0 seconds.
  - [`omni_log_harvester_and_warehouse.py`](file:///home/hpe/HPE/cross_layer_dataset/bin/omni_log_harvester_and_warehouse.py): Incrementally tails and normalizes **all logs, alerts, and events** across all 6 planes into JSONL, CSV, SQLite WAL (`cross_layer_warehouse.db`), Pandas `.pkl`, and NumPy `.npz` tensors, with automated 250 MB `gzip` partition rotation and 80% disk watermark protection.
  - [`omni_harvester_daemon.py`](file:///home/hpe/HPE/cross_layer_dataset/bin/omni_harvester_daemon.py): Managed by `/etc/systemd/system/omni-crosslayer-harvester.service`.

---

## 4. Operational Runbook, Verification Commands & Moving Forward Guide

### 4.1 Instant System Health & Dataset Verification Commands

```bash
# 1. Inspect the live 6-plane dataset warehouse (368 parameters + 42,500+ logs/alerts)
dataset-status

# 2. Verify all core autonomous daemons are active
sudo systemctl status omni-crosslayer-harvester.service self-healing-agent.service multi-domain-exporter.service 5g-telemetry.service wazuh-manager.service

# 3. Verify OpenStack Horizon login endpoint & 23 Juju LXD containers
python3 /home/hpe/test_horizon_login.py
sudo lxc exec openstack-ctl -- lxc list

# 4. Verify Kubernetes 5G SA Core (13 pods) & Online Boutique (12 pods)
KUBECONFIG=/home/hpe/k8s-5g/config kubectl get pods -A -o wide

# 5. Verify Physical USRP B210 SDRs & srsRAN gNodeB / UE Services
ssh ubuntu@10.10.10.4 "lsusb | grep 2500:0020; systemctl is-active srsgnb; tail -n 10 /tmp/gnb.log"
ssh ubuntu@10.10.10.5 "lsusb | grep 2500:0020; systemctl is-active srsue1 srsue2"

# 6. Watch Autonomous AIOps Self-Healing Decisions in Real Time
tail -f /home/hpe/agent/logs/remediation_audit.log
```

### 4.2 Web Interfaces & Dashboards Quick Reference

| Interface | URL | Credentials / Access |
| :--- | :--- | :--- |
| **OpenStack Horizon Dashboard** | `http://10.0.0.10/horizon/auth/login/` | User: `admin` \| Pass: `ahseiweeNgaik8uX` \| Domain: `admin_domain` |
| **Grafana Multi-Domain Dashboards** | `http://10.0.0.10:3000` | Live 6-Plane Executive & Technical Telemetry Panels |
| **Prometheus Time-Series Server** | `http://10.0.0.10:9090` | Scrape targets `:9105` (Multi-Domain) & `:9475` (OVS/OVN) |
| **Raw Multi-Domain Metrics Exporter** | `http://10.0.0.10:9105/metrics` | Live Prometheus text exposition format |
| **Online Boutique Cloud E-Commerce** | `http://192.168.100.131:30080` | Live 12-microservice application workload |
| **Ollama Qwen3-14B LLM API** | `http://10.0.0.21:11434` | Automated incident post-mortem synthesis endpoint |

