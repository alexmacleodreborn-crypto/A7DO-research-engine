import time
from collections import defaultdict


class Hypothesis:
    def __init__(self, text):
        self.text = text
        self.confidence = 0.2
        self.Z = 0
        self.Sigma = 0
        self.history = []


class A7DOResearchEngine:
    def __init__(self):
        self.graph = defaultdict(dict)

    # -----------------------------
    # Add relation
    # -----------------------------
    def add_relation(self, source, relation, target):
        self.graph[source][target] = relation

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
    # Path Detection (DFS)
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
    # Compute Z (rigidity)
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
    # Compute Sigma (entropy proxy)
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

        # Detect paths related to hypothesis wording
        detected_paths = []
        nodes = self.nodes()

        for a in nodes:
            for b in nodes:
                if a != b:
                    paths = self.find_paths(a, b)
                    if paths:
                        for p in paths:
                            if len(p) > 1:
                                detected_paths.append(p)

        return {
            "Z": Z,
            "Sigma": Sigma,
            "confidence": hypothesis.confidence,
            "paths": detected_paths
        }