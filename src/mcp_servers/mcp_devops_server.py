#!/usr/bin/env python3
"""
MCP-DevOps Server - Cloud-Native Container & Microservices Operations Endpoint
Manages Magnum Kubernetes v1.23 cluster, Open5GS core network pods, and Online Boutique microservices.
Exposes tools: get_k8s_cluster_health, get_pods_by_namespace, get_microservices_status, restart_deployment, scale_deployment
"""
import sys
import os
import json
import logging
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp-devops")

KUBECONFIG = os.environ.get("KUBECONFIG", "/home/hpe/k8s-5g/config")

class DevOpsManager:
    def __init__(self, kubeconfig=KUBECONFIG):
        self.kubeconfig = kubeconfig

    def _run_kubectl(self, args: list, timeout=10) -> tuple:
        cmd = ["kubectl", f"--kubeconfig={self.kubeconfig}"] + args
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return res.returncode, res.stdout, res.stderr
        except Exception as e:
            return -1, "", str(e)

    def get_k8s_cluster_health(self) -> dict:
        """Inspect Kubernetes cluster nodes and conditions"""
        health = {
            "cluster": "k8s-5g (Magnum Fedora CoreOS)",
            "nodes": [],
            "overall_status": "UNKNOWN"
        }
        rc, out, err = self._run_kubectl(["get", "nodes", "-o", "json"])
        if rc == 0:
            try:
                data = json.loads(out)
                ready_count = 0
                for item in data.get("items", []):
                    name = item.get("metadata", {}).get("name")
                    status = item.get("status", {})
                    conditions = status.get("conditions", [])
                    is_ready = any(c.get("type") == "Ready" and c.get("status") == "True" for c in conditions)
                    if is_ready:
                        ready_count += 1
                    
                    addresses = {a.get("type"): a.get("address") for a in status.get("addresses", [])}
                    node_info = status.get("nodeInfo", {})
                    health["nodes"].append({
                        "name": name,
                        "ready": is_ready,
                        "ip": addresses.get("InternalIP"),
                        "kubelet_version": node_info.get("kubeletVersion"),
                        "os_image": node_info.get("osImage")
                    })
                health["overall_status"] = "HEALTHY" if (ready_count == len(data.get("items", [])) and ready_count > 0) else "DEGRADED"
                health["ready_nodes"] = ready_count
                health["total_nodes"] = len(data.get("items", []))
            except Exception as e:
                health["error"] = str(e)
        else:
            health["error"] = err or "Failed to query nodes"
            health["overall_status"] = "UNREACHABLE"

        return health

    def get_pods_by_namespace(self, namespace: str = "open5gs") -> dict:
        """Get pods and container status in a given namespace"""
        result = {
            "namespace": namespace,
            "total_pods": 0,
            "running_pods": 0,
            "pods": []
        }
        rc, out, err = self._run_kubectl(["get", "pods", "-n", namespace, "-o", "json"])
        if rc == 0:
            try:
                data = json.loads(out)
                items = data.get("items", [])
                result["total_pods"] = len(items)
                for pod in items:
                    meta = pod.get("metadata", {})
                    pname = meta.get("name")
                    status = pod.get("status", {})
                    phase = status.get("phase")
                    c_statuses = status.get("containerStatuses", [])
                    restarts = sum(c.get("restartCount", 0) for c in c_statuses)
                    all_ready = all(c.get("ready", False) for c in c_statuses) if c_statuses else False
                    if phase == "Running" and all_ready:
                        result["running_pods"] += 1

                    result["pods"].append({
                        "name": pname,
                        "phase": phase,
                        "ready": all_ready,
                        "restarts": restarts,
                        "pod_ip": status.get("podIP"),
                        "host_ip": status.get("hostIP")
                    })
            except Exception as e:
                result["error"] = str(e)
        else:
            result["error"] = err
        return result

    def get_microservices_status(self) -> dict:
        """Inspect the 11 Google Online Boutique microservice deployments"""
        return self.get_pods_by_namespace("microservices")

    def restart_deployment(self, deployment_name: str, namespace: str = "open5gs") -> dict:
        """Execute a rolling restart of a Kubernetes deployment"""
        logger.info(f"Restarting deployment {deployment_name} in namespace {namespace}...")
        rc, out, err = self._run_kubectl(["rollout", "restart", f"deployment/{deployment_name}", "-n", namespace])
        success = (rc == 0)
        return {
            "action": "rollout_restart",
            "deployment": deployment_name,
            "namespace": namespace,
            "success": success,
            "output": out.strip() if success else err.strip()
        }

    def scale_deployment(self, deployment_name: str, replicas: int, namespace: str = "microservices") -> dict:
        """Scale replica count for a deployment"""
        logger.info(f"Scaling deployment {deployment_name} in namespace {namespace} to {replicas} replicas...")
        rc, out, err = self._run_kubectl(["scale", f"deployment/{deployment_name}", f"--replicas={replicas}", "-n", namespace])
        success = (rc == 0)
        return {
            "action": "scale_deployment",
            "deployment": deployment_name,
            "namespace": namespace,
            "replicas": replicas,
            "success": success,
            "output": out.strip() if success else err.strip()
        }

def run_test():
    mgr = DevOpsManager()
    print("=" * 60)
    print("MCP-DevOps Self-Test & Diagnostic Audit")
    print("=" * 60)

    print("\n[*] K8s Cluster Health:")
    cluster = mgr.get_k8s_cluster_health()
    print(f"Overall Status: {cluster.get('overall_status')} ({cluster.get('ready_nodes')}/{cluster.get('total_nodes')} Ready)")
    for n in cluster.get("nodes", []):
        print(f"  - {n['name']} [{n['ip']}] Ready: {n['ready']} ({n['os_image']})")

    print("\n[*] Open5GS Core Network Pods:")
    open5gs = mgr.get_pods_by_namespace("open5gs")
    print(f"Running: {open5gs['running_pods']}/{open5gs['total_pods']} Pods")
    for p in open5gs.get("pods", []):
        print(f"  - {p['name']} [{p['phase']}] Ready: {p['ready']}, Restarts: {p['restarts']}")

    print("\n[*] Google Online Boutique Microservices:")
    ms = mgr.get_microservices_status()
    print(f"Running: {ms['running_pods']}/{ms['total_pods']} Pods")
    for p in ms.get("pods", []):
        print(f"  - {p['name']} [{p['phase']}] Ready: {p['ready']}")

def run_stdio():
    mgr = DevOpsManager()
    logger.info("mcp-devops JSON-RPC server listening on stdio...")
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            params = req.get("params", {})

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {"name": "get_k8s_cluster_health", "description": "Get Kubernetes node statuses, versions, and readiness"},
                            {"name": "get_pods_by_namespace", "description": "Get pod phases, readiness, and restart counts in any namespace"},
                            {"name": "get_microservices_status", "description": "Get status of Google Online Boutique 11-tier microservice pods"},
                            {"name": "restart_deployment", "description": "Perform rolling restart of a deployment in open5gs or microservices"},
                            {"name": "scale_deployment", "description": "Scale replica count of a deployment"}
                        ]
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})
                if tool_name == "get_k8s_cluster_health":
                    res = mgr.get_k8s_cluster_health()
                elif tool_name == "get_pods_by_namespace":
                    res = mgr.get_pods_by_namespace(args.get("namespace", "open5gs"))
                elif tool_name == "get_microservices_status":
                    res = mgr.get_microservices_status()
                elif tool_name == "restart_deployment":
                    res = mgr.restart_deployment(args.get("deployment_name"), args.get("namespace", "open5gs"))
                elif tool_name == "scale_deployment":
                    res = mgr.scale_deployment(args.get("deployment_name"), args.get("replicas", 1), args.get("namespace", "microservices"))
                else:
                    res = {"error": f"Unknown tool {tool_name}"}
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": req.get("id") if 'req' in locals() else None, "error": {"code": -32603, "message": str(e)}}
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        run_stdio()
    elif len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_test()
    else:
        if sys.stdin.isatty():
            run_test()
        else:
            run_stdio()

