import numpy as np

from utility import parse_edge_list


def augmenting_dfs(G, s, t, residual_capacity, flow):
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
            if not visited[u] and residual_capacity[v, u] > 0:
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

        print(' '.join(reversed(ll)), len(ll))

    return True if min_capacity[t] != np.inf else False


def ford_fulkerson(G, s, t, residual_capacity):
    flow = np.zeros((n, n), dtype=np.int)

    augmenting_path = True
    cycles = 0

    while augmenting_path:
        augmenting_path = augmenting_dfs(G, s, t, residual_capacity, flow)
        cycles += 1

    print(cycles)
    return sum(flow[:, t]), flow


if __name__ == "__main__":
    G, s, t, capacity, n, m = parse_edge_list('sample_1024-10_1-256.txt')

    f, flow = ford_fulkerson(G, s, t, capacity)

    print(f)
