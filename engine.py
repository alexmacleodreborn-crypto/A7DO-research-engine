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

    def add_relation(self, source, relation, target):
        self.graph[source][target] = relation

    def nodes(self):
        nodes = set(self.graph.keys())
        for src in self.graph:
            for tgt in self.graph[src]:
                nodes.add(tgt)
        return list(nodes)

    def compute_Z(self):
        nodes = self.nodes()
        n = len(nodes)
        if n <= 1:
            return 1.0

        possible_edges = n * (n - 1)
        actual_edges = sum(len(self.graph[src]) for src in self.graph)
        return actual_edges / possible_edges

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

        return {
            "Z": Z,
            "Sigma": Sigma,
            "confidence": hypothesis.confidence
        }