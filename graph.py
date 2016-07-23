class AdjacencyListVertex(object):
    def __init__(self, id):
        self.id = id
        self._adjacent = []

    def add_edge(self, to):
        self._adjacent.append(to)

    def __str__(self):
        return str(self._adjacent)

    def adjacent(self):
        return self._adjacent


class AdjacencyListGraph(object):
    def __init__(self):
        self._vertices = []

    def add_vertex(self):
        v = AdjacencyListVertex(len(self._vertices))
        self._vertices.append(v)
        return v

    def __str__(self):
        return '\n'.join([str(v.id) + ": " + str(v) for v in self._vertices])

    def __getitem__(self, item):
        return self._vertices[item]

    def __len__(self):
        return len(self._vertices)

    def connected(self, source, dst):
        return dst in self[source].adjacent()
