# Junior Knowledge Transfer (KT), Operational Safety & Disaster Recovery Guide
## Autonomous Cross-Layer 5G SA Telco-Cloud, Distributed Dual-GPU/AMX Compute, Wazuh SIEM & Explainable Agentic AIOps

Welcome to the lab! This testbed is **100% operational across all 6 architectural planes** and is protected by an automated **Golden State Persistence Guardian (`system-golden-guardian.service`)** and an **Immutable Golden State Backup Vault (`/data_16tb/GOLDEN_STATE_VAULT/`)**.

Read this guide carefully before running commands on the cluster.

---

## 1. The 4 Essential Commands Every Operator Must Know

Run these commands from any terminal on `hpe-PowerEdge-R760xs` (`10.0.0.10`):

| Command | What It Does | When to Use It |
| :--- | :--- | :--- |
| **`verify-golden-state`** | Runs a **24-point automated health check** across all 6 planes (Storage, SSH to `compute-pc1`/`pc2`, OpenStack 23 LXD containers, Horizon login, KVM VMs, OVN Geneve tunnels, K8s 3 nodes, 13 Open5GS pods, 12 Online Boutique pods, 4 USRP B210 SDRs, Wazuh SIEM, 4 MCP servers, XIE Agent, and Dataset Warehouse). | Run daily or before any demo/review to confirm `24 / 24 CHECKS PASSED`. |
| **`dataset-status`** | Displays real-time counters, tensor shapes (`(90368+, 360)`), log counts across all 6 planes, and free capacity on the `16.77 TB` RAID storage pool. | Run anytime to inspect the live multi-dimensional AI training dataset. |
| **`run-video-demo`** | Launches the interactive 7-scene terminal walkthrough (`Press [ENTER]` between scenes). | Run during live demonstrations or video recordings. |
| **`sudo restore-golden-state`** | **One-Click Disaster Recovery & Rollback**: Restores all Python code, ML models, ChromaDB vector memory, systemd services, Kubernetes `kubeconfig`, network bridges (`veth-host`/`br-ex`), `proxy_arp=0`, Horizon FDB/ARP entries, and restarts all daemons from `/data_16tb/GOLDEN_STATE_VAULT/`. | Run immediately if anyone accidentally modifies/deletes a script, breaks a bridge, or stops services! |

---

## 2. How the Setup Protects Itself Automatically (`system-golden-guardian.service`)

Even if the server is rebooted or someone accidentally stops a service, **`system-golden-guardian.service`** runs at boot and every 60 seconds in the background to automatically enforce:
1. **Storage Mounts**: Ensures `/data` (`2.95 TB`) and `/data_16tb` (`14.0 TB`) remain mounted.
2. **Floating IP & Provider Bridge Persistence**: Recreates `veth-host` (`172.24.4.254/24`) $\leftrightarrow$ `veth-br` (in OVS `br-ex`), loopback aliases (`10.228.0.92`, `10.0.0.215`, `10.0.0.206`, `10.0.0.232`), and `iptables` NAT `MASQUERADE` rules for `172.24.4.0/24` and `192.168.100.0/24`.
3. **Horizon Proxy-ARP & Permanent FDB/ARP Protection**: Enforces `net.ipv4.conf.br-data.proxy_arp=0` and runs `/usr/local/bin/openstack-horizon-guard.sh` so OpenStack Horizon (`10.10.10.8`) and Keystone (`10.10.10.9`) never experience ARP/MAC flapping.
4. **KVM Virtual Machines & LXD Containers**: Automatically restarts `instance-00000006` (`k8s-node-1`), `instance-00000007` (`k8s-node-0`), or `instance-00000008` (`k8s-master-0`) if any VM is shut off.
5. **All Critical Systemd Daemons**: Auto-restarts `omni-crosslayer-harvester`, `self-healing-agent`, `multi-domain-exporter`, `grafana-prometheus`, `5g-telemetry`, `mcp-dcops` (`:8101`), `mcp-devops` (`:8102`), `mcp-secops` (`:8103`), `mcp-aiops` (`:8104`), `wazuh-manager`, `wazuh-indexer`, `wazuh-dashboard`, plus `srsgnb`, `srsue1`, `srsue2`, and `node-monitor-tty1` on `compute-pc1` (`10.10.10.4`) and `compute-pc2` (`10.10.10.5`).

---

## 3. Golden Safety Rules for Juniors (Do's & Don'ts)

### DO:
- **DO** work inside a separate git branch or copy datasets from `/home/hpe/HPE/cross_layer_dataset/` to your own experiment folder when training new PyTorch/Scikit-Learn models.
- **DO** use `verify-golden-state` to check cluster health before and after running experiments.
- **DO** use `/home/hpe/telemetry/fault_injector.py` or `/home/hpe/demo_harness.py` if you want to test fault injection—the XIE self-healing agent will automatically detect and remediate the fault in `< 1 second`.

### DO NOT:
1. **DO NOT delete or format `/data` or `/data_16tb`**:
   - `/data/cross_layer_dataset` holds the live growing multi-million-cell dataset warehouse.
   - `/data_16tb/GOLDEN_STATE_VAULT` and `/data_16tb/GOLDEN_STATE_MASTER_ARCHIVE_20261121.tar.gz` (locked with kernel `chattr +i` immutable flag) hold the full disaster-recovery snapshot of the cluster.
2. **DO NOT enable `proxy_arp=1` on `br-data`**:
   - Keep `net.ipv4.conf.br-data.proxy_arp=0` at all times so the Dell host does not intercept ARP broadcast frames between the 23 Juju LXD containers inside `openstack-ctl`.
3. **DO NOT stop or delete `openstack-ctl` or KVM instances `instance-00000006/7/8`**:
   - `openstack-ctl` (`10.10.10.3`) hosts all 23 OpenStack control-plane containers.
   - `instance-00000006`, `00000007`, and `00000008` are the 3 Fedora CoreOS Magnum Kubernetes nodes hosting the 13 Open5GS 5G Core NFs and 12 Online Boutique microservices.
4. **DO NOT unplug the 4 Ettus USRP B210 USB 3.0 cables**:
   - `compute-pc1` (`10.10.10.4`) drives the gNodeB USRP B210 (`34B18C8`), and `compute-pc2` (`10.10.10.5`) drives the 3 UE USRP B210 units (`34B18A2`, `34B1905`, USRP #3).

---

## 4. How to Recover If Something Goes Wrong

### Case A: A script, config, service, or bridge was accidentally modified or stopped
Simply run:
```bash
sudo restore-golden-state
```
This restores all scripts, ML models, ChromaDB vector memory, systemd service files, Kubernetes `kubeconfig`, and network bridges from `/data_16tb/GOLDEN_STATE_VAULT/`, restarts all services, and runs the 24-point verification check.

### Case B: An OpenStack LXD container or `openstack-ctl` needs a full VM-level rollback
We took a full LXD storage snapshot of `openstack-ctl` named `golden-healthy-20261121`, plus a full MySQL 8.0 InnoDB cluster dump at `/data_16tb/GOLDEN_STATE_VAULT/02_openstack_and_lxd_snapshots/mysql_innodb_all_databases.sql.gz`:
```bash
# View the LXD golden snapshot
sudo lxc info openstack-ctl | grep -A 5 "Snapshots:"

# Restore openstack-ctl to the golden LXD snapshot if ever required
sudo lxc restore openstack-ctl golden-healthy-20261121
sudo /usr/local/bin/openstack-horizon-guard.sh
```

### Case C: A Kubernetes deployment in `open5gs` or `microservices` was deleted
Full YAML manifests of every namespace are saved in `/data_16tb/GOLDEN_STATE_VAULT/04_kubernetes_5gcore_and_microservices/` (and in `/home/hpe/HPE/configs/kubernetes_manifests/`):
```bash
kubectl apply -f /home/hpe/HPE/configs/kubernetes_manifests/open5gs_namespace_full.yaml
kubectl apply -f /home/hpe/HPE/configs/kubernetes_manifests/microservices_namespace_full.yaml
```

