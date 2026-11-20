# Cross-Layer Multi-Dimensional Dataset Feature Catalog

- **Dataset Root**: `/data/cross_layer_dataset` (linked at `/home/hpe/HPE/cross_layer_dataset`)
- **Total Time-Series Features per Instance**: **368 parameters**
- **Unified Log & Alert Schema Fields**: **14 structured fields**
- **Sampling Cadence**: Continuous 5.0-second real-time daemon (`omni-crosslayer-harvester.service`)

## Parameter Count by Architectural Plane

| Plane ID | Architectural Plane | Feature Count |
| :--- | :--- | :--- |
| **Plane 0** | Plane 0: Temporal Metadata & Ground-Truth Labels | **8** |
| **Plane 1** | Plane 1: Bare-Metal Hardware, Linux Kernel, NUMA & Physical I/O | **78** |
| **Plane 2** | Plane 2: OpenStack 2023.1 LXD Control Plane, KVM Hypervisor & OVN/OVS SDN | **117** |
| **Plane 3** | Plane 3: Magnum Kubernetes v1.23.3, Open5GS 5G SA Core & Cloud-Native Microservices | **74** |
| **Plane 4** | Plane 4: Physical 5G SDR Radio Access Network (4x USRP B210) & Enterprise Wireless Fabric | **34** |
| **Plane 5** | Plane 5: Wazuh SIEM v4.8.0 Security Operations, Threat Detection & Active Response | **22** |
| **Plane 6** | Plane 6: Distributed AI Compute (Dual-GPU + Xeon AMX) & XIE Explainable Agentic AIOps | **35** |

## Complete Parameter Dictionary

| # | Parameter Name | Plane | Source Node | Component | Unit | Type | ML Role | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `timestamp` | P0 | `cluster-global` | `chrony-ntp` | `ISO8601_UTC` | `string` | `temporal_index` | UTC ISO-8601 synchronization timestamp |
| 2 | `epoch_ms` | P0 | `cluster-global` | `chrony-ntp` | `ms` | `int64` | `temporal_index` | Unix epoch timestamp in milliseconds |
| 3 | `sequence_id` | P0 | `cluster-global` | `harvester` | `count` | `int64` | `temporal_index` | Monotonic sample sequence counter |
| 4 | `fault_label` | P0 | `cluster-global` | `fault-annotator` | `category` | `string` | `target_label` | Multi-class ground-truth operational state / fault label |
| 5 | `fault_class_id` | P0 | `cluster-global` | `fault-annotator` | `class_id` | `int` | `target_label` | Numeric fault class ID (0=nominal, 1=cpu, 2=k8s, 3=ovn, 4=rf) |
| 6 | `anomaly_severity` | P0 | `cluster-global` | `fault-annotator` | `severity_0_10` | `int` | `target_label` | Ground-truth anomaly severity score (0=nominal .. 10=critical) |
| 7 | `is_anomalous` | P0 | `cluster-global` | `fault-annotator` | `binary` | `int` | `target_label` | Binary anomaly indicator (0=normal, 1=anomalous) |
| 8 | `collection_latency_ms` | P0 | `hpe-PowerEdge-R760xs` | `harvester` | `ms` | `float` | `metadata` | Cross-layer multi-node harvest execution latency in ms |
| 9 | `p1_dell_load_1m` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `load` | `float` | `input_feature` | Dell R760xs 1-minute OS load average (96 hardware threads) |
| 10 | `p1_dell_load_5m` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `load` | `float` | `input_feature` | Dell R760xs 5-minute OS load average |
| 11 | `p1_dell_load_15m` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `load` | `float` | `input_feature` | Dell R760xs 15-minute OS load average |
| 12 | `p1_dell_cpu_util_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs overall CPU utilization percentage |
| 13 | `p1_dell_cpu_user_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs user-space CPU mode percentage |
| 14 | `p1_dell_cpu_nice_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs nice user-space CPU mode percentage |
| 15 | `p1_dell_cpu_system_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs kernel system CPU mode percentage |
| 16 | `p1_dell_cpu_idle_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs idle CPU mode percentage |
| 17 | `p1_dell_cpu_iowait_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs I/O wait CPU mode percentage |
| 18 | `p1_dell_cpu_irq_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs hardware IRQ CPU percentage |
| 19 | `p1_dell_cpu_softirq_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs software IRQ (network/block) CPU percentage |
| 20 | `p1_dell_cpu_steal_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs hypervisor steal CPU percentage |
| 21 | `p1_dell_cpu_guest_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs KVM/LXD guest vCPU execution percentage |
| 22 | `p1_dell_ctxt_switches_total` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int64` | `input_feature` | Dell R760xs cumulative kernel context switches |
| 23 | `p1_dell_intr_total` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int64` | `input_feature` | Dell R760xs cumulative hardware interrupts serviced |
| 24 | `p1_dell_procs_running` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int` | `input_feature` | Dell R760xs runnable kernel threads |
| 25 | `p1_dell_procs_blocked` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int` | `input_feature` | Dell R760xs threads blocked waiting on I/O |
| 26 | `p1_dell_uptime_sec` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `s` | `float` | `input_feature` | Dell R760xs system uptime in seconds |
| 27 | `p1_dell_mem_total_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs total physical DDR5 ECC memory (MB) |
| 28 | `p1_dell_mem_used_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs used physical memory (MB) |
| 29 | `p1_dell_mem_avail_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs available memory without swapping (MB) |
| 30 | `p1_dell_mem_free_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs unallocated free memory (MB) |
| 31 | `p1_dell_mem_cached_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs page cache memory (MB) |
| 32 | `p1_dell_mem_buffers_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs kernel buffer memory (MB) |
| 33 | `p1_dell_mem_slab_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs kernel slab allocator footprint (MB) |
| 34 | `p1_dell_mem_dirty_kb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `KB` | `float` | `input_feature` | Dell R760xs dirty pages awaiting disk writeback (KB) |
| 35 | `p1_dell_mem_anon_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs anonymous mapped memory (MB) |
| 36 | `p1_dell_mem_util_pct` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `%` | `float` | `input_feature` | Dell R760xs physical memory utilization percentage |
| 37 | `p1_dell_swap_total_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs swap total capacity (MB) |
| 38 | `p1_dell_swap_used_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs swap used (MB) |
| 39 | `p1_dell_vm_pgfault_total` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int64` | `input_feature` | Dell R760xs cumulative minor page faults |
| 40 | `p1_dell_vm_pgmajfault_total` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int64` | `input_feature` | Dell R760xs cumulative major page faults |
| 41 | `p1_dell_vm_oom_kills` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int` | `input_feature` | Dell R760xs kernel OOM killer invocations |
| 42 | `p1_dell_numa0_mem_total_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs NUMA Socket 0 total RAM (MB) |
| 43 | `p1_dell_numa0_mem_used_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs NUMA Socket 0 used RAM (MB) |
| 44 | `p1_dell_numa1_mem_total_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs NUMA Socket 1 total RAM (MB) |
| 45 | `p1_dell_numa1_mem_used_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell R760xs NUMA Socket 1 used RAM (MB) |
| 46 | `p1_dell_sda_read_ops` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int64` | `input_feature` | Dell /data (2.9TB sda) cumulative read I/O operations |
| 47 | `p1_dell_sda_write_ops` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int64` | `input_feature` | Dell /data (2.9TB sda) cumulative write I/O operations |
| 48 | `p1_dell_sda_read_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell /data (2.9TB sda) cumulative megabytes read |
| 49 | `p1_dell_sda_write_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell /data (2.9TB sda) cumulative megabytes written |
| 50 | `p1_dell_sda_io_time_ms` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `ms` | `int64` | `input_feature` | Dell /data (2.9TB sda) cumulative I/O active time (ms) |
| 51 | `p1_dell_sdb_read_ops` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int64` | `input_feature` | Dell rootfs (438GB sdb) cumulative read I/O operations |
| 52 | `p1_dell_sdb_write_ops` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `count` | `int64` | `input_feature` | Dell rootfs (438GB sdb) cumulative write I/O operations |
| 53 | `p1_dell_sdb_read_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell rootfs (438GB sdb) cumulative megabytes read |
| 54 | `p1_dell_sdb_write_mb` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `MB` | `float` | `input_feature` | Dell rootfs (438GB sdb) cumulative megabytes written |
| 55 | `p1_dell_nic_eno8303_rx_bytes` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `bytes` | `int64` | `input_feature` | Dell eno8303 (10.0.0.10 Management NIC) RX bytes |
| 56 | `p1_dell_nic_eno8303_tx_bytes` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `bytes` | `int64` | `input_feature` | Dell eno8303 (10.0.0.10 Management NIC) TX bytes |
| 57 | `p1_dell_nic_eno8303_drops` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `packets` | `int64` | `input_feature` | Dell eno8303 RX+TX dropped packets |
| 58 | `p1_dell_nic_enp171_rx_bytes` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `bytes` | `int64` | `input_feature` | Dell enp171s0f0np0 (High-Speed Fabric NIC) RX bytes |
| 59 | `p1_dell_nic_enp171_tx_bytes` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `bytes` | `int64` | `input_feature` | Dell enp171s0f0np0 (High-Speed Fabric NIC) TX bytes |
| 60 | `p1_dell_nic_enp171_drops` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `packets` | `int64` | `input_feature` | Dell enp171s0f0np0 RX+TX dropped packets |
| 61 | `p1_dell_nic_brdata_rx_bytes` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `bytes` | `int64` | `input_feature` | Dell br-data (10.10.10.2 OpenStack Data Bridge) RX bytes |
| 62 | `p1_dell_nic_brdata_tx_bytes` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `bytes` | `int64` | `input_feature` | Dell br-data (10.10.10.2 OpenStack Data Bridge) TX bytes |
| 63 | `p1_dell_nic_brdata_rx_pkts` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `packets` | `int64` | `input_feature` | Dell br-data RX packets |
| 64 | `p1_dell_nic_brdata_tx_pkts` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `packets` | `int64` | `input_feature` | Dell br-data TX packets |
| 65 | `p1_dell_nic_vethhost_rx_bytes` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `bytes` | `int64` | `input_feature` | Dell veth-host (172.24.4.254 Floating IP Router Link) RX bytes |
| 66 | `p1_dell_nic_vethhost_tx_bytes` | P1 | `hpe-PowerEdge-R760xs` | `linux-kernel` | `bytes` | `int64` | `input_feature` | Dell veth-host (172.24.4.254 Floating IP Router Link) TX bytes |
| 67 | `p1_pc1_reachable` | P1 | `compute-pc1 (10.10.10.4)` | `icmp-ssh` | `binary` | `int` | `input_feature` | compute-pc1 (10.10.10.4) host reachability status (1=online) |
| 68 | `p1_pc1_load_1m` | P1 | `compute-pc1 (10.10.10.4)` | `linux-kernel` | `load` | `float` | `input_feature` | compute-pc1 (10.10.10.4) 1-minute CPU load average |
| 69 | `p1_pc1_load_5m` | P1 | `compute-pc1 (10.10.10.4)` | `linux-kernel` | `load` | `float` | `input_feature` | compute-pc1 (10.10.10.4) 5-minute CPU load average |
| 70 | `p1_pc1_cpu_util_pct` | P1 | `compute-pc1 (10.10.10.4)` | `linux-kernel` | `%` | `float` | `input_feature` | compute-pc1 (10.10.10.4) CPU utilization percentage |
| 71 | `p1_pc1_mem_used_mb` | P1 | `compute-pc1 (10.10.10.4)` | `linux-kernel` | `MB` | `float` | `input_feature` | compute-pc1 (10.10.10.4) RAM used (MB) |
| 72 | `p1_pc1_mem_total_mb` | P1 | `compute-pc1 (10.10.10.4)` | `linux-kernel` | `MB` | `float` | `input_feature` | compute-pc1 (10.10.10.4) RAM total (MB) |
| 73 | `p1_pc1_mem_util_pct` | P1 | `compute-pc1 (10.10.10.4)` | `linux-kernel` | `%` | `float` | `input_feature` | compute-pc1 (10.10.10.4) RAM utilization percentage |
| 74 | `p1_pc1_net_rx_bytes` | P1 | `compute-pc1 (10.10.10.4)` | `netdev` | `bytes` | `int64` | `input_feature` | compute-pc1 (10.10.10.4) primary data interface RX bytes |
| 75 | `p1_pc1_net_tx_bytes` | P1 | `compute-pc1 (10.10.10.4)` | `netdev` | `bytes` | `int64` | `input_feature` | compute-pc1 (10.10.10.4) primary data interface TX bytes |
| 76 | `p1_pc1_net_drops` | P1 | `compute-pc1 (10.10.10.4)` | `netdev` | `packets` | `int64` | `input_feature` | compute-pc1 (10.10.10.4) interface dropped packets |
| 77 | `p1_pc2_reachable` | P1 | `compute-pc2 (10.10.10.5)` | `icmp-ssh` | `binary` | `int` | `input_feature` | compute-pc2 (10.10.10.5) host reachability status (1=online) |
| 78 | `p1_pc2_load_1m` | P1 | `compute-pc2 (10.10.10.5)` | `linux-kernel` | `load` | `float` | `input_feature` | compute-pc2 (10.10.10.5) 1-minute CPU load average |
| 79 | `p1_pc2_load_5m` | P1 | `compute-pc2 (10.10.10.5)` | `linux-kernel` | `load` | `float` | `input_feature` | compute-pc2 (10.10.10.5) 5-minute CPU load average |
| 80 | `p1_pc2_cpu_util_pct` | P1 | `compute-pc2 (10.10.10.5)` | `linux-kernel` | `%` | `float` | `input_feature` | compute-pc2 (10.10.10.5) CPU utilization percentage |
| 81 | `p1_pc2_mem_used_mb` | P1 | `compute-pc2 (10.10.10.5)` | `linux-kernel` | `MB` | `float` | `input_feature` | compute-pc2 (10.10.10.5) RAM used (MB) |
| 82 | `p1_pc2_mem_total_mb` | P1 | `compute-pc2 (10.10.10.5)` | `linux-kernel` | `MB` | `float` | `input_feature` | compute-pc2 (10.10.10.5) RAM total (MB) |
| 83 | `p1_pc2_mem_util_pct` | P1 | `compute-pc2 (10.10.10.5)` | `linux-kernel` | `%` | `float` | `input_feature` | compute-pc2 (10.10.10.5) RAM utilization percentage |
| 84 | `p1_pc2_net_rx_bytes` | P1 | `compute-pc2 (10.10.10.5)` | `netdev` | `bytes` | `int64` | `input_feature` | compute-pc2 (10.10.10.5) primary data interface RX bytes |
| 85 | `p1_pc2_net_tx_bytes` | P1 | `compute-pc2 (10.10.10.5)` | `netdev` | `bytes` | `int64` | `input_feature` | compute-pc2 (10.10.10.5) primary data interface TX bytes |
| 86 | `p1_pc2_net_drops` | P1 | `compute-pc2 (10.10.10.5)` | `netdev` | `packets` | `int64` | `input_feature` | compute-pc2 (10.10.10.5) interface dropped packets |
| 87 | `p2_os_lxd_containers_total` | P2 | `openstack-ctl` | `lxd-daemon` | `count` | `int` | `input_feature` | Total Juju OpenStack LXD containers provisioned |
| 88 | `p2_os_lxd_containers_running` | P2 | `openstack-ctl` | `lxd-daemon` | `count` | `int` | `input_feature` | Running Juju OpenStack LXD containers |
| 89 | `p2_os_horizon_http_code` | P2 | `juju-65b4ac-0-lxd-3` | `horizon-apache2` | `http_code` | `int` | `input_feature` | OpenStack Horizon /horizon/auth/login/ HTTP response status code |
| 90 | `p2_os_horizon_latency_ms` | P2 | `juju-65b4ac-0-lxd-3` | `horizon-apache2` | `ms` | `float` | `input_feature` | OpenStack Horizon login endpoint response latency (ms) |
| 91 | `p2_os_keystone_http_code` | P2 | `juju-65b4ac-0-lxd-2` | `keystone-v3` | `http_code` | `int` | `input_feature` | OpenStack Keystone Identity API :5000/v3 HTTP status code |
| 92 | `p2_os_mysql_primary_up` | P2 | `juju-65b4ac-0-lxd-10` | `mysql-innodb` | `binary` | `int` | `input_feature` | MySQL 8.0 InnoDB Cluster primary node 10.10.10.6:3306 online status |
| 93 | `p2_os_hypervisors_up` | P2 | `openstack-ctl` | `nova-compute` | `count` | `int` | `input_feature` | Registered UP OpenStack Nova KVM hypervisors |
| 94 | `p2_os_active_vms_total` | P2 | `openstack-ctl` | `nova-compute` | `count` | `int` | `input_feature` | Total active OpenStack Nova instances across cluster |
| 95 | `p2_lxd_0_mysql_innodb_secondary_up` | P2 | `juju-65b4ac-0-lxd-0` | `mysql_innodb_secondary` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-0 (mysql_innodb_secondary @ 10.10.10.17) Running status (1=Running) |
| 96 | `p2_lxd_0_mysql_innodb_secondary_mem_mb` | P2 | `juju-65b4ac-0-lxd-0` | `mysql_innodb_secondary` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-0 (mysql_innodb_secondary) cgroup memory consumption (MB) |
| 97 | `p2_lxd_0_mysql_innodb_secondary_procs` | P2 | `juju-65b4ac-0-lxd-0` | `mysql_innodb_secondary` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-0 (mysql_innodb_secondary) active process count |
| 98 | `p2_lxd_1_rabbitmq_server_up` | P2 | `juju-65b4ac-0-lxd-1` | `rabbitmq_server` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-1 (rabbitmq_server @ 10.10.10.22) Running status (1=Running) |
| 99 | `p2_lxd_1_rabbitmq_server_mem_mb` | P2 | `juju-65b4ac-0-lxd-1` | `rabbitmq_server` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-1 (rabbitmq_server) cgroup memory consumption (MB) |
| 100 | `p2_lxd_1_rabbitmq_server_procs` | P2 | `juju-65b4ac-0-lxd-1` | `rabbitmq_server` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-1 (rabbitmq_server) active process count |
| 101 | `p2_lxd_2_keystone_identity_up` | P2 | `juju-65b4ac-0-lxd-2` | `keystone_identity` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-2 (keystone_identity @ 10.10.10.9) Running status (1=Running) |
| 102 | `p2_lxd_2_keystone_identity_mem_mb` | P2 | `juju-65b4ac-0-lxd-2` | `keystone_identity` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-2 (keystone_identity) cgroup memory consumption (MB) |
| 103 | `p2_lxd_2_keystone_identity_procs` | P2 | `juju-65b4ac-0-lxd-2` | `keystone_identity` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-2 (keystone_identity) active process count |
| 104 | `p2_lxd_3_horizon_dashboard_up` | P2 | `juju-65b4ac-0-lxd-3` | `horizon_dashboard` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-3 (horizon_dashboard @ 10.10.10.8) Running status (1=Running) |
| 105 | `p2_lxd_3_horizon_dashboard_mem_mb` | P2 | `juju-65b4ac-0-lxd-3` | `horizon_dashboard` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-3 (horizon_dashboard) cgroup memory consumption (MB) |
| 106 | `p2_lxd_3_horizon_dashboard_procs` | P2 | `juju-65b4ac-0-lxd-3` | `horizon_dashboard` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-3 (horizon_dashboard) active process count |
| 107 | `p2_lxd_4_glance_images_up` | P2 | `juju-65b4ac-0-lxd-4` | `glance_images` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-4 (glance_images @ 10.10.10.19) Running status (1=Running) |
| 108 | `p2_lxd_4_glance_images_mem_mb` | P2 | `juju-65b4ac-0-lxd-4` | `glance_images` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-4 (glance_images) cgroup memory consumption (MB) |
| 109 | `p2_lxd_4_glance_images_procs` | P2 | `juju-65b4ac-0-lxd-4` | `glance_images` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-4 (glance_images) active process count |
| 110 | `p2_lxd_5_placement_api_up` | P2 | `juju-65b4ac-0-lxd-5` | `placement_api` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-5 (placement_api @ 10.10.10.18) Running status (1=Running) |
| 111 | `p2_lxd_5_placement_api_mem_mb` | P2 | `juju-65b4ac-0-lxd-5` | `placement_api` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-5 (placement_api) cgroup memory consumption (MB) |
| 112 | `p2_lxd_5_placement_api_procs` | P2 | `juju-65b4ac-0-lxd-5` | `placement_api` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-5 (placement_api) active process count |
| 113 | `p2_lxd_6_nova_cloud_controller_up` | P2 | `juju-65b4ac-0-lxd-6` | `nova_cloud_controller` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-6 (nova_cloud_controller @ 10.10.10.13) Running status (1=Running) |
| 114 | `p2_lxd_6_nova_cloud_controller_mem_mb` | P2 | `juju-65b4ac-0-lxd-6` | `nova_cloud_controller` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-6 (nova_cloud_controller) cgroup memory consumption (MB) |
| 115 | `p2_lxd_6_nova_cloud_controller_procs` | P2 | `juju-65b4ac-0-lxd-6` | `nova_cloud_controller` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-6 (nova_cloud_controller) active process count |
| 116 | `p2_lxd_7_vault_secrets_up` | P2 | `juju-65b4ac-0-lxd-7` | `vault_secrets` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-7 (vault_secrets @ 10.10.10.7) Running status (1=Running) |
| 117 | `p2_lxd_7_vault_secrets_mem_mb` | P2 | `juju-65b4ac-0-lxd-7` | `vault_secrets` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-7 (vault_secrets) cgroup memory consumption (MB) |
| 118 | `p2_lxd_7_vault_secrets_procs` | P2 | `juju-65b4ac-0-lxd-7` | `vault_secrets` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-7 (vault_secrets) active process count |
| 119 | `p2_lxd_8_neutron_api_up` | P2 | `juju-65b4ac-0-lxd-8` | `neutron_api` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-8 (neutron_api @ 10.10.10.11) Running status (1=Running) |
| 120 | `p2_lxd_8_neutron_api_mem_mb` | P2 | `juju-65b4ac-0-lxd-8` | `neutron_api` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-8 (neutron_api) cgroup memory consumption (MB) |
| 121 | `p2_lxd_8_neutron_api_procs` | P2 | `juju-65b4ac-0-lxd-8` | `neutron_api` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-8 (neutron_api) active process count |
| 122 | `p2_lxd_9_ovn_chassis_ctl_up` | P2 | `juju-65b4ac-0-lxd-9` | `ovn_chassis_ctl` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-9 (ovn_chassis_ctl @ 10.10.10.3) Running status (1=Running) |
| 123 | `p2_lxd_9_ovn_chassis_ctl_mem_mb` | P2 | `juju-65b4ac-0-lxd-9` | `ovn_chassis_ctl` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-9 (ovn_chassis_ctl) cgroup memory consumption (MB) |
| 124 | `p2_lxd_9_ovn_chassis_ctl_procs` | P2 | `juju-65b4ac-0-lxd-9` | `ovn_chassis_ctl` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-9 (ovn_chassis_ctl) active process count |
| 125 | `p2_lxd_10_mysql_innodb_primary_up` | P2 | `juju-65b4ac-0-lxd-10` | `mysql_innodb_primary` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-10 (mysql_innodb_primary @ 10.10.10.6) Running status (1=Running) |
| 126 | `p2_lxd_10_mysql_innodb_primary_mem_mb` | P2 | `juju-65b4ac-0-lxd-10` | `mysql_innodb_primary` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-10 (mysql_innodb_primary) cgroup memory consumption (MB) |
| 127 | `p2_lxd_10_mysql_innodb_primary_procs` | P2 | `juju-65b4ac-0-lxd-10` | `mysql_innodb_primary` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-10 (mysql_innodb_primary) active process count |
| 128 | `p2_lxd_11_ovn_central_up` | P2 | `juju-65b4ac-0-lxd-11` | `ovn_central` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-11 (ovn_central @ 10.10.10.12) Running status (1=Running) |
| 129 | `p2_lxd_11_ovn_central_mem_mb` | P2 | `juju-65b4ac-0-lxd-11` | `ovn_central` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-11 (ovn_central) cgroup memory consumption (MB) |
| 130 | `p2_lxd_11_ovn_central_procs` | P2 | `juju-65b4ac-0-lxd-11` | `ovn_central` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-11 (ovn_central) active process count |
| 131 | `p2_lxd_12_heat_orchestration_up` | P2 | `juju-65b4ac-0-lxd-12` | `heat_orchestration` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-12 (heat_orchestration @ 10.10.10.14) Running status (1=Running) |
| 132 | `p2_lxd_12_heat_orchestration_mem_mb` | P2 | `juju-65b4ac-0-lxd-12` | `heat_orchestration` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-12 (heat_orchestration) cgroup memory consumption (MB) |
| 133 | `p2_lxd_12_heat_orchestration_procs` | P2 | `juju-65b4ac-0-lxd-12` | `heat_orchestration` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-12 (heat_orchestration) active process count |
| 134 | `p2_lxd_13_barbican_keymgr_up` | P2 | `juju-65b4ac-0-lxd-13` | `barbican_keymgr` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-13 (barbican_keymgr @ 10.10.10.15) Running status (1=Running) |
| 135 | `p2_lxd_13_barbican_keymgr_mem_mb` | P2 | `juju-65b4ac-0-lxd-13` | `barbican_keymgr` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-13 (barbican_keymgr) cgroup memory consumption (MB) |
| 136 | `p2_lxd_13_barbican_keymgr_procs` | P2 | `juju-65b4ac-0-lxd-13` | `barbican_keymgr` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-13 (barbican_keymgr) active process count |
| 137 | `p2_lxd_14_octavia_lbaas_up` | P2 | `juju-65b4ac-0-lxd-14` | `octavia_lbaas` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-14 (octavia_lbaas @ 10.10.10.16) Running status (1=Running) |
| 138 | `p2_lxd_14_octavia_lbaas_mem_mb` | P2 | `juju-65b4ac-0-lxd-14` | `octavia_lbaas` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-14 (octavia_lbaas) cgroup memory consumption (MB) |
| 139 | `p2_lxd_14_octavia_lbaas_procs` | P2 | `juju-65b4ac-0-lxd-14` | `octavia_lbaas` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-14 (octavia_lbaas) active process count |
| 140 | `p2_lxd_15_magnum_coe_up` | P2 | `juju-65b4ac-0-lxd-15` | `magnum_coe` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-15 (magnum_coe @ 10.10.10.10) Running status (1=Running) |
| 141 | `p2_lxd_15_magnum_coe_mem_mb` | P2 | `juju-65b4ac-0-lxd-15` | `magnum_coe` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-15 (magnum_coe) cgroup memory consumption (MB) |
| 142 | `p2_lxd_15_magnum_coe_procs` | P2 | `juju-65b4ac-0-lxd-15` | `magnum_coe` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-15 (magnum_coe) active process count |
| 143 | `p2_lxd_16_manila_shares_up` | P2 | `juju-65b4ac-0-lxd-16` | `manila_shares` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-16 (manila_shares @ 10.10.10.20) Running status (1=Running) |
| 144 | `p2_lxd_16_manila_shares_mem_mb` | P2 | `juju-65b4ac-0-lxd-16` | `manila_shares` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-16 (manila_shares) cgroup memory consumption (MB) |
| 145 | `p2_lxd_16_manila_shares_procs` | P2 | `juju-65b4ac-0-lxd-16` | `manila_shares` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-16 (manila_shares) active process count |
| 146 | `p2_lxd_17_designate_bind_up` | P2 | `juju-65b4ac-0-lxd-17` | `designate_bind` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-17 (designate_bind @ 10.10.10.27) Running status (1=Running) |
| 147 | `p2_lxd_17_designate_bind_mem_mb` | P2 | `juju-65b4ac-0-lxd-17` | `designate_bind` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-17 (designate_bind) cgroup memory consumption (MB) |
| 148 | `p2_lxd_17_designate_bind_procs` | P2 | `juju-65b4ac-0-lxd-17` | `designate_bind` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-17 (designate_bind) active process count |
| 149 | `p2_lxd_18_designate_dns_up` | P2 | `juju-65b4ac-0-lxd-18` | `designate_dns` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-18 (designate_dns @ 10.10.10.21) Running status (1=Running) |
| 150 | `p2_lxd_18_designate_dns_mem_mb` | P2 | `juju-65b4ac-0-lxd-18` | `designate_dns` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-18 (designate_dns) cgroup memory consumption (MB) |
| 151 | `p2_lxd_18_designate_dns_procs` | P2 | `juju-65b4ac-0-lxd-18` | `designate_dns` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-18 (designate_dns) active process count |
| 152 | `p2_lxd_19_gnocchi_metricd_up` | P2 | `juju-65b4ac-0-lxd-19` | `gnocchi_metricd` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-19 (gnocchi_metricd @ 10.10.10.23) Running status (1=Running) |
| 153 | `p2_lxd_19_gnocchi_metricd_mem_mb` | P2 | `juju-65b4ac-0-lxd-19` | `gnocchi_metricd` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-19 (gnocchi_metricd) cgroup memory consumption (MB) |
| 154 | `p2_lxd_19_gnocchi_metricd_procs` | P2 | `juju-65b4ac-0-lxd-19` | `gnocchi_metricd` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-19 (gnocchi_metricd) active process count |
| 155 | `p2_lxd_20_ceilometer_polling_up` | P2 | `juju-65b4ac-0-lxd-20` | `ceilometer_polling` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-20 (ceilometer_polling @ 10.10.10.24) Running status (1=Running) |
| 156 | `p2_lxd_20_ceilometer_polling_mem_mb` | P2 | `juju-65b4ac-0-lxd-20` | `ceilometer_polling` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-20 (ceilometer_polling) cgroup memory consumption (MB) |
| 157 | `p2_lxd_20_ceilometer_polling_procs` | P2 | `juju-65b4ac-0-lxd-20` | `ceilometer_polling` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-20 (ceilometer_polling) active process count |
| 158 | `p2_lxd_21_aodh_alarming_up` | P2 | `juju-65b4ac-0-lxd-21` | `aodh_alarming` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-21 (aodh_alarming @ 10.10.10.25) Running status (1=Running) |
| 159 | `p2_lxd_21_aodh_alarming_mem_mb` | P2 | `juju-65b4ac-0-lxd-21` | `aodh_alarming` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-21 (aodh_alarming) cgroup memory consumption (MB) |
| 160 | `p2_lxd_21_aodh_alarming_procs` | P2 | `juju-65b4ac-0-lxd-21` | `aodh_alarming` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-21 (aodh_alarming) active process count |
| 161 | `p2_lxd_22_memcached_cache_up` | P2 | `juju-65b4ac-0-lxd-22` | `memcached_cache` | `binary` | `int` | `input_feature` | juju-65b4ac-0-lxd-22 (memcached_cache @ 10.10.10.26) Running status (1=Running) |
| 162 | `p2_lxd_22_memcached_cache_mem_mb` | P2 | `juju-65b4ac-0-lxd-22` | `memcached_cache` | `MB` | `float` | `input_feature` | juju-65b4ac-0-lxd-22 (memcached_cache) cgroup memory consumption (MB) |
| 163 | `p2_lxd_22_memcached_cache_procs` | P2 | `juju-65b4ac-0-lxd-22` | `memcached_cache` | `count` | `int` | `input_feature` | juju-65b4ac-0-lxd-22 (memcached_cache) active process count |
| 164 | `p2_kvm_inst06_up` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000006` | `binary` | `int` | `input_feature` | KVM domain instance-00000006 (k8s-node-1 (192.168.100.174)) running state |
| 165 | `p2_kvm_inst06_vcpu_time_s` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000006` | `s` | `float` | `input_feature` | KVM domain instance-00000006 cumulative vCPU execution time (s) |
| 166 | `p2_kvm_inst06_vcpu_delay_s` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000006` | `s` | `float` | `input_feature` | KVM domain instance-00000006 cumulative vCPU scheduling delay (s) |
| 167 | `p2_kvm_inst06_rss_mb` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000006` | `MB` | `float` | `input_feature` | KVM domain instance-00000006 host RSS memory footprint (MB) |
| 168 | `p2_kvm_inst06_usable_mb` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000006` | `MB` | `float` | `input_feature` | KVM domain instance-00000006 guest usable memory via virtio-balloon (MB) |
| 169 | `p2_kvm_inst06_net_rx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000006` | `bytes` | `int64` | `input_feature` | KVM domain instance-00000006 OVS tap interface RX bytes |
| 170 | `p2_kvm_inst06_net_tx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000006` | `bytes` | `int64` | `input_feature` | KVM domain instance-00000006 OVS tap interface TX bytes |
| 171 | `p2_kvm_inst06_net_drops` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000006` | `packets` | `int64` | `input_feature` | KVM domain instance-00000006 OVS tap interface dropped packets |
| 172 | `p2_kvm_inst07_up` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000007` | `binary` | `int` | `input_feature` | KVM domain instance-00000007 (k8s-node-0 (192.168.100.131)) running state |
| 173 | `p2_kvm_inst07_vcpu_time_s` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000007` | `s` | `float` | `input_feature` | KVM domain instance-00000007 cumulative vCPU execution time (s) |
| 174 | `p2_kvm_inst07_vcpu_delay_s` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000007` | `s` | `float` | `input_feature` | KVM domain instance-00000007 cumulative vCPU scheduling delay (s) |
| 175 | `p2_kvm_inst07_rss_mb` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000007` | `MB` | `float` | `input_feature` | KVM domain instance-00000007 host RSS memory footprint (MB) |
| 176 | `p2_kvm_inst07_usable_mb` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000007` | `MB` | `float` | `input_feature` | KVM domain instance-00000007 guest usable memory via virtio-balloon (MB) |
| 177 | `p2_kvm_inst07_net_rx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000007` | `bytes` | `int64` | `input_feature` | KVM domain instance-00000007 OVS tap interface RX bytes |
| 178 | `p2_kvm_inst07_net_tx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000007` | `bytes` | `int64` | `input_feature` | KVM domain instance-00000007 OVS tap interface TX bytes |
| 179 | `p2_kvm_inst07_net_drops` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000007` | `packets` | `int64` | `input_feature` | KVM domain instance-00000007 OVS tap interface dropped packets |
| 180 | `p2_kvm_inst08_up` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000008` | `binary` | `int` | `input_feature` | KVM domain instance-00000008 (k8s-master-0 (192.168.100.72)) running state |
| 181 | `p2_kvm_inst08_vcpu_time_s` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000008` | `s` | `float` | `input_feature` | KVM domain instance-00000008 cumulative vCPU execution time (s) |
| 182 | `p2_kvm_inst08_vcpu_delay_s` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000008` | `s` | `float` | `input_feature` | KVM domain instance-00000008 cumulative vCPU scheduling delay (s) |
| 183 | `p2_kvm_inst08_rss_mb` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000008` | `MB` | `float` | `input_feature` | KVM domain instance-00000008 host RSS memory footprint (MB) |
| 184 | `p2_kvm_inst08_usable_mb` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000008` | `MB` | `float` | `input_feature` | KVM domain instance-00000008 guest usable memory via virtio-balloon (MB) |
| 185 | `p2_kvm_inst08_net_rx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000008` | `bytes` | `int64` | `input_feature` | KVM domain instance-00000008 OVS tap interface RX bytes |
| 186 | `p2_kvm_inst08_net_tx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000008` | `bytes` | `int64` | `input_feature` | KVM domain instance-00000008 OVS tap interface TX bytes |
| 187 | `p2_kvm_inst08_net_drops` | P2 | `hpe-PowerEdge-R760xs` | `instance-00000008` | `packets` | `int64` | `input_feature` | KVM domain instance-00000008 OVS tap interface dropped packets |
| 188 | `p2_ovn_compu0_bfd_up` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `binary` | `int` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-0 (to 10.10.10.5) BFD session UP status |
| 189 | `p2_ovn_compu0_flaps` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `count` | `int` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-0 BFD flap count |
| 190 | `p2_ovn_compu0_rx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `bytes` | `int64` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-0 RX bytes |
| 191 | `p2_ovn_compu0_tx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `bytes` | `int64` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-0 TX bytes |
| 192 | `p2_ovn_compu0_rx_pkts` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `packets` | `int64` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-0 RX packets |
| 193 | `p2_ovn_compu0_tx_pkts` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `packets` | `int64` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-0 TX packets |
| 194 | `p2_ovn_compu1_bfd_up` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `binary` | `int` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-1 (to 10.10.10.4) BFD session UP status |
| 195 | `p2_ovn_compu1_flaps` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `count` | `int` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-1 BFD flap count |
| 196 | `p2_ovn_compu1_rx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `bytes` | `int64` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-1 RX bytes |
| 197 | `p2_ovn_compu1_tx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `bytes` | `int64` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-1 TX bytes |
| 198 | `p2_ovn_compu1_rx_pkts` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `packets` | `int64` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-1 RX packets |
| 199 | `p2_ovn_compu1_tx_pkts` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `packets` | `int64` | `causal_graph_node` | OVN Geneve tunnel ovn0-compu-1 TX packets |
| 200 | `p2_ovs_brint_tap_rx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `bytes` | `int64` | `causal_graph_node` | OVS br-int aggregate tap ports RX bytes |
| 201 | `p2_ovs_brint_tap_tx_bytes` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `bytes` | `int64` | `causal_graph_node` | OVS br-int aggregate tap ports TX bytes |
| 202 | `p2_ovs_brint_tap_drops` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `packets` | `int64` | `causal_graph_node` | OVS br-int aggregate tap ports dropped packets |
| 203 | `p2_ovs_brint_tap_errors` | P2 | `hpe-PowerEdge-R760xs` | `ovs-ovn-geneve` | `packets` | `int64` | `causal_graph_node` | OVS br-int aggregate tap ports packet errors |
| 204 | `p3_k8s_nodes_ready` | P3 | `k8s-5g-cluster` | `kubernetes` | `count` | `int` | `causal_graph_node` | Ready Fedora CoreOS 35 Kubernetes nodes in k8s-5g-cluster |
| 205 | `p3_k8s_master0_cpu_m` | P3 | `k8s-5g-cluster` | `kubernetes` | `millicores` | `int` | `causal_graph_node` | Kubernetes master-0 (192.168.100.72) CPU usage in millicores |
| 206 | `p3_k8s_master0_cpu_pct` | P3 | `k8s-5g-cluster` | `kubernetes` | `%` | `float` | `causal_graph_node` | Kubernetes master-0 CPU utilization percentage |
| 207 | `p3_k8s_master0_mem_mib` | P3 | `k8s-5g-cluster` | `kubernetes` | `MiB` | `float` | `causal_graph_node` | Kubernetes master-0 memory usage in MiB |
| 208 | `p3_k8s_master0_mem_pct` | P3 | `k8s-5g-cluster` | `kubernetes` | `%` | `float` | `causal_graph_node` | Kubernetes master-0 memory utilization percentage |
| 209 | `p3_k8s_node0_cpu_m` | P3 | `k8s-5g-cluster` | `kubernetes` | `millicores` | `int` | `causal_graph_node` | Kubernetes node-0 (192.168.100.131) CPU usage in millicores |
| 210 | `p3_k8s_node0_cpu_pct` | P3 | `k8s-5g-cluster` | `kubernetes` | `%` | `float` | `causal_graph_node` | Kubernetes node-0 CPU utilization percentage |
| 211 | `p3_k8s_node0_mem_mib` | P3 | `k8s-5g-cluster` | `kubernetes` | `MiB` | `float` | `causal_graph_node` | Kubernetes node-0 memory usage in MiB |
| 212 | `p3_k8s_node0_mem_pct` | P3 | `k8s-5g-cluster` | `kubernetes` | `%` | `float` | `causal_graph_node` | Kubernetes node-0 memory utilization percentage |
| 213 | `p3_k8s_node1_cpu_m` | P3 | `k8s-5g-cluster` | `kubernetes` | `millicores` | `int` | `causal_graph_node` | Kubernetes node-1 (192.168.100.174) CPU usage in millicores |
| 214 | `p3_k8s_node1_cpu_pct` | P3 | `k8s-5g-cluster` | `kubernetes` | `%` | `float` | `causal_graph_node` | Kubernetes node-1 CPU utilization percentage |
| 215 | `p3_k8s_node1_mem_mib` | P3 | `k8s-5g-cluster` | `kubernetes` | `MiB` | `float` | `causal_graph_node` | Kubernetes node-1 memory usage in MiB |
| 216 | `p3_k8s_node1_mem_pct` | P3 | `k8s-5g-cluster` | `kubernetes` | `%` | `float` | `causal_graph_node` | Kubernetes node-1 memory utilization percentage |
| 217 | `p3_open5gs_pods_ready` | P3 | `k8s-5g-cluster` | `kubernetes` | `count` | `int` | `causal_graph_node` | Healthy Ready pods in open5gs namespace (out of 13) |
| 218 | `p3_open5gs_total_restarts` | P3 | `k8s-5g-cluster` | `kubernetes` | `count` | `int` | `causal_graph_node` | Cumulative container restarts across open5gs 5G Core pods |
| 219 | `p3_open5gs_amf_gnb_connected` | P3 | `k8s-5g-cluster` | `kubernetes` | `count` | `int` | `causal_graph_node` | Active gNodeBs associated with Open5GS AMF via N2 NGAP SCTP :38412 |
| 220 | `p3_open5gs_active_ue_sessions` | P3 | `k8s-5g-cluster` | `kubernetes` | `count` | `int` | `causal_graph_node` | Registered 5G SA UEs in Open5GS AMF/SMF |
| 221 | `p3_open5gs_gtpu_throughput_mbps` | P3 | `k8s-5g-cluster` | `kubernetes` | `Mbps` | `float` | `causal_graph_node` | Open5GS UPF N3 GTP-U user plane tunnel throughput (ogstun 10.45.0.0/16) |
| 222 | `p3_open5gs_n2_ngap_rtt_ms` | P3 | `k8s-5g-cluster` | `kubernetes` | `ms` | `float` | `causal_graph_node` | 5G Control Plane N2 NGAP SCTP round-trip latency (ms) |
| 223 | `p3_open5gs_n4_pfcp_rtt_ms` | P3 | `k8s-5g-cluster` | `kubernetes` | `ms` | `float` | `causal_graph_node` | 5G Control/User Plane SMF-to-UPF N4 PFCP latency (ms) |
| 224 | `p3_boutique_pods_ready` | P3 | `k8s-5g-cluster` | `kubernetes` | `count` | `int` | `causal_graph_node` | Healthy Ready pods in microservices namespace (Google Online Boutique, out of 12) |
| 225 | `p3_boutique_total_restarts` | P3 | `k8s-5g-cluster` | `kubernetes` | `count` | `int` | `causal_graph_node` | Cumulative container restarts across Online Boutique microservices |
| 226 | `p3_boutique_frontend_http_code` | P3 | `k8s-5g-cluster` | `kubernetes` | `http_code` | `int` | `causal_graph_node` | Online Boutique frontend HTTP status code on NodePort :30080 |
| 227 | `p3_boutique_frontend_lat_ms` | P3 | `k8s-5g-cluster` | `kubernetes` | `ms` | `float` | `causal_graph_node` | Online Boutique frontend HTTP response latency (ms) |
| 228 | `p3_nf_mongodb_ready` | P3 | `k8s-5g-cluster` | `open5gs-mongodb` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core MONGODB pod ready status (1=Ready) |
| 229 | `p3_nf_mongodb_restarts` | P3 | `k8s-5g-cluster` | `open5gs-mongodb` | `count` | `int` | `input_feature` | Open5GS 5G SA Core MONGODB container restart count |
| 230 | `p3_nf_nrf_ready` | P3 | `k8s-5g-cluster` | `open5gs-nrf` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core NRF pod ready status (1=Ready) |
| 231 | `p3_nf_nrf_restarts` | P3 | `k8s-5g-cluster` | `open5gs-nrf` | `count` | `int` | `input_feature` | Open5GS 5G SA Core NRF container restart count |
| 232 | `p3_nf_scp_ready` | P3 | `k8s-5g-cluster` | `open5gs-scp` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core SCP pod ready status (1=Ready) |
| 233 | `p3_nf_scp_restarts` | P3 | `k8s-5g-cluster` | `open5gs-scp` | `count` | `int` | `input_feature` | Open5GS 5G SA Core SCP container restart count |
| 234 | `p3_nf_ausf_ready` | P3 | `k8s-5g-cluster` | `open5gs-ausf` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core AUSF pod ready status (1=Ready) |
| 235 | `p3_nf_ausf_restarts` | P3 | `k8s-5g-cluster` | `open5gs-ausf` | `count` | `int` | `input_feature` | Open5GS 5G SA Core AUSF container restart count |
| 236 | `p3_nf_udm_ready` | P3 | `k8s-5g-cluster` | `open5gs-udm` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core UDM pod ready status (1=Ready) |
| 237 | `p3_nf_udm_restarts` | P3 | `k8s-5g-cluster` | `open5gs-udm` | `count` | `int` | `input_feature` | Open5GS 5G SA Core UDM container restart count |
| 238 | `p3_nf_udr_ready` | P3 | `k8s-5g-cluster` | `open5gs-udr` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core UDR pod ready status (1=Ready) |
| 239 | `p3_nf_udr_restarts` | P3 | `k8s-5g-cluster` | `open5gs-udr` | `count` | `int` | `input_feature` | Open5GS 5G SA Core UDR container restart count |
| 240 | `p3_nf_pcf_ready` | P3 | `k8s-5g-cluster` | `open5gs-pcf` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core PCF pod ready status (1=Ready) |
| 241 | `p3_nf_pcf_restarts` | P3 | `k8s-5g-cluster` | `open5gs-pcf` | `count` | `int` | `input_feature` | Open5GS 5G SA Core PCF container restart count |
| 242 | `p3_nf_nssf_ready` | P3 | `k8s-5g-cluster` | `open5gs-nssf` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core NSSF pod ready status (1=Ready) |
| 243 | `p3_nf_nssf_restarts` | P3 | `k8s-5g-cluster` | `open5gs-nssf` | `count` | `int` | `input_feature` | Open5GS 5G SA Core NSSF container restart count |
| 244 | `p3_nf_bsf_ready` | P3 | `k8s-5g-cluster` | `open5gs-bsf` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core BSF pod ready status (1=Ready) |
| 245 | `p3_nf_bsf_restarts` | P3 | `k8s-5g-cluster` | `open5gs-bsf` | `count` | `int` | `input_feature` | Open5GS 5G SA Core BSF container restart count |
| 246 | `p3_nf_amf_ready` | P3 | `k8s-5g-cluster` | `open5gs-amf` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core AMF pod ready status (1=Ready) |
| 247 | `p3_nf_amf_restarts` | P3 | `k8s-5g-cluster` | `open5gs-amf` | `count` | `int` | `input_feature` | Open5GS 5G SA Core AMF container restart count |
| 248 | `p3_nf_smf_ready` | P3 | `k8s-5g-cluster` | `open5gs-smf` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core SMF pod ready status (1=Ready) |
| 249 | `p3_nf_smf_restarts` | P3 | `k8s-5g-cluster` | `open5gs-smf` | `count` | `int` | `input_feature` | Open5GS 5G SA Core SMF container restart count |
| 250 | `p3_nf_upf_ready` | P3 | `k8s-5g-cluster` | `open5gs-upf` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core UPF pod ready status (1=Ready) |
| 251 | `p3_nf_upf_restarts` | P3 | `k8s-5g-cluster` | `open5gs-upf` | `count` | `int` | `input_feature` | Open5GS 5G SA Core UPF container restart count |
| 252 | `p3_nf_webui_ready` | P3 | `k8s-5g-cluster` | `open5gs-webui` | `binary` | `int` | `input_feature` | Open5GS 5G SA Core WEBUI pod ready status (1=Ready) |
| 253 | `p3_nf_webui_restarts` | P3 | `k8s-5g-cluster` | `open5gs-webui` | `count` | `int` | `input_feature` | Open5GS 5G SA Core WEBUI container restart count |
| 254 | `p3_ms_frontend_ready` | P3 | `k8s-5g-cluster` | `frontend` | `binary` | `int` | `input_feature` | Online Boutique frontend pod ready status (1=Ready) |
| 255 | `p3_ms_frontend_restarts` | P3 | `k8s-5g-cluster` | `frontend` | `count` | `int` | `input_feature` | Online Boutique frontend container restart count |
| 256 | `p3_ms_cartservice_ready` | P3 | `k8s-5g-cluster` | `cartservice` | `binary` | `int` | `input_feature` | Online Boutique cartservice pod ready status (1=Ready) |
| 257 | `p3_ms_cartservice_restarts` | P3 | `k8s-5g-cluster` | `cartservice` | `count` | `int` | `input_feature` | Online Boutique cartservice container restart count |
| 258 | `p3_ms_checkoutservice_ready` | P3 | `k8s-5g-cluster` | `checkoutservice` | `binary` | `int` | `input_feature` | Online Boutique checkoutservice pod ready status (1=Ready) |
| 259 | `p3_ms_checkoutservice_restarts` | P3 | `k8s-5g-cluster` | `checkoutservice` | `count` | `int` | `input_feature` | Online Boutique checkoutservice container restart count |
| 260 | `p3_ms_currencyservice_ready` | P3 | `k8s-5g-cluster` | `currencyservice` | `binary` | `int` | `input_feature` | Online Boutique currencyservice pod ready status (1=Ready) |
| 261 | `p3_ms_currencyservice_restarts` | P3 | `k8s-5g-cluster` | `currencyservice` | `count` | `int` | `input_feature` | Online Boutique currencyservice container restart count |
| 262 | `p3_ms_emailservice_ready` | P3 | `k8s-5g-cluster` | `emailservice` | `binary` | `int` | `input_feature` | Online Boutique emailservice pod ready status (1=Ready) |
| 263 | `p3_ms_emailservice_restarts` | P3 | `k8s-5g-cluster` | `emailservice` | `count` | `int` | `input_feature` | Online Boutique emailservice container restart count |
| 264 | `p3_ms_paymentservice_ready` | P3 | `k8s-5g-cluster` | `paymentservice` | `binary` | `int` | `input_feature` | Online Boutique paymentservice pod ready status (1=Ready) |
| 265 | `p3_ms_paymentservice_restarts` | P3 | `k8s-5g-cluster` | `paymentservice` | `count` | `int` | `input_feature` | Online Boutique paymentservice container restart count |
| 266 | `p3_ms_productcatalogservice_ready` | P3 | `k8s-5g-cluster` | `productcatalogservice` | `binary` | `int` | `input_feature` | Online Boutique productcatalogservice pod ready status (1=Ready) |
| 267 | `p3_ms_productcatalogservice_restarts` | P3 | `k8s-5g-cluster` | `productcatalogservice` | `count` | `int` | `input_feature` | Online Boutique productcatalogservice container restart count |
| 268 | `p3_ms_recommendationservice_ready` | P3 | `k8s-5g-cluster` | `recommendationservice` | `binary` | `int` | `input_feature` | Online Boutique recommendationservice pod ready status (1=Ready) |
| 269 | `p3_ms_recommendationservice_restarts` | P3 | `k8s-5g-cluster` | `recommendationservice` | `count` | `int` | `input_feature` | Online Boutique recommendationservice container restart count |
| 270 | `p3_ms_shippingservice_ready` | P3 | `k8s-5g-cluster` | `shippingservice` | `binary` | `int` | `input_feature` | Online Boutique shippingservice pod ready status (1=Ready) |
| 271 | `p3_ms_shippingservice_restarts` | P3 | `k8s-5g-cluster` | `shippingservice` | `count` | `int` | `input_feature` | Online Boutique shippingservice container restart count |
| 272 | `p3_ms_adservice_ready` | P3 | `k8s-5g-cluster` | `adservice` | `binary` | `int` | `input_feature` | Online Boutique adservice pod ready status (1=Ready) |
| 273 | `p3_ms_adservice_restarts` | P3 | `k8s-5g-cluster` | `adservice` | `count` | `int` | `input_feature` | Online Boutique adservice container restart count |
| 274 | `p3_ms_redis_cart_ready` | P3 | `k8s-5g-cluster` | `redis-cart` | `binary` | `int` | `input_feature` | Online Boutique redis-cart pod ready status (1=Ready) |
| 275 | `p3_ms_redis_cart_restarts` | P3 | `k8s-5g-cluster` | `redis-cart` | `count` | `int` | `input_feature` | Online Boutique redis-cart container restart count |
| 276 | `p3_ms_loadgenerator_ready` | P3 | `k8s-5g-cluster` | `loadgenerator` | `binary` | `int` | `input_feature` | Online Boutique loadgenerator pod ready status (1=Ready) |
| 277 | `p3_ms_loadgenerator_restarts` | P3 | `k8s-5g-cluster` | `loadgenerator` | `count` | `int` | `input_feature` | Online Boutique loadgenerator container restart count |
| 278 | `p4_ran_gnb_service_active` | P4 | `compute-pc1` | `srsgnb` | `binary` | `int` | `causal_graph_node` | srsRAN 5G gNodeB systemd service active status on compute-pc1 |
| 279 | `p4_ran_ue1_service_active` | P4 | `compute-pc2` | `srsue1` | `binary` | `int` | `causal_graph_node` | srsRAN 5G UE-1 systemd service active status on compute-pc2 (USRP 34B18A2) |
| 280 | `p4_ran_ue2_service_active` | P4 | `compute-pc2` | `srsue2` | `binary` | `int` | `causal_graph_node` | srsRAN 5G UE-2 systemd service active status on compute-pc2 (USRP 34B1905) |
| 281 | `p4_ran_ue3_service_active` | P4 | `compute-pc2` | `srsue3` | `binary` | `int` | `causal_graph_node` | srsRAN 5G UE-3 systemd service active status on compute-pc2 (USRP #3) |
| 282 | `p4_usrp_b210_detected_pc1` | P4 | `compute-pc1` | `uhd-usrp` | `count` | `int` | `causal_graph_node` | Ettus USRP B210 SDR units detected on compute-pc1 USB 3.0 bus (2500:0020) |
| 283 | `p4_usrp_b210_detected_pc2` | P4 | `compute-pc2` | `uhd-usrp` | `count` | `int` | `causal_graph_node` | Ettus USRP B210 SDR units detected on compute-pc2 USB 3.0 bus (2500:0020) |
| 284 | `p4_usrp_active_rf_channels` | P4 | `cluster-ran` | `ad9361-rfic` | `count` | `int` | `causal_graph_node` | Total active AD9361 RF chains across all 4 USRP B210 SDRs (RF-A + RF-B MIMO/CA) |
| 285 | `p4_ran_band_n78_arfcn` | P4 | `compute-pc1` | `srsgnb-phy` | `arfcn` | `int` | `causal_graph_node` | 5G NR Band n78 TDD Downlink/Uplink ARFCN (658628 = 3879.42 MHz) |
| 286 | `p4_ran_bandwidth_mhz` | P4 | `compute-pc1` | `srsgnb-phy` | `MHz` | `float` | `causal_graph_node` | 5G NR channel bandwidth (MHz) |
| 287 | `p4_ran_gnb_tx_gain_db` | P4 | `compute-pc1` | `srsgnb-phy` | `dB` | `float` | `causal_graph_node` | USRP B210 gNodeB TX gain (dB) |
| 288 | `p4_ran_gnb_rx_gain_db` | P4 | `compute-pc1` | `srsgnb-phy` | `dB` | `float` | `causal_graph_node` | USRP B210 gNodeB RX gain (dB) |
| 289 | `p4_ran_prach_rssi_db` | P4 | `compute-pc1` | `srsgnb-phy` | `dB` | `float` | `causal_graph_node` | 5G Physical Random Access Channel (PRACH) RSSI (dB) |
| 290 | `p4_ran_prach_snr_db` | P4 | `compute-pc1` | `srsgnb-phy` | `dB` | `float` | `causal_graph_node` | 5G PRACH Signal-to-Noise Ratio (dB) |
| 291 | `p4_ran_prach_ta_us` | P4 | `compute-pc1` | `srsgnb-phy` | `us` | `float` | `causal_graph_node` | 5G PRACH Timing Advance (microseconds) |
| 292 | `p4_ran_pusch_sinr_db` | P4 | `compute-pc1` | `srsgnb-phy` | `dB` | `float` | `causal_graph_node` | 5G Physical Uplink Shared Channel (PUSCH) SINR (dB) |
| 293 | `p4_ran_pusch_crc_ok` | P4 | `compute-pc1` | `srsgnb-mac` | `binary` | `int` | `causal_graph_node` | 5G PUSCH transport block CRC check status (1=OK, 0=KO) |
| 294 | `p4_ran_pdsch_rsrp_dbm` | P4 | `compute-pc2` | `srsue-phy` | `dBm` | `float` | `causal_graph_node` | 5G Downlink Reference Signal Received Power RSRP (dBm) |
| 295 | `p4_ran_pdsch_rsrq_db` | P4 | `compute-pc2` | `srsue-phy` | `dB` | `float` | `causal_graph_node` | 5G Downlink Reference Signal Received Quality RSRQ (dB) |
| 296 | `p4_ran_pdsch_sinr_db` | P4 | `compute-pc2` | `srsue-phy` | `dB` | `float` | `causal_graph_node` | 5G Downlink PDSCH SINR (dB) |
| 297 | `p4_ran_dl_cqi` | P4 | `compute-pc2` | `srsue-mac` | `index_0_15` | `int` | `causal_graph_node` | 5G Downlink Channel Quality Indicator (CQI 0..15) |
| 298 | `p4_ran_dl_mcs` | P4 | `compute-pc1` | `srsgnb-mac` | `index_0_28` | `int` | `causal_graph_node` | 5G Downlink Modulation and Coding Scheme index (MCS) |
| 299 | `p4_ran_ul_mcs` | P4 | `compute-pc1` | `srsgnb-mac` | `index_0_28` | `int` | `causal_graph_node` | 5G Uplink Modulation and Coding Scheme index (MCS) |
| 300 | `p4_ran_dl_bler_pct` | P4 | `compute-pc1` | `srsgnb-mac` | `%` | `float` | `causal_graph_node` | 5G Downlink Block Error Rate percentage (BLER %) |
| 301 | `p4_ran_ul_bler_pct` | P4 | `compute-pc1` | `srsgnb-mac` | `%` | `float` | `causal_graph_node` | 5G Uplink Block Error Rate percentage (BLER %) |
| 302 | `p4_ran_dl_bitrate_mbps` | P4 | `compute-pc1` | `srsgnb-rlc` | `Mbps` | `float` | `causal_graph_node` | 5G NR Downlink RLC/PDCP throughput (Mbps) |
| 303 | `p4_ran_ul_bitrate_mbps` | P4 | `compute-pc1` | `srsgnb-rlc` | `Mbps` | `float` | `causal_graph_node` | 5G NR Uplink RLC/PDCP throughput (Mbps) |
| 304 | `p4_ran_usb_overflows` | P4 | `compute-pc1` | `uhd-usb3` | `count` | `int` | `causal_graph_node` | USRP B210 USB 3.0 RX overflow event count (O) |
| 305 | `p4_ran_usb_underruns` | P4 | `compute-pc1` | `uhd-usb3` | `count` | `int` | `causal_graph_node` | USRP B210 USB 3.0 TX underrun event count (U) |
| 306 | `p4_ran_usb_late_pkts` | P4 | `compute-pc1` | `uhd-usb3` | `count` | `int` | `causal_graph_node` | USRP B210 USB 3.0 late timestamp packet count (L) |
| 307 | `p4_wifi_mist_ap_online` | P4 | `mist-ap43` | `mist-wlan` | `binary` | `int` | `causal_graph_node` | Mist AP43 Enterprise Wi-Fi Access Point (VLAN 20) online status |
| 308 | `p4_wifi_rssi_dbm` | P4 | `mist-ap43` | `mist-wlan` | `dBm` | `float` | `causal_graph_node` | Mist Wi-Fi SSID 5G-AIOps-Lab client RSSI (dBm) |
| 309 | `p4_wifi_snr_db` | P4 | `mist-ap43` | `mist-wlan` | `dB` | `float` | `causal_graph_node` | Mist Wi-Fi SSID 5G-AIOps-Lab client SNR (dB) |
| 310 | `p4_wifi_tx_mbps` | P4 | `mist-ap43` | `mist-wlan` | `Mbps` | `float` | `causal_graph_node` | Mist Wi-Fi 5GHz downlink PHY throughput (Mbps) |
| 311 | `p4_juniper_srx300_rtt_ms` | P4 | `juniper-srx300` | `wan-gateway` | `ms` | `float` | `causal_graph_node` | Juniper SRX300 Gateway (10.0.0.1) ICMP round-trip latency (ms) |
| 312 | `p5_wazuh_manager_up` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `binary` | `int` | `security_feature` | Wazuh SIEM Manager v4.8.0 service active status on Dell R760xs |
| 313 | `p5_wazuh_indexer_up` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `binary` | `int` | `security_feature` | Wazuh OpenSearch Indexer (:9200) active status |
| 314 | `p5_wazuh_agent_000_dell_up` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `binary` | `int` | `security_feature` | Wazuh Agent 000 (hpe-PowerEdge-R760xs) active status |
| 315 | `p5_wazuh_agent_002_pc1_up` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `binary` | `int` | `security_feature` | Wazuh Agent 002 (compute-pc1 10.10.10.4) active status |
| 316 | `p5_wazuh_agent_003_pc2_up` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `binary` | `int` | `security_feature` | Wazuh Agent 003 (compute-pc2 10.10.10.5) active status |
| 317 | `p5_wazuh_agent_004_win_up` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `binary` | `int` | `security_feature` | Wazuh Agent 004 (Windows Jump Host 10.0.0.21) active status |
| 318 | `p5_wazuh_alerts_total_cum` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Cumulative Wazuh SIEM alerts in /var/ossec/logs/alerts/alerts.json |
| 319 | `p5_wazuh_alerts_delta_tick` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int` | `security_feature` | New Wazuh SIEM alerts generated during current collection tick |
| 320 | `p5_wazuh_alerts_agent_dell` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Cumulative Wazuh alerts attributed to Agent 000 (Dell R760xs) |
| 321 | `p5_wazuh_alerts_agent_pc1` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Cumulative Wazuh alerts attributed to Agent 002 (compute-pc1) |
| 322 | `p5_wazuh_alerts_agent_pc2` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Cumulative Wazuh alerts attributed to Agent 003 (compute-pc2) |
| 323 | `p5_wazuh_alerts_agent_win` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Cumulative Wazuh alerts attributed to Agent 004 (Windows Jump Host) |
| 324 | `p5_wazuh_sev_level_1_3` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Wazuh alerts at Severity Level 1-3 (Informational / PAM Session) |
| 325 | `p5_wazuh_sev_level_4_6` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Wazuh alerts at Severity Level 4-6 (Low / System & Sudo Events) |
| 326 | `p5_wazuh_sev_level_7_9` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Wazuh alerts at Severity Level 7-9 (Medium / CIS Benchmark & FIM) |
| 327 | `p5_wazuh_sev_level_10_11` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Wazuh alerts at Severity Level 10-11 (High / Service Failure / Brute Force) |
| 328 | `p5_wazuh_sev_level_12plus` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Wazuh alerts at Severity Level 12+ (Critical / High-Risk Threat) |
| 329 | `p5_wazuh_mitre_auth_events` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Wazuh MITRE ATT&CK T1078 Valid Accounts / Authentication events |
| 330 | `p5_wazuh_mitre_priv_esc` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int64` | `security_feature` | Wazuh MITRE ATT&CK Privilege Escalation / Sudo events |
| 331 | `p5_wazuh_active_responses_total` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `count` | `int` | `security_feature` | Wazuh Active Response automated firewall/remediation executions |
| 332 | `p5_wazuh_last_rule_id` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `rule_id` | `int` | `security_feature` | Most recent Wazuh SIEM triggered rule ID |
| 333 | `p5_wazuh_last_rule_level` | P5 | `hpe-PowerEdge-R760xs` | `wazuh-siem` | `level` | `int` | `security_feature` | Most recent Wazuh SIEM triggered rule severity level |
| 334 | `p6_gpu0_pc1_util_pct` | P6 | `compute-pc1` | `intel-uhd-770-gpu0` | `%` | `float` | `input_feature` | Compute-PC1 Intel UHD Graphics 770 (GPU0 /dev/dri/renderD128) utilization % |
| 335 | `p6_gpu0_pc1_vram_used_mb` | P6 | `compute-pc1` | `intel-uhd-770-gpu0` | `MB` | `float` | `input_feature` | Compute-PC1 GPU0 shared VRAM allocated (MB) |
| 336 | `p6_gpu0_pc1_clock_mhz` | P6 | `compute-pc1` | `intel-uhd-770-gpu0` | `MHz` | `float` | `input_feature` | Compute-PC1 GPU0 render clock frequency (MHz) |
| 337 | `p6_gpu0_pc1_gflops` | P6 | `compute-pc1` | `intel-uhd-770-gpu0` | `GFLOPS` | `float` | `input_feature` | Compute-PC1 GPU0 measured FP32 tensor throughput (GFLOPS) |
| 338 | `p6_gpu0_pc1_batch_lat_ms` | P6 | `compute-pc1` | `intel-uhd-770-gpu0` | `ms` | `float` | `input_feature` | Compute-PC1 GPU0 micro-batch inference latency (ms) |
| 339 | `p6_gpu1_pc2_util_pct` | P6 | `compute-pc2` | `intel-uhd-770-gpu1` | `%` | `float` | `input_feature` | Compute-PC2 Intel UHD Graphics 770 (GPU1 /dev/dri/renderD128) utilization % |
| 340 | `p6_gpu1_pc2_vram_used_mb` | P6 | `compute-pc2` | `intel-uhd-770-gpu1` | `MB` | `float` | `input_feature` | Compute-PC2 GPU1 shared VRAM allocated (MB) |
| 341 | `p6_gpu1_pc2_clock_mhz` | P6 | `compute-pc2` | `intel-uhd-770-gpu1` | `MHz` | `float` | `input_feature` | Compute-PC2 GPU1 render clock frequency (MHz) |
| 342 | `p6_gpu1_pc2_gflops` | P6 | `compute-pc2` | `intel-uhd-770-gpu1` | `GFLOPS` | `float` | `input_feature` | Compute-PC2 GPU1 measured FP32 tensor throughput (GFLOPS) |
| 343 | `p6_gpu1_pc2_batch_lat_ms` | P6 | `compute-pc2` | `intel-uhd-770-gpu1` | `ms` | `float` | `input_feature` | Compute-PC2 GPU1 micro-batch inference latency (ms) |
| 344 | `p6_dell_xeon_amx_gflops` | P6 | `hpe-PowerEdge-R760xs` | `xeon-5418y-amx` | `GFLOPS` | `float` | `input_feature` | Dell Dual Xeon Gold 5418Y AVX-512/AMX matrix engine throughput (GFLOPS) |
| 345 | `p6_dell_tensor_workers` | P6 | `hpe-PowerEdge-R760xs` | `xeon-5418y-amx` | `count` | `int` | `input_feature` | Active parallel tensor compute worker processes on Dell R760xs |
| 346 | `p6_cluster_total_ai_gflops` | P6 | `cluster-ai` | `distributed-compute` | `GFLOPS` | `float` | `input_feature` | Combined cluster AI compute throughput (Dell AMX + GPU0 + GPU1 GFLOPS) |
| 347 | `p6_xie_zscore_cpu` | P6 | `hpe-PowerEdge-R760xs` | `xie-detector` | `z_score` | `float` | `input_feature` | XIE Tier-1 rolling Z-score for compute CPU load |
| 348 | `p6_xie_zscore_mem` | P6 | `hpe-PowerEdge-R760xs` | `xie-detector` | `z_score` | `float` | `input_feature` | XIE Tier-1 rolling Z-score for controller memory utilization |
| 349 | `p6_xie_zscore_sinr` | P6 | `hpe-PowerEdge-R760xs` | `xie-detector` | `z_score` | `float` | `input_feature` | XIE Tier-1 rolling Z-score for 5G RAN PUSCH SINR |
| 350 | `p6_xie_zscore_drops` | P6 | `hpe-PowerEdge-R760xs` | `xie-detector` | `z_score` | `float` | `input_feature` | XIE Tier-1 rolling Z-score for SDN/NIC packet drops |
| 351 | `p6_xie_zscore_pods` | P6 | `hpe-PowerEdge-R760xs` | `xie-detector` | `z_score` | `float` | `input_feature` | XIE Tier-1 rolling Z-score for Open5GS healthy pod count |
| 352 | `p6_xie_rf_prob_nominal` | P6 | `hpe-PowerEdge-R760xs` | `xie-rf-classifier` | `probability` | `float` | `input_feature` | Random Forest posterior probability P(y = nominal | x_t) |
| 353 | `p6_xie_rf_prob_cpu_exhaustion` | P6 | `hpe-PowerEdge-R760xs` | `xie-rf-classifier` | `probability` | `float` | `input_feature` | Random Forest posterior probability P(y = compute_cpu_exhaustion | x_t) |
| 354 | `p6_xie_rf_prob_k8s_crash` | P6 | `hpe-PowerEdge-R760xs` | `xie-rf-classifier` | `probability` | `float` | `input_feature` | Random Forest posterior probability P(y = k8s_container_crash | x_t) |
| 355 | `p6_xie_rf_prob_ovn_loss` | P6 | `hpe-PowerEdge-R760xs` | `xie-rf-classifier` | `probability` | `float` | `input_feature` | Random Forest posterior probability P(y = ovn_sdn_latency_loss | x_t) |
| 356 | `p6_xie_rf_prob_rf_attenuation` | P6 | `hpe-PowerEdge-R760xs` | `xie-rf-classifier` | `probability` | `float` | `input_feature` | Random Forest posterior probability P(y = rf_path_loss_attenuation | x_t) |
| 357 | `p6_xie_ppr_score_cpu` | P6 | `hpe-PowerEdge-R760xs` | `xie-causal-ppr` | `ppr_score` | `float` | `input_feature` | Reversed-DAG Personalized PageRank attribution score pi(compute_cpu) |
| 358 | `p6_xie_ppr_score_ovn` | P6 | `hpe-PowerEdge-R760xs` | `xie-causal-ppr` | `ppr_score` | `float` | `input_feature` | Reversed-DAG Personalized PageRank attribution score pi(ovn_geneve_sdn) |
| 359 | `p6_xie_ppr_score_k8s` | P6 | `hpe-PowerEdge-R760xs` | `xie-causal-ppr` | `ppr_score` | `float` | `input_feature` | Reversed-DAG Personalized PageRank attribution score pi(k8s_open5gs_core) |
| 360 | `p6_xie_ppr_score_ran` | P6 | `hpe-PowerEdge-R760xs` | `xie-causal-ppr` | `ppr_score` | `float` | `input_feature` | Reversed-DAG Personalized PageRank attribution score pi(srsran_usrp_phy) |
| 361 | `p6_xie_granger_max_weight` | P6 | `hpe-PowerEdge-R760xs` | `xie-var2-granger` | `weight` | `float` | `input_feature` | Maximum active VAR(2) Granger causal edge weight W_ij |
| 362 | `p6_xie_chromadb_episodes` | P6 | `hpe-PowerEdge-R760xs` | `chromadb-hnsw` | `count` | `int` | `input_feature` | Total incident episodes stored in ChromaDB HNSW vector memory |
| 363 | `p6_xie_chromadb_top_sim` | P6 | `hpe-PowerEdge-R760xs` | `chromadb-hnsw` | `cosine_sim` | `float` | `input_feature` | Top-1 ChromaDB episodic memory cosine similarity score |
| 364 | `p6_xie_remediations_total` | P6 | `hpe-PowerEdge-R760xs` | `mcp-orchestrator` | `count` | `int` | `input_feature` | Cumulative autonomous closed-loop remediations executed |
| 365 | `p6_xie_remediations_ppr` | P6 | `hpe-PowerEdge-R760xs` | `mcp-orchestrator` | `count` | `int` | `input_feature` | Remediations triggered by Causal-PPR engine |
| 366 | `p6_xie_remediations_zeroshot` | P6 | `hpe-PowerEdge-R760xs` | `mcp-orchestrator` | `count` | `int` | `input_feature` | Remediations triggered by ChromaDB Zero-Shot episodic memory |
| 367 | `p6_xie_last_mttr_sec` | P6 | `hpe-PowerEdge-R760xs` | `mcp-orchestrator` | `s` | `float` | `input_feature` | Most recent autonomous remediation Mean Time To Remediate (s) |
| 368 | `p6_xie_ollama_qwen3_online` | P6 | `windows-jump-host` | `ollama-qwen3-14b` | `binary` | `int` | `input_feature` | Ollama Qwen3-14B LLM inference server (10.0.0.21:11434) online status |
