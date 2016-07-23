import numpy as np


# residual capacity
def calculate_delta(residual_capacity, cut):
    return np.sum(residual_capacity[:cut, cut:])


n = 6
s = 0  # source
t = -1  # sink

adj_matrix = np.random.randint(0, 1 + 1, size=(n, n))
for i in range(n):
    # i != j
    adj_matrix[i, i] = 0
    for j in range(i, n):
        # For each (i,j), (j,i) is also in A
        adj_matrix[i, j] = adj_matrix[j, i]

# For every internal i, (s,i) and (i,t) are in A
adj_matrix[s, s + 1:t] = 1
adj_matrix[s + 1:t, t] = 1

# No external edges connect to s, or from t
adj_matrix[:, s] = 0
adj_matrix[t, :] = 0

m = np.sum(adj_matrix)

rand_par = 100

capacity = np.zeros((n, n), dtype=np.int)

for i in range(n):
    for j in range(n):
        if adj_matrix[i, j]:
            capacity[i, j] = np.random.exponential(rand_par)

U_max = np.max(capacity)
U_min = np.min(capacity[capacity > 0])
U_star = U_max / U_min

flow = np.zeros((n, n, 1), dtype=np.int)
residual_capacity = np.dstack([capacity])
cut = np.random.randint(1, n, dtype=np.int, size=(1))
delta = np.array([calculate_delta(residual_capacity[:, :, -1], cut[-1])])

i = 0
maximum = False
while not maximum:
    # new_flow, new_residual_capacity, new_cut = improvement_phase(flow[:,:,-1], residual_capacity[:,:,-1], cut[-1])
    # flow = np.dstack([flow, new_flow])
    # residual_capacity = np.dstack([residual_capacity, new_residual_capacity])
    # cut = np.hstack([cut, new_cut])
    # delta = np.hstack([delta, calculate_delta(residual_capacity[:,:,-1], cut[-1]))
    maximum = True

print("n =", n, "| m =", m, "| U_max =", U_max, "| U_min =", U_min, "| U* =", U_star)
print(adj_matrix)
print(residual_capacity[:, :, -1])
print(flow[:, :, -1])
print(cut[-1], delta[-1])
