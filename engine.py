# engine.py

import time
from collections import defaultdict


class A7DOResearchEngine:
    def __init__(self):
        self.graph = defaultdict(dict)

    # -----------------------------
    # Add relation
    # -----------------------------
    def add_relation(self, relation_obj):
        src, rel, tgt = relation_obj.as_tuple()
        self.graph[src][tgt] = rel

    # -----------------------------
    # Get all nodes
    # -----------------------------
    def nodes(self):
        nodes = set(self.graph.keys())
        for src in self.graph:
            for tgt in self.graph[src]:
                nodes.add(tgt)
        return list(nodes)

    # -----------------------------
    # DFS path detection
    # -----------------------------
    def find_paths(self, start, end, path=None):
        if path is None:
            path = [start]

        if start == end:
            return [path]

        if start not in self.graph:
            return []

        paths = []

        for node in self.graph[start]:
            if node not in path:
                new_paths = self.find_paths(node, end, path + [node])
                for p in new_paths:
                    paths.append(p)

        return paths

    # -----------------------------
    # Missing link detection
    # -----------------------------
    def detect_missing_links(self, hypothesis):
        start = hypothesis.subject
        end = hypothesis.object

        paths = self.find_paths(start, end)

        if paths:
            return []

        return [(start, "potential_link", end)]

    # -----------------------------
    # Compute Z
    # -----------------------------
    def compute_Z(self):
        nodes = self.nodes()
        n = len(nodes)
        if n <= 1:
            return 1.0

        possible_edges = n * (n - 1)
        actual_edges = sum(len(self.graph[src]) for src in self.graph)

        return actual_edges / possible_edges

    # -----------------------------
    # Compute Sigma
    # -----------------------------
    def compute_Sigma(self):
        nodes = self.nodes()
        if not nodes:
            return 0.0

        visited = set()
        components = 0

        for node in nodes:
            if node not in visited:
                components += 1
                stack = [node]
                while stack:
                    n = stack.pop()
                    if n not in visited:
                        visited.add(n)
                        neighbors = list(self.graph.get(n, {}).keys())
                        reverse = [src for src in self.graph if n in self.graph[src]]
                        stack.extend(neighbors + reverse)

        return components / len(nodes)

    # -----------------------------
    # Run analysis
    # -----------------------------
    def analyze(self, hypothesis):
        Z = self.compute_Z()
        Sigma = self.compute_Sigma()

        hypothesis.Z = Z
        hypothesis.Sigma = Sigma

        decay = 0.95
        hypothesis.confidence *= (1 - Z) * Sigma * decay

        hypothesis.history.append({
            "timestamp": time.time(),
            "Z": Z,
            "Sigma": Sigma,
            "confidence": hypothesis.confidence
        })

        paths = self.find_paths(hypothesis.subject, hypothesis.object)
        missing_links = self.detect_missing_links(hypothesis)

        return {
            "Z": Z,
            "Sigma": Sigma,
            "confidence": hypothesis.confidence,
            "paths": paths,
            "missing_links": missing_links
        }