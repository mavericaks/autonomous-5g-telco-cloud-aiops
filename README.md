# Autonomous Cross-Layer 5G SA Telco-Cloud, Distributed Dual-GPU/AMX Compute, Wazuh SIEM & Explainable Agentic AIOps

> **Motto:** ***"Zero-Touch, Explainable, Cross-Layer Autonomous Self-Healing — From Physical 5G RF Silicon to Cloud-Native Microservices."***

![Operational Status](https://img.shields.io/badge/Golden_State_Health-24%2F24_Checks_Passed-success?style=for-the-badge)
![Mean MTTR](https://img.shields.io/badge/Mean_MTTR-0.354_Seconds_(99.97%25_Faster)-0284c7?style=for-the-badge)
![Cascading RCA Accuracy](https://img.shields.io/badge/Cascading_RCA_Accuracy-98.33%25_(Reversed--DAG_PPR)-0d9488?style=for-the-badge)
![5G NR RAN](https://img.shields.io/badge/5G_NR_Band_n78-4x_Ettus_USRP_B210_(8_RF_Chains)-15803d?style=for-the-badge)
![AI Compute](https://img.shields.io/badge/Distributed_AI_Fabric-960%2B_GFLOPS_(Dual_GPU_%2B_Xeon_AMX)-7e22ce?style=for-the-badge)
![Dataset Warehouse](https://img.shields.io/badge/6--Plane_Dataset-368_Params_%7C_16.77_TB_RAID_Pool-b45309?style=for-the-badge)

---

## 1. Executive Overview & Vision

Modern 5G Standalone (SA) Telco-Cloud deployments are deeply layered cyber-physical systems spanning **bare-metal dual-socket NUMA servers**, **OpenStack/KVM virtualization**, **OVN/OVS Geneve software-defined networking (SDN)**, **Kubernetes cloud-native microservices**, **3GPP Release-17 5G Core network functions**, **physical Software-Defined Radio (SDR) transceivers**, **SIEM security operations**, and **distributed AI accelerators**.

In such environments, a single physical or virtual fault—such as packet loss on an OVN Geneve tunnel (`br-int`) or radio path-loss attenuation on a USRP B210 antenna—propagates vertically and horizontally within milliseconds, triggering a **cascading alarm storm** across Kubernetes readiness probes, 5G AMF/UPF SCTP/GTP-U tunnels, and application frontends.
- **Traditional Threshold & Rule Engines** evaluate metrics in isolation, confusing downstream symptoms with the root cause ($42.50\%$ accuracy under cascading faults).
- **Black-Box Deep Neural Models & Direct LLM Prompts** lack mathematical attribution guarantees and incur $8$–$30\text{ s}$ inference latency, making them unsafe for autonomous control-plane actuation.

### What This Repository Delivers
This repository contains the complete production source code, configurations, mathematical models, FastMCP servers, multi-dimensional dataset harvester, disaster-recovery golden-state scripts, and publication documentation for our **6-Plane Physical 5G SA Telco-Cloud & Explainable Agentic AIOps Testbed**:

![Complete 6-Plane System Architecture](docs/figures/fig_4_1_system_architecture.png)

1. **Physical 6-Plane Multi-Node Infrastructure**:
   - **Plane 1 (Bare-Metal Hardware, NUMA & 16.77 TB RAID Storage)**: Dell PowerEdge R760xs (`96 threads` Dual Xeon Gold 5418Y, `503 GiB` DDR5 ECC RAM, `16.77 TB` PERC H755 RAID storage across `/data` and `/data_16tb`) + `compute-pc1` (`10.10.10.4`, Core i9-14900K `32 threads`, `62 GiB` RAM) + `compute-pc2` (`10.10.10.5`, Core i9-14900K `32 threads`, `62 GiB` RAM) + Windows GPU Jump Host (`10.0.0.21`).
   - **Plane 2 (OpenStack 2023.1 Antelope Control Plane, KVM & OVN/OVS SDN)**: `openstack-ctl` VM (`10.10.10.3`) hosting **23 Juju LXD service containers** (`lxd-0` to `lxd-22`), **3 Nova KVM hypervisors** hosting **7 active KVM instances**, and **BFD-monitored OVS/OVN Geneve tunnels** (`ovn0-compu-0`, `ovn0-compu-1`).
   - **Plane 3 (Magnum Kubernetes v1.23.3, Open5GS 5G SA Core & Online Boutique)**: 3 Fedora CoreOS Kubernetes nodes (`master-0`, `node-0`, `node-1`) running **13 Open5GS 5G SA Core Network Functions** (`NRF`, `SCP`, `AMF`, `SMF`, `UPF`, `AUSF`, `UDM`, `UDR`, `PCF`, `NSSF`, `BSF`, `WebUI`, `MongoDB`) and **12 Google Online Boutique microservices**.
   - **Plane 4 (Physical 5G NR Band n78 SDR RAN — 4x Ettus USRP B210)**: 1x USRP B210 (`34B18C8`) on `compute-pc1` running `srsRAN` 5G gNodeB (`3879.42 MHz`, ARFCN `658628`, `20 MHz` BW) + 3x USRP B210 SDRs (`34B18A2`, `34B1905`, USRP #3) on `compute-pc2` running 5G SA UEs (`srsue1`, `srsue2`) across **8 active AD9361 RF chains**, plus **Mist AP43 Wi-Fi 6** and **Juniper SRX300** gateway telemetry.
   - **Plane 5 (Wazuh SIEM v4.8.0 Security Operations)**: Central Wazuh Manager + OpenSearch Indexer + 4 enrolled agents (`000`–`004`), correlating **600,000+ security alerts** across PAM/SSH, File Integrity Monitoring (FIM), CIS benchmarks, and MITRE ATT&CK tactics (`T1078`).
   - **Plane 6 (Distributed Dual-GPU/AMX Compute & Experiential Intelligence Engine [XIE Core v1.0])**: Combines Dual Intel UHD Graphics 770 GPUs (`GPU0` PC1, `GPU1` PC2) + Dual Xeon Gold 5418Y AMX (`960+ GFLOPS` combined), Ollama `qwen3:14b` LLM, **XIE Core v1.0** (Rolling Z-Score + 100-Tree Random Forest + ChromaDB HNSW Episodic Memory + Lag-2 VAR(2) Granger Causality + Reversed-DAG Personalized PageRank $\boldsymbol{\pi}$), and **4 Domain-Specific FastMCP Servers** (`mcp-dcops`, `mcp-devops`, `mcp-secops`, `mcp-aiops`).

---

## 2. Repository Directory Structure

```text
autonomous-5g-telco-cloud-aiops/
├── README.md                                           # Comprehensive Architecture, Setup, Math & KT Manual
├── .gitignore                                          # Excludes multi-GB live databases/archives from Git push
├── src/
│   ├── xie_core/                                       # Experiential Intelligence Engine (XIE Core v1.0)
│   │   ├── causal_discovery.py                         # Lag-2 VAR(2) Granger causality F-test & DAG builder
│   │   ├── causal_rca.py                               # Reversed-DAG Personalized PageRank (pi) root-cause solver
│   │   ├── episodic_memory.py                          # ChromaDB HNSW vector memory for <100ms Zero-Shot recovery
│   │   ├── dataset_loader.py                           # Multi-tier telemetry stream loader & normalizer
│   │   └── models/causal_dag.json                      # Learned cross-layer causal adjacency graph
│   ├── agent/                                          # Closed-Loop Self-Healing Agent & LLM Post-Mortem Engine
│   │   ├── self_healing_agent.py                       # 5-Tier autonomous detection, RCA & actuation daemon
│   │   ├── llm_reporter.py                             # Asynchronous Ollama Qwen3-14B Markdown post-mortem generator
│   │   ├── train_model.py                              # 100-tree Random Forest anomaly classifier trainer (99.97% acc)
│   │   └── models/                                     # Trained anomaly_detector.pkl & feature_metadata.json
│   ├── mcp_servers/                                    # 4 Domain-Specific Model Context Protocol (FastMCP) Servers
│   │   ├── central_agent.py                            # Multi-domain coordinator & full-stack health auditor
│   │   ├── mcp_http_daemon.py                          # JSON-RPC / HTTP daemon wrapper (:8101-:8104)
│   │   ├── mcp_dcops_server.py                         # Plane 1 & 2: Bare-Metal, OpenStack 2023.1 & OVN SDN (:8101)
│   │   ├── mcp_devops_server.py                        # Plane 3: Magnum K8s, Open5GS 5G Core & Boutique (:8102)
│   │   ├── mcp_secops_server.py                        # Plane 5: Wazuh SIEM v4.8.0 & Active Response (:8103)
│   │   └── mcp_aiops_server.py                         # Plane 6: XIE Causal PPR & ChromaDB Vector Memory (:8104)
│   ├── observability_and_gateway/                      # Prometheus, Grafana, Multi-Domain Exporter & GPU/AMX Engine
│   │   ├── multi_domain_exporter.py                    # Unified 6-Plane Prometheus Exporter (:9105)
│   │   ├── grafana_and_prometheus_server.py            # Prometheus (:9090) & Grafana (:3000) Observability Server
│   │   ├── k8s_and_cloud_gateway.py                    # Universal TCP/HTTP Gateway & Cloud Portal (:8081-:8444)
│   │   ├── gpu_and_cpu_workload.py                     # Distributed Dual UHD 770 GPU + Xeon AMX Tensor Engine
│   │   ├── collector.py                                # Core 5G RAN/Core telemetry collector
│   │   ├── telemetry_daemon.py                         # 5g-telemetry.service daemon entrypoint
│   │   └── fault_injector.py                           # Controlled multi-domain fault injection harness
│   └── dataset_harvester/                              # Continuous 6-Plane 368-Parameter + Log/Alert Data Factory
│       ├── omni_schema_and_harvester.py                # Parallel 368-feature collector & schema dictionary generator
│       ├── omni_log_harvester_and_warehouse.py         # Cursor-based log/alert tailer, SQLite WAL & 16TB auto-tiering
│       ├── omni_harvester_daemon.py                    # omni-crosslayer-harvester.service continuous daemon
│       ├── bootstrap_historical_dataset.py             # Historical multi-plane backfill & multi-class labeler
│       └── inspect_dataset.py                          # O(1) fast CLI inspector (`dataset-status`)
├── configs/
│   ├── systemd/                                        # All systemd service units (Dell R760xs, compute-pc1, compute-pc2)
│   ├── kubernetes_manifests/                           # Complete YAML manifests for open5gs (13 NFs) & microservices (12 pods)
│   ├── srsran_usrp/                                    # USRP B210 Band n78 gNodeB & Multi-UE configurations
│   └── openstack_and_network/                          # 23 Juju LXD inventory, sysctl proxy_arp hardening & OVS topology
├── dataset_schema_and_samples/                         # Complete 368-Feature Schema & 100-Row Sample Datasets
│   ├── FEATURE_CATALOG.md                              # Human-readable table of all 368 cross-layer parameters
│   ├── feature_dictionary.json                         # Machine-readable JSON schema of all 368 parameters & 14 log fields
│   ├── dataset_manifest.json                           # Live warehouse volume, tensor shapes & disk health manifest
│   ├── sustainability_policy.json                      # 250MB gzip rotation & 16.77 TB storage tiering policy
│   ├── sample_100_cross_layer_metrics.csv              # 100-row × 368-column sample of the wide time-series matrix
│   └── sample_100_logs_alerts_stream.csv               # 100-row × 14-column sample of the unified 6-plane log corpus
├── scripts/                                            # Junior-Proof Guardian, Verification, Restore & Demo Scripts
│   ├── system-golden-guardian.sh                       # Boot & 60s continuous self-healing guardian daemon
│   ├── verify-golden-state.sh                          # 24-point full-stack verification CLI (`verify-golden-state`)
│   ├── restore-golden-state.sh                         # One-click disaster recovery CLI (`sudo restore-golden-state`)
│   ├── openstack-horizon-guard.sh                      # Minute-by-minute permanent FDB/ARP lock for OpenStack Horizon
│   ├── node-monitor-dashboard-pc1.sh                   # Live 37x100 physical monitor dashboard on compute-pc1 (/dev/tty1)
│   ├── node-monitor-dashboard-pc2.sh                   # Live 37x100 physical monitor dashboard on compute-pc2 (/dev/tty1)
│   ├── video_demo_director.sh                          # Interactive 7-scene terminal walkthrough (`run-video-demo`)
│   └── build_setup_manual_and_ppt.py                   # Automated builder for the 24-slide PPTX & architectural figures
└── docs/                                               # Reports, Manuals, Presentations, KT Guides & 22 High-DPI Figures
    ├── Final_Project_Report_Autonomous_AIOps.pdf       # 67-Page Comprehensive Final Project Report
    ├── Complete_System_Setup_and_Replication_Manual.pdf# Illustrated Step-by-Step Setup & Replication Manual (PDF)
    ├── Complete_System_Setup_and_Replication_Manual.md # Step-by-Step Setup & Replication Manual (Markdown)
    ├── Autonomous_5G_AIOps_Complete_Presentation.pptx  # 24-Slide Widescreen Executive & Technical PowerPoint Deck
    ├── Autonomous_5G_AIOps_Complete_Presentation.pdf   # 24-Slide Presentation Deck (PDF Export)
    ├── Video_Walkthrough_and_Narration_Script.md       # 12-Minute Timestamped Video Walkthrough & Narration Script
    ├── JUNIOR_KNOWLEDGE_TRANSFER_AND_SAFETY_GUIDE.md   # Junior Operator Safety Rules & Instant Rollback Guide
    └── figures/                                        # 22 Publication-Grade 300-DPI Architectural & Results Figures
```

---

## 3. Quick-Start Operational & Verification Commands

Four system-wide CLI utilities are installed in `/usr/local/bin/` so anyone can inspect, demonstrate, or recover the setup with a single command:

```bash
# 1. Run the 24-Point Full-Stack Golden State Health Verification Scorecard
verify-golden-state

# 2. Inspect the Live 6-Plane 368-Parameter Dataset Warehouse & 16.77 TB Storage Pool
dataset-status

# 3. Launch the Interactive 7-Scene Live Video Walkthrough Director (Press [ENTER] per scene)
run-video-demo

# 4. One-Click Disaster Recovery (Restores code, configs, bridges, K8s & services from /data_16tb/GOLDEN_STATE_VAULT)
sudo restore-golden-state
```

---

## 4. Mathematical Formulation & 5-Tier XIE Closed-Loop Architecture

![5-Tier XIE Autonomous Flowchart](docs/figures/fig_4_2_agent_flowchart.png)

### Tier 1: Multi-Modal Anomaly Detection (Rolling Z-Score + 100-Tree Random Forest)
At every sampling instant $t$ ($\Delta t = 5.0\text{ s}$), the system collects the state vector $\mathbf{x}_t \in \mathbb{R}^{368}$. For fast statistical screening over a sliding window $W = 20$, the rolling Z-score for metric $i$ is:

$$z_t^{(i)} = \frac{x_t^{(i)} - \mu_t^{(i)}}{\sigma_t^{(i)} + \epsilon}, \quad \mu_t^{(i)} = \frac{1}{W}\sum_{k=0}^{W-1} x_{t-k}^{(i)}, \quad \epsilon = 10^{-6}$$

Simultaneously, a 100-tree Random Forest ensemble evaluates the posterior fault class distribution across $\mathcal{C} = \{\text{nominal}, \text{compute\_cpu\_exhaustion}, \text{k8s\_container\_crash}, \text{ovn\_sdn\_latency\_loss}, \text{rf\_path\_loss\_attenuation}\}$:

$$P(y = c \mid \mathbf{x}_t) = \frac{1}{B} \sum_{b=1}^{B} P_b(y = c \mid \mathbf{x}_t), \quad B = 100$$

achieving **$99.97\%$ classification accuracy**.

### Tier 2: ChromaDB HNSW Episodic Vector Memory (Sub-100ms Zero-Shot Recovery)
When an anomaly is flagged, the normalized symptom vector $\mathbf{e}_t$ is queried against `14,993+` historical incident episodes indexed in ChromaDB's Hierarchical Navigable Small World (HNSW) graph:

$$\text{sim}(\mathbf{e}_t, \mathbf{e}_k) = \frac{\mathbf{e}_t \cdot \mathbf{e}_k}{\|\mathbf{e}_t\|_2 \, \|\mathbf{e}_k\|_2} \ge \tau_{\text{sim}} \quad (\tau_{\text{sim}} = 0.92)$$

If a verified match exceeds $\tau_{\text{sim}}$, XIE bypasses heavy causal graph inference and dispatches the proven historical remediation in **$< 100\text{ ms}$** (mean top-1 similarity $= 0.9964$).

### Tier 3: Lag-2 VAR(2) Granger Causal Discovery & Reversed-DAG Personalized PageRank ($\boldsymbol{\pi}$)
For novel or cascading multi-layer alarm storms, XIE fits a lag-$P$ Vector Autoregressive model ($P=2$):

$$\mathbf{x}_t = \mathbf{c} + \sum_{p=1}^{P} A^{(p)} \mathbf{x}_{t-p} + \boldsymbol{\varepsilon}_t$$

Directed causal edge weights $W_{ij}$ ($i \to j$) are derived via the Granger causality $F$-statistic comparing the unrestricted model against the restricted model omitting lagged terms of metric $i$.

![Learned Cross-Layer Causal DAG](docs/figures/fig_4_5_causal_dag.png)

Because causal effects propagate forward from **Root Cause $\to$ Downstream Symptoms**, a standard random walk would accumulate at leaf symptoms. XIE **reverses the causal adjacency matrix** ($W_{\text{rev}} = W^{\top}$) so probability mass flows **upstream from noisy symptoms back to the physical root cause**, solving Personalized PageRank with damping factor $\alpha = 0.85$:

$$\boldsymbol{\pi} = (1 - \alpha)\mathbf{v} + \alpha P_{\text{rev}}^{\top}\boldsymbol{\pi}, \quad v_i = \frac{|z_t^{(i)}|}{\sum_{j} |z_t^{(j)}|}$$

The subsystem maximizing $\pi_i^* = \arg\max_i \pi_i$ is mathematically isolated as the true root cause (**$98.33\%$ accuracy**).

### Tier 4 & Tier 5: 4-Domain FastMCP Closed-Loop Actuation & Qwen3-14B Post-Mortems
Remediation is executed exclusively through deterministic, JSON-Schema-validated Model Context Protocol (FastMCP) tools with a 45-second per-domain cooldown guard, while Ollama `qwen3:14b` (`10.0.0.21:11434`) asynchronously writes structured Markdown post-mortem reports.

---

## 5. Experimental Validation & Quantified Results

| Metric / Fault Domain | Manual NOC Baseline | Legacy Rule-v0 | Spatial-Only PageRank | **Proposed XIE Core v1.0** | Improvement vs. Manual |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Overall Mean MTTR** | $1140.0\text{ s}$ ($19\text{ min}$) | $14.20\text{ s}$ | $4.85\text{ s}$ | **$0.354\text{ s}$** | **$99.97\%$ Faster** |
| **K8s / 5G Core Pod Crash MTTR** | $900.0\text{ s}$ | $11.40\text{ s}$ | $3.20\text{ s}$ | **$0.091\text{ s}$** | **$99.99\%$ Faster** |
| **Compute CPU Exhaustion MTTR** | $1080.0\text{ s}$ | $13.80\text{ s}$ | $4.50\text{ s}$ | **$0.371\text{ s}$** | **$99.97\%$ Faster** |
| **OVN Geneve SDN Loss MTTR** | $1320.0\text{ s}$ | $16.50\text{ s}$ | $5.80\text{ s}$ | **$0.382\text{ s}$** | **$99.97\%$ Faster** |
| **5G USRP RF Attenuation MTTR** | $1260.0\text{ s}$ | $15.10\text{ s}$ | $5.90\text{ s}$ | **$0.435\text{ s}$** | **$99.97\%$ Faster** |
| **Overall RCA Accuracy (120 Trials)** | N/A | $51.67\%$ | $74.17\%$ | **$98.33\%$** | **$+46.66\%$ vs. Rule-v0** |
| **Cascading Storm RCA Accuracy** | N/A | $42.50\%$ | $68.33\%$ | **$96.67\%$** | **$+54.17\%$ vs. Rule-v0** |

| Sub-Second MTTR Comparison | Cascading Alarm Storm RCA Accuracy |
| :---: | :---: |
| ![MTTR Comparison](docs/figures/fig_6_1_mttr_comparison.png) | ![Cascading Accuracy](docs/figures/fig_6_4_cascading_accuracy.png) |

---

## 6. Continuous 6-Plane Multi-Dimensional Dataset Warehouse (`16.77 TB` RAID Pool)

![6-Plane Dataset Warehouse Architecture](docs/figures/fig_dataset_warehouse_architecture.png)

Managed by `omni-crosslayer-harvester.service`, the data factory captures **368 cross-layer parameters** and **every log, alert, and event** across all 6 planes every 5.0 seconds onto the `16.77 TB` PERC H755 RAID pool (`/data/cross_layer_dataset` + `/data_16tb/cross_layer_dataset_vault`):

- **Plane 0 (Metadata & Ground-Truth Labels)**: `8` parameters (`timestamp`, `epoch_ms`, `sequence_id`, `fault_label`, `fault_class_id`, `anomaly_severity`, `is_anomalous`, `collection_latency_ms`)
- **Plane 1 (Bare-Metal Hardware, NUMA, Kernel, Disk & Physical NICs)**: `78` parameters across Dell R760xs, `compute-pc1`, and `compute-pc2`
- **Plane 2 (OpenStack 2023.1 23 Juju LXD Containers, KVM `virsh domstats` & OVS/OVN Geneve BFD)**: `117` parameters
- **Plane 3 (Magnum K8s 3 CoreOS Nodes, 13 Open5GS 5G SA Core NFs & 12 Online Boutique Pods)**: `74` parameters
- **Plane 4 (Physical 5G SDR RAN — 4x Ettus USRP B210, 8 RF Chains, Band n78 PHY/MAC & Mist Wi-Fi)**: `34` parameters
- **Plane 5 (Wazuh SIEM v4.8.0 Security Alerts, Agents `000`–`004` & MITRE ATT&CK Counters)**: `22` parameters
- **Plane 6 (Dual Intel UHD 770 GPUs + Xeon AMX GFLOPS & XIE Z-Scores, RF Probs, VAR(2), PPR $\boldsymbol{\pi}$, ChromaDB)**: `35` parameters

See [`dataset_schema_and_samples/FEATURE_CATALOG.md`](dataset_schema_and_samples/FEATURE_CATALOG.md) for the complete 368-parameter dictionary and [`dataset_schema_and_samples/sample_100_cross_layer_metrics.csv`](dataset_schema_and_samples/sample_100_cross_layer_metrics.csv) for a 100-row sample table.

---

## 7. Web Dashboards, Endpoints & Credentials Reference

| Service / Dashboard | Endpoint URL | Credentials / Notes |
| :--- | :--- | :--- |
| **OpenStack Horizon Cloud Dashboard** | `http://10.0.0.10/horizon/auth/login/` | User: `admin` \| Pass: `ahseiweeNgaik8uX` \| Domain: `admin_domain` |
| **Wazuh SIEM v4.8.0 Security Dashboard** | `https://10.0.0.10:443` | User: `admin` \| Pass: `6WEAGMhS+S8uyZxsofy+rBl6N1hkf.FI` |
| **Grafana Enterprise Observability UI** | `http://10.0.0.10:3000` | Live 6-Plane Telemetry & AIOps Dashboards |
| **Prometheus Time-Series Server** | `http://10.0.0.10:9090` | Targets: `:9105` (Multi-Domain Exporter) & `:9475` (OVS Exporter) |
| **Google Online Boutique Storefront** | `http://10.0.0.10:8081` / `http://192.168.100.131:32375` | 12-Microservice Cloud-Native Application |
| **Open5GS 5G SA Subscriber WebUI** | `http://10.0.0.10:8082` | 3GPP 5G Core Subscriber Management |
| **FastMCP JSON-RPC HTTP Servers** | `http://10.0.0.10:8101` .. `:8104` | `:8101` DCOps \| `:8102` DevOps \| `:8103` SecOps \| `:8104` AIOps |
| **Ollama Qwen3-14B LLM Server** | `http://10.0.0.21:11434` | Asynchronous Incident Post-Mortem Synthesis |

---

## 8. Documentation, Reports & Knowledge Transfer Artifacts

- **67-Page Final Project Report (PDF)**: [`docs/Final_Project_Report_Autonomous_AIOps.pdf`](docs/Final_Project_Report_Autonomous_AIOps.pdf)
- **Step-by-Step Setup & Replication Manual (PDF & Markdown)**:
  - [`docs/Complete_System_Setup_and_Replication_Manual.pdf`](docs/Complete_System_Setup_and_Replication_Manual.pdf)
  - [`docs/Complete_System_Setup_and_Replication_Manual.md`](docs/Complete_System_Setup_and_Replication_Manual.md)
- **24-Slide Widescreen PowerPoint Deck (`.pptx` & `.pdf`)**:
  - [`docs/Autonomous_5G_AIOps_Complete_Presentation.pptx`](docs/Autonomous_5G_AIOps_Complete_Presentation.pptx)
  - [`docs/Autonomous_5G_AIOps_Complete_Presentation.pdf`](docs/Autonomous_5G_AIOps_Complete_Presentation.pdf)
- **12-Minute Video Walkthrough & Word-for-Word Narration Script**: [`docs/Video_Walkthrough_and_Narration_Script.md`](docs/Video_Walkthrough_and_Narration_Script.md)
- **Junior Knowledge Transfer & Disaster Recovery Guide**: [`docs/JUNIOR_KNOWLEDGE_TRANSFER_AND_SAFETY_GUIDE.md`](docs/JUNIOR_KNOWLEDGE_TRANSFER_AND_SAFETY_GUIDE.md)

