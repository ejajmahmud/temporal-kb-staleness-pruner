"""Core KB Staleness Pruner implementation."""
import time
import math
from typing import Dict, List, Optional

class KnowledgeFact:
    def __init__(self, fact_id: str, topic: str, content: str, timestamp: float, superseded_by: Optional[str] = None):
        self.fact_id = fact_id
        self.topic = topic
        self.content = content
        self.timestamp = timestamp
        self.superseded_by = superseded_by

class KBStalenessPruner:
    def __init__(self, half_life_seconds: float = 86400.0, retention_threshold: float = 0.25):
        self.half_life = half_life_seconds
        self.threshold = retention_threshold
        self.facts: Dict[str, KnowledgeFact] = {}

    def add_fact(self, fact_id: str, topic: str, content: str, timestamp: Optional[float] = None) -> KnowledgeFact:
        ts = timestamp if timestamp is not None else time.time()
        fact = KnowledgeFact(fact_id, topic, content, ts)
        self.facts[fact_id] = fact
        return fact

    def supersede(self, old_fact_id: str, new_fact_id: str):
        if old_fact_id in self.facts:
            self.facts[old_fact_id].superseded_by = new_fact_id

    def prune(self, current_time: Optional[float] = None) -> List[str]:
        now = current_time if current_time is not None else time.time()
        pruned_ids = []

        for fid, f in list(self.facts.items()):
            if f.superseded_by:
                pruned_ids.append(fid)
                del self.facts[fid]
                continue

            age = max(0.0, now - f.timestamp)
            weight = math.pow(0.5, age / self.half_life)
            if weight < self.threshold:
                pruned_ids.append(fid)
                del self.facts[fid]

        return pruned_ids
