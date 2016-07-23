import numpy as np

from utility import parse_edge_list


def distance(G, s, residual_capacity):
    visited = np.zeros(len(G), dtype=np.bool)
    distance_vector = list(np.full(len(G), np.inf))
    distance_vector[s] = 0
    stack = [s]
    while stack:
        v = stack.pop(0)
        visited[v] = True
        for u in G[v].adjacent():
            if not visited[u] and residual_capacity[v, u] > 0:
                stack.append(u)
                distance_vector[u] = min(distance_vector[u], distance_vector[v] + 1)

    return distance_vector


def augmenting_dfs(G, s, t, residual_capacity, flow, distance_vector):
    visited = np.zeros(len(G), dtype=np.bool)
    fathers = -np.ones(len(G), dtype=np.int)
    min_capacity = list(np.full(len(G), np.inf))
    stack = [s]
    while stack:
        v = stack.pop()
        visited[v] = True
        if v == t:
            break
        for u in G[v].adjacent():
            if not visited[u] and residual_capacity[v, u] > 0 and distance_vector[v] + 1 == distance_vector[u]:
                stack.append(u)
                fathers[u] = v
                min_capacity[u] = min(min_capacity[v], residual_capacity[v, u])

    if min_capacity[t] != np.inf:
        current = t
        ll = []
        while current:
            ll.append(str(current))
            residual_capacity[fathers[current], current] -= min_capacity[t]
            flow[fathers[current], current] += min_capacity[t]
            residual_capacity[current, fathers[current]] += min_capacity[t]
            flow[current, fathers[current]] -= min_capacity[t]
            current = fathers[current]

        print(' '.join(reversed(ll)), '-', len(ll), 'Capacity:', min_capacity[t])

    return True if min_capacity[t] != np.inf else False


def dinic(G, s, t, capacity):
    flow = np.zeros((n, n), dtype=np.int)
    augmenting_path = True

    while augmenting_path:
        distance_vector = distance(G, s, capacity)
        print(distance_vector)
        augmenting_path = augmenting_dfs(G, s, t, capacity, flow, distance_vector)

    return sum(flow[:, t]), flow


if __name__ == "__main__":
    G, s, t, capacity, n, m = parse_edge_list('sample.txt')

    f, flow = dinic(G, s, t, capacity)

    # print(capacity)
    # print(flow)
    print(f)
