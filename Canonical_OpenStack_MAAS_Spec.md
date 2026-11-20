# Canonical OpenStack & MAAS Deployment Guide: Machine-to-Machine Operational Spec
**Target System:** Dell PowerEdge R760xs (Ubuntu 22.04 LTS Desktop)  
**Agent Role:** Autonomous Cloud Orchestration Agent (Antigravity on Dell Server)  
**Hardware Topology:**
- Node 1: Dell PowerEdge R760xs (512GB RAM, 20TB Storage pool mounted at `/data`, 480GB OS RAID1)
  - `eno8303` (Onboard 1GbE): Management / Internet Uplink (`10.0.0.10/24`)
  - `enp171s0f0np0` (OCP/PCIe 10GbE): Isolated MAAS Cluster Data Plane (`10.10.10.2/24`)
- Node 2: Compute PC 1 (64GB RAM, 2TB Disk, UEFI PXE Boot configured on built-in NIC)
- Node 3: Compute PC 2 (64GB RAM, 2TB Disk, UEFI PXE Boot configured on built-in NIC)
- Switching: Juniper EX2300-C Top-of-Rack Switch
  - Ports `ge-0/0/1` to `ge-0/0/3` locked into `Isolated-Data-VLAN10` (Tag 10)

---

## 1. Architectural Mission & Strict Constraints
1. **Zero-DHCP on Management (VLAN 20):**
   - Under NO circumstances may any DHCP service run or broadcast on `eno8303` or the college uplink.
2. **MAAS DHCP Encapsulation (VLAN 10):**
   - Canonical MAAS must bind its internal DHCP (`dnsmasq`) **STRICTLY and EXCLUSIVELY** to `enp171s0f0np0` (`10.10.10.0/24`).
3. **Execution Stack:**
   - Layer 0: Metal-as-a-Service (MAAS 3.4) on bare metal Dell R760xs.
   - Layer 1: Juju 3.x controller bootstrapped on MAAS.
   - Layer 2: Charmed OpenStack (Antelope / 2023.1 release) deployed across the 3 physical machines.
   - Layer 3: OpenStack Magnum (Kubernetes Cluster API) providing container orchestration.

---

## 2. Phase 1: Canonical MAAS Installation & Configuration

### 2.1 Package Installation
Run on the Dell Server:
```bash
sudo snap install maas --channel=3.4/stable
sudo snap install maas-test-db
```

### 2.2 Database & Region/Rack Initialization
Initialize MAAS pointing strictly to the local database and the 10G IP:
```bash
sudo maas init region+rack \
  --maas-url http://10.10.10.2:5240/MAAS \
  --database-uri maas-test-db:///
```

### 2.3 Create Admin Account
```bash
sudo maas createadmin \
  --username admin \
  --password admin \
  --email admin@local.lab
```

### 2.4 API Login
Log in to the local MAAS CLI:
```bash
API_KEY=$(sudo maas apikey --username admin)
maas login admin http://10.10.10.2:5240/MAAS/api/2.0/ "$API_KEY"
```

### 2.5 Configure Subnet & Isolated DHCP
Configure MAAS so that DHCP is strictly enabled on the 10G subnet (`10.10.10.0/24`) and explicitly disabled on all other interfaces:
```bash
# 1. Set upstream DNS (prevents external DNS resolution loops)
maas admin maas set-config name=upstream_dns value="8.8.8.8 1.1.1.1"

# 2. Retrieve fabric and VLAN IDs for the 10.10.10.0/24 network
FABRIC_ID=$(maas admin subnets read | jq -r '.[] | select(.cidr=="10.10.10.0/24") | .vlan.fabric_id')
VLAN_TAG=$(maas admin subnets read | jq -r '.[] | select(.cidr=="10.10.10.0/24") | .vlan.vid')
SUBNET_ID=$(maas admin subnets read | jq -r '.[] | select(.cidr=="10.10.10.0/24") | .id')

# 3. Configure Subnet Gateway and Dynamic IP Range
maas admin subnet update $SUBNET_ID gateway_ip="10.10.10.2" dns_servers="10.10.10.2"

# 4. Enable DHCP strictly on VLAN 10 (Dynamic range 10.10.10.100 - 10.10.10.200)
maas admin ipranges create type=dynamic \
  start_ip=10.10.10.100 end_ip=10.10.10.200 \
  subnet=$SUBNET_ID

maas admin vlan update $FABRIC_ID $VLAN_TAG dhcp_on=true primary_rack=$(maas admin rack-controllers read | jq -r '.[0].system_id')
```

### 2.6 Sync Ubuntu 22.04 LTS Boot Images
MAAS needs the Ubuntu 22.04 LTS boot stream to serve over PXE:
```bash
maas admin boot-source-selections create 1 \
  os="ubuntu" release="jammy" arches="amd64" subarches="*" labels="*"

# Trigger boot image import
maas admin boot-resources import
```
*Monitor image download progress via CLI:*
```bash
maas admin boot-resources is-importing
```
Wait until `false` is returned and `maas admin boot-resources read` shows `jammy` status as `synced`.

---

## 3. Phase 2: Compute Node Enlistment & Commissioning

### 3.1 Powering On Nodes
Once the boot images are synced:
1. Power on **Compute PC 1** and **Compute PC 2**.
2. Both machines will PXE-boot into RAM via `enp171s0f0np0` / VLAN 10.
3. MAAS will automatically enlist them. They will appear with status `New`.

### 3.2 Automated Commissioning
Run via MAAS CLI:
```bash
# Get system IDs of newly discovered machines
NEW_SYSTEMS=$(maas admin machines read | jq -r '.[] | select(.status_name=="New") | .system_id')

for SYS_ID in $NEW_SYSTEMS; do
  echo "Commissioning machine: $SYS_ID"
  maas admin machine commission $SYS_ID
done
```
Wait for status to transition: `New` -> `Commissioning` -> `Ready`.

### 3.3 Static IP & Tag Assignment
Tag nodes for OpenStack roles:
```bash
# Tag compute nodes
maas admin tags create name=compute comment="OpenStack Nova Compute Nodes"

MACHINES=($(maas admin machines read | jq -r '.[] | select(.status_name=="Ready") | .system_id'))

# Machine 1 -> Compute PC 1
maas admin tag update-nodes compute add="${MACHINES[0]}"
maas admin machine update "${MACHINES[0]}" hostname="compute-pc1"

# Machine 2 -> Compute PC 2
maas admin tag update-nodes compute add="${MACHINES[1]}"
maas admin machine update "${MACHINES[1]}" hostname="compute-pc2"
```

---

## 4. Phase 3: Juju Controller Bootstrap & OpenStack Deployment

### 4.1 Install Juju 3.x
```bash
sudo snap install juju --channel=3.4/stable --classic
```

### 4.2 Add MAAS Cloud to Juju
```bash
# Add MAAS cloud definition
juju add-cloud --client maas-cloud -f - <<EOF
clouds:
  maas-cloud:
    type: maas
    auth-types: [oauth1]
    endpoint: http://10.10.10.2:5240/MAAS
EOF

# Add MAAS Credentials
juju add-credential --client maas-cloud -f - <<EOF
credentials:
  maas-cloud:
    admin:
      auth-type: oauth1
      maas-oauth: $API_KEY
EOF
```

### 4.3 Bootstrap Juju Controller onto Dell Server
```bash
juju bootstrap maas-cloud maas-controller \
  --to localhost \
  --config default-series=jammy
```

### 4.4 Deploy Charmed OpenStack (Antelope / 2023.1)
Create OpenStack deployment model:
```bash
juju add-model openstack
```

Deploy core OpenStack services via Juju bundles:
- **Keystone:** Identity service
- **Nova:** Compute orchestration
- **Neutron:** Software Defined Networking (Configured with `--no-dhcp` / Config Drive)
- **Glance:** Image registry
- **Cinder:** Block storage (Backed by `/data` LVM/Ceph)
- **Octavia:** Load Balancer as a Service
- **Magnum:** Kubernetes Container Infrastructure Management
- **Dashboard:** Horizon Web UI

Deploy command:
```bash
juju deploy openstack-base \
  --constraints "tags=compute" \
  --series jammy
```

Monitor cluster convergence:
```bash
juju status --watch 5s
```

---

## 5. Verification & Hand-off Matrix
The deployment is complete when:
1. `juju status` reports all charms in `active/idle` state.
2. `source admin-openrc.sh && openstack hypervisor list` shows:
   - `compute-pc1` (State: UP, Status: ENABLED)
   - `compute-pc2` (State: UP, Status: ENABLED)
3. OpenStack Horizon dashboard is accessible at `http://10.0.0.10/horizon`.
4. Kubernetes cluster can be provisioned via `openstack coe cluster create`.

