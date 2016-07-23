import numpy as np

from utility import get_small_world_network

n = 2 ** 10

G, m = get_small_world_network(n)


def dfs(G, s):
    visited = [False for v in range(len(G[:]))]
    stack = [s]
    visited[s] = True
    while stack:
        v = stack.pop()
        for u in G[v].adjacent():
            if not visited[u]:
                stack.append(u)

    print(sum(visited), sum(visited) / len(visited))


capacity = np.random.randint(0, 10, size=((n, n)))
flow = np.zeros((n, n))

dfs(G, 0)
print(n, m)
