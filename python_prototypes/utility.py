import numpy as np

from python_prototypes.graph import AdjacencyListGraph as Graph
from python_prototypes.graph import AdjacencyListVertex


def get_small_world_network(n):
    G = Graph()
    edges = 0
    vertices = np.empty(n, dtype=AdjacencyListVertex)
    for i in range(n):
        vertices[i] = G.add_vertex()
    for v in vertices:
        out_edges = np.random.choice(n, np.random.randint(0, np.log2(n)), replace=False)
        for j in out_edges:
            v.add_edge(j)
            vertices[j].add_edge(v.id)
            edges += 2
    return G, edges


def parse_edge_list(input_file):
    G = Graph()
    f = open(input_file)
    x = f.readlines()
    n, m = x[0].strip().split()
    s, t = x[1].strip().split()
    n = int(n);
    m = int(m);
    s = int(s);
    t = int(t)
    data = np.genfromtxt(input_file, skip_header=2, dtype=np.int)
    capacity = np.zeros((n, n), dtype=np.int)
    for _ in range(n):
        G.add_vertex()
    for source, dst, edge_cap in data:
        if G.connected(source, dst):
            capacity[source, dst] += edge_cap
        else:
            G[source].add_edge(dst)
            G[dst].add_edge(source)
            capacity[source, dst] = edge_cap

    return G, s, t, capacity, n, m
