import numpy as np
import time

n = 1000000

a = np.random.rand(n)
b = np.random.rand(n)

c = np.zeros(n)

s = time.time()
for i in range(a.size):
	c[i] = a[i]*b[i]
e = time.time()

print(e-s)

s = time.time()
c = np.multiply(a,b)
e = time.time()

print(e-s)
