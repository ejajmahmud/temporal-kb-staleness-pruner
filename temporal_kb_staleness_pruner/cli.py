"""CLI for KB Staleness Pruner."""
import argparse
from .core import KBStalenessPruner

def main():
    parser = argparse.ArgumentParser(description="Temporal KB Staleness Pruner CLI")
    parser.add_argument("--demo", action="store_true", help="Run staleness prune demo")
    args = parser.parse_args()

    pruner = KBStalenessPruner(half_life_seconds=10.0, retention_threshold=0.3)
    pruner.add_fact("f1", "api", "Use API v1", timestamp=100.0)
    pruner.add_fact("f2", "api", "Use API v2", timestamp=115.0)
    pruner.supersede("f1", "f2")

    pruned = pruner.prune(current_time=120.0)
    print("Pruned fact IDs:", pruned)
    print("Remaining active facts:", list(pruner.facts.keys()))

if __name__ == "__main__":
    main()
