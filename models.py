# models.py

class SymbolicRelation:
    def __init__(self, source, relation, target):
        self.source = source.strip()
        self.relation = relation.strip()
        self.target = target.strip()

    def as_tuple(self):
        return (self.source, self.relation, self.target)


class SymbolicHypothesis:
    def __init__(self, subject, relation, obj):
        self.subject = subject.strip()
        self.relation = relation.strip()
        self.object = obj.strip()

        self.confidence = 0.2
        self.Z = 0
        self.Sigma = 0
        self.history = []

    def as_tuple(self):
        return (self.subject, self.relation, self.object)