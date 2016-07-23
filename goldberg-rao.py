import numpy as np

from utility import parse_edge_list


def min_capacity_canonical_cut(G, capacity, distance_vector):
    x = np.array(distance_vector)
    cut_capacity = np.zeros(distance_vector[0] + 1, dtype=np.int)
    for v in range(len(G)):
        for u in G[v].adjacent():
            if distance_vector[v] >= distance_vector[u] and capacity[v, u] > 0:
                cut_capacity[distance_vector[v]] += capacity[v, u]

    print(cut_capacity)
    return np.min(cut_capacity)


def length_function(v, u, residual_capacity, Delta):
    if residual_capacity[v, u] >= 3 * Delta:
        return 0
    else:
        return 1


# With recursive DFS
def goldberg_rao_distance(G, s, t, residual_capacity, Delta):
    def recursive(v):
        if v == t:
            distance_vector[t] = 0
        elif np.isinf(distance_vector[v]):
            for u in G[v].adjacent():
                if residual_capacity[v, u] > 0:
                    distance_vector[v] = min(recursive(u) + length_function(v, u, residual_capacity, Delta),
                                             distance_vector[v])
        return distance_vector[v]

    distance_vector = list(np.full(len(G), np.inf))

    # Start a recursive DFS from s
    recursive(s)

    return distance_vector


def augmenting_dfs(G, s, t, residual_capacity, flow, distance_vector, Delta):
    visited = [False for _ in range(len(G))]
    fathers = [-1 for _ in range(len(G))]
    min_capacity = [np.inf for _ in range(len(G))]
    stack = [s]
    while stack:
        v = stack.pop()
        visited[v] = True
        if v == t:
            break
        for u in G[v].adjacent():
            if not visited[u] and residual_capacity[v, u] > 0 and distance_vector[v] == distance_vector[
                u] + length_function(v, u, residual_capacity, Delta):
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


def goldberg_rao(G, s, t, capacity, n, m):
    flow = np.zeros((n, n), dtype=np.int)
    Lambda = min(n ** 2 / 3, m ** 1 / 2)
    F = m * np.max(capacity)
    cycles = 1
    # augmenting_path = True
    while F >= 1:
        print(Lambda)
        Delta = np.ceil(F / Lambda).astype(np.int)
        print(cycles, "delta: ", Delta)
        distance_vector = goldberg_rao_distance(G, s, t, capacity, Delta)
        print(cycles, "distance_vector: ", distance_vector)
        augmenting_path = augmenting_dfs(G, s, t, capacity, flow, distance_vector, Delta)
        F = min_capacity_canonical_cut(G, capacity, distance_vector)
        cycles += 1

    return sum(flow[:, t]), flow


if __name__ == "__main__":
    G, s, t, capacity, n, m = parse_edge_list('sample.txt')

    f, flow = goldberg_rao(G, s, t, capacity, n, m)

    print(f)
