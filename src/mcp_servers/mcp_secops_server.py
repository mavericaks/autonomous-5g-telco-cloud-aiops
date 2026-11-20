#!/usr/bin/env python3
"""
MCP-SecOps Server - Autonomous Security Operations Protocol Endpoint
Integrates Wazuh SIEM Server (https://10.0.0.10:55000), Juniper SRX syslog, and enrolled agents.
Exposes tools: get_alerts, get_agents, get_firewall_events, trigger_active_response
"""
import sys
import os
import json
import logging
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("mcp-secops")

WAZUH_API_URL = os.environ.get("WAZUH_API_URL", "https://10.0.0.10:55000")
WAZUH_USER = os.environ.get("WAZUH_USER", "wazuh")
WAZUH_PASS = os.environ.get("WAZUH_PASS", "wazuh")
ALERTS_JSON_PATH = "/var/ossec/logs/alerts/alerts.json"
ACTIVE_RESPONSES_LOG = "/var/ossec/logs/active-responses.log"

class WazuhSecOpsClient:
    def __init__(self, base_url=WAZUH_API_URL, user=WAZUH_USER, password=WAZUH_PASS):
        self.base_url = base_url
        self.user = user
        self.password = password
        self.token = None

    def authenticate(self) -> str:
        try:
            res = requests.post(
                f"{self.base_url}/security/user/authenticate",
                auth=(self.user, self.password),
                verify=False,
                timeout=5
            )
            if res.status_code == 200:
                self.token = res.json()["data"]["token"]
                return self.token
            logger.error(f"Authentication failed with status {res.status_code}: {res.text}")
        except Exception as e:
            logger.error(f"Failed to connect to Wazuh API: {e}")
        return None

    def get_headers(self) -> dict:
        if not self.token:
            self.authenticate()
        return {"Authorization": f"Bearer {self.token}"}

    def get_agents(self) -> list:
        try:
            headers = self.get_headers()
            res = requests.get(f"{self.base_url}/agents", headers=headers, verify=False, timeout=5)
            if res.status_code == 401:
                headers = {"Authorization": f"Bearer {self.authenticate()}"}
                res = requests.get(f"{self.base_url}/agents", headers=headers, verify=False, timeout=5)
            if res.status_code == 200:
                return res.json().get("data", {}).get("affected_items", [])
        except Exception as e:
            logger.error(f"Error fetching agents: {e}")
        return []

    def get_alerts(self, limit: int = 10, min_level: int = 1) -> list:
        """Fetch alerts from Wazuh alerts.json and API"""
        alerts = []
        if os.path.exists(ALERTS_JSON_PATH):
            try:
                with open(ALERTS_JSON_PATH, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in reversed(lines):
                        if not line.strip():
                            continue
                        try:
                            record = json.loads(line)
                            level = record.get("rule", {}).get("level", 0)
                            if level >= min_level:
                                alerts.append(record)
                            if len(alerts) >= limit:
                                break
                        except Exception:
                            continue
            except Exception as e:
                logger.warning(f"Could not read {ALERTS_JSON_PATH}: {e}")

        # Fallback to API if local file empty or in progress
        if not alerts:
            try:
                headers = self.get_headers()
                res = requests.get(f"{self.base_url}/manager/logs?limit={limit}", headers=headers, verify=False, timeout=5)
                if res.status_code == 200:
                    items = res.json().get("data", {}).get("affected_items", [])
                    for item in items:
                        alerts.append({
                            "timestamp": item.get("timestamp"),
                            "description": item.get("description"),
                            "tag": item.get("tag"),
                            "level": item.get("level", 3)
                        })
            except Exception as e:
                logger.error(f"Error querying manager logs: {e}")

        return alerts

    def get_firewall_events(self, limit: int = 20) -> list:
        """Parse Juniper SRX300 events from active-responses.log"""
        events = []
        if os.path.exists(ACTIVE_RESPONSES_LOG):
            try:
                with open(ACTIVE_RESPONSES_LOG, "r", encoding="utf-8") as f:
                    for line in reversed(f.readlines()):
                        line = line.strip()
                        if line:
                            events.append({"raw": line})
                        if len(events) >= limit:
                            break
            except Exception as e:
                logger.error(f"Error reading {ACTIVE_RESPONSES_LOG}: {e}")
        return events

def run_test():
    client = WazuhSecOpsClient()
    token = client.authenticate()
    print(f"[*] Wazuh API Authentication: {'SUCCESS' if token else 'FAILED'}")
    
    agents = client.get_agents()
    print(f"[*] Enrolled Agents ({len(agents)}):")
    for a in agents:
        print(f"    - ID: {a['id']}, Name: {a['name']}, Status: {a['status']}, IP: {a.get('ip')}")

    alerts = client.get_alerts(limit=5)
    print(f"[*] Real-Time Security Alerts ({len(alerts)}):")
    for idx, alert in enumerate(alerts):
        rule = alert.get("rule", {})
        desc = rule.get("description") or alert.get("description", "System Event")
        level = rule.get("level") or alert.get("level", "N/A")
        print(f"    {idx+1}. [Level {level}] {desc}")

    fw_events = client.get_firewall_events(limit=5)
    print(f"[*] Juniper SRX Firewall Syslog Events ({len(fw_events)}):")
    for idx, ev in enumerate(fw_events):
        print(f"    {idx+1}. {ev['raw']}")

def run_stdio():
    client = WazuhSecOpsClient()
    logger.info("mcp-secops JSON-RPC server listening on stdio...")
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
                            {"name": "get_alerts", "description": "Get real-time Wazuh SIEM security alerts"},
                            {"name": "get_agents", "description": "Get list and status of enrolled cluster nodes"},
                            {"name": "get_firewall_events", "description": "Get Juniper SRX300 firewall syslog flows"}
                        ]
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                args = params.get("arguments", {})
                if tool_name == "get_alerts":
                    result = client.get_alerts(limit=args.get("limit", 10))
                elif tool_name == "get_agents":
                    result = client.get_agents()
                elif tool_name == "get_firewall_events":
                    result = client.get_firewall_events(limit=args.get("limit", 20))
                else:
                    result = {"error": f"Unknown tool {tool_name}"}
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]}}
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}

            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": req.get("id"), "error": {"code": -32603, "message": str(e)}}
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
