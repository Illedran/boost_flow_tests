import numpy as np

n = 2 ** 16
m = int(np.log2(n))

U_min = 0
U_max = 2 ** 8

with open('sample_' + str(n) + '-' + str(m) + '_' + str(U_min) + '-' + str(U_max) + '.txt', 'w') as f:
    f.write(str(n) + ' ' + str(m) + '\n')
    f.write('0 ' + str(n - 1) + '\n')
    for i in range(n):
        for j in np.random.choice(n, np.random.randint(0, m), replace=False):
            f.write(str(i) + ' ' + str(j) + ' ' + str(np.random.randint(U_min, U_max)) + '\n')
