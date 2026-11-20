#!/usr/bin/env python3
"""
Experiential Intelligence Engine (XIE Core) - ChromaDB Episodic Memory
Stores historical incident signatures, root causes, and verified remediations.
Enables Zero-Shot instant repair via vector cosine similarity retrieval (>= 0.85).
"""
import os
import json
import logging
import uuid
import chromadb
from typing import Dict, List, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("xie.episodic_memory")

CHROMA_PATH = "/home/hpe/xie/chroma_db"
COLLECTION_NAME = "incident_episodic_memory"

class IncidentEpisodicMemory:
    def __init__(self, persist_dir: str = CHROMA_PATH):
        self.persist_dir = persist_dir
        os.makedirs(self.persist_dir, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.persist_dir)
        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info(f"Connected to ChromaDB Episodic Memory at {self.persist_dir}. Incidents stored: {self.collection.count()}")

    def record_incident(self, 
                        incident_id: str,
                        symptom_text: str,
                        metrics_summary: Dict[str, float],
                        root_cause: str,
                        fault_domain: str,
                        remediation_action: str,
                        success: bool = True,
                        mttd_sec: float = 0.0,
                        mttr_sec: float = 0.0) -> str:
        """Stores a resolved incident episode into vector memory."""
        doc_id = incident_id or f"inc-{uuid.uuid4().hex[:8]}"
        doc_text = f"Incident: {symptom_text}. Root Cause: {root_cause} in {fault_domain}. Action: {remediation_action}."
        
        metadata = {
            "root_cause": str(root_cause),
            "fault_domain": str(fault_domain),
            "remediation_action": str(remediation_action),
            "success": str(success),
            "mttd_sec": float(mttd_sec),
            "mttr_sec": float(mttr_sec),
            "metrics_json": json.dumps(metrics_summary)
        }

        self.collection.upsert(
            ids=[doc_id],
            documents=[doc_text],
            metadatas=[metadata]
        )
        logger.info(f"Stored incident {doc_id} into ChromaDB episodic memory. Total: {self.collection.count()}")
        return doc_id

    def query_nearest_incident(self, symptom_text: str, similarity_threshold: float = 0.80) -> Optional[Dict[str, Any]]:
        """
        Queries ChromaDB for the closest historical incident episode.
        Returns match if cosine similarity >= similarity_threshold (cosine distance <= 1 - threshold).
        """
        if self.collection.count() == 0:
            return None

        results = self.collection.query(
            query_texts=[symptom_text],
            n_results=1
        )

        if not results or not results["ids"] or not results["ids"][0]:
            return None

        doc_id = results["ids"][0][0]
        distance = results["distances"][0][0] if "distances" in results and results["distances"] else 1.0
        # For cosine space: similarity = 1 - distance
        similarity = 1.0 - float(distance)
        metadata = results["metadatas"][0][0]
        document = results["documents"][0][0]

        logger.info(f"ChromaDB lookup for '{symptom_text[:40]}...' -> Match {doc_id} with similarity {similarity:.3f}")

        if similarity >= similarity_threshold:
            return {
                "match": True,
                "incident_id": doc_id,
                "similarity": round(similarity, 4),
                "root_cause": metadata.get("root_cause"),
                "fault_domain": metadata.get("fault_domain"),
                "recommended_action": metadata.get("remediation_action"),
                "document": document,
                "metadata": metadata
            }

        return {
            "match": False,
            "incident_id": doc_id,
            "similarity": round(similarity, 4),
            "root_cause": metadata.get("root_cause")
        }

def seed_baseline_episodes(memory: IncidentEpisodicMemory):
    """Seed proven historical incidents from prior 5G, SDN, K8s, and CPU testbed runs"""
    if memory.collection.count() > 0:
        return

    episodes = [
        {
            "id": "inc-baseline-001",
            "text": "OVN SDN overlay Geneve tunnel delay 80ms and packet loss 7% on enp1s0",
            "metrics": {"latency_ms": 82.5, "dropped_packets": 35.0},
            "cause": "dropped_packets",
            "domain": "sdn_overlay_network",
            "action": "tc_qdisc_del_reset",
            "mttd": 1.2,
            "mttr": 2.1
        },
        {
            "id": "inc-baseline-002",
            "text": "Kubernetes Open5GS UPF pod crash termination missing healthy pods",
            "metrics": {"healthy_pod_count": 12.0, "pod_restart_count": 1.0},
            "cause": "healthy_pod_count",
            "domain": "k8s_container",
            "action": "k8s_rollout_restart",
            "mttd": 0.8,
            "mttr": 4.5
        },
        {
            "id": "inc-baseline-003",
            "text": "Compute node CPU resource exhaustion 8 cores stress-ng saturation",
            "metrics": {"cpu_load_pct": 98.2, "latency_ms": 45.0},
            "cause": "cpu_load_pct",
            "domain": "compute_resource",
            "action": "throttle_traffic_and_isolate_core",
            "mttd": 1.5,
            "mttr": 3.0
        },
        {
            "id": "inc-baseline-004",
            "text": "Physical RF path loss attenuation USRP B210 PRACH SNR < 5 dB degraded CQI",
            "metrics": {"prach_sinr": -32.0, "cqi": 2.0},
            "cause": "prach_sinr",
            "domain": "rf_physical_layer",
            "action": "recalibrate_rf_attenuation_and_power",
            "mttd": 1.1,
            "mttr": 3.2
        }
    ]

    for ep in episodes:
        memory.record_incident(
            incident_id=ep["id"],
            symptom_text=ep["text"],
            metrics_summary=ep["metrics"],
            root_cause=ep["cause"],
            fault_domain=ep["domain"],
            remediation_action=ep["action"],
            success=True,
            mttd_sec=ep["mttd"],
            mttr_sec=ep["mttr"]
        )
    logger.info(f"Seeded {len(episodes)} baseline episodes into ChromaDB.")

if __name__ == "__main__":
    mem = IncidentEpisodicMemory()
    seed_baseline_episodes(mem)
    
    # Test query
    query_text = "Severe packet drop on enp1s0 Geneve overlay interface"
    print(f"\nQuerying: '{query_text}'")
    match = mem.query_nearest_incident(query_text)
    print("Match Result:", json.dumps(match, indent=2))

