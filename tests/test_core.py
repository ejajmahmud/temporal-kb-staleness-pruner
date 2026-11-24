"""Tests for KBStalenessPruner."""
import unittest
from temporal_kb_staleness_pruner.core import KBStalenessPruner

class TestKBStalenessPruner(unittest.TestCase):
    def test_superseded_and_decay_pruning(self):
        pruner = KBStalenessPruner(half_life_seconds=100.0, retention_threshold=0.2)
        pruner.add_fact("f1", "auth", "Old token format", timestamp=0.0)
        pruner.add_fact("f2", "auth", "New token format", timestamp=1000.0)
        pruner.supersede("f1", "f2")

        pruned = pruner.prune(current_time=1005.0)
        self.assertIn("f1", pruned)
        self.assertIn("f2", pruner.facts)
