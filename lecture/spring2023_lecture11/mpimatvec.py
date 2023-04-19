
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = size * 2
m = 5
if rank == 0:
    A = np.random.randn(n, m)
    x = np.random.randn(m)

    ytarget = A.dot(x) # to check the result
    
    A = A.reshape(size, -1, m)
else:
    A = None
    x = np.zeros(m)

Asmall = np.zeros((n // size, m))

# Asmall = comm.scatter(A, root=0)
comm.Scatter(A, Asmall, root=0)

# x = comm.bcast(x, root=0)
comm.Bcast(x, root=0)

print('rank', rank, ':', Asmall.shape, x.shape)

ysmall = Asmall.dot(x)

# y = comm.gather(ysmall, root=0)
y = np.zeros((size, n // size))
comm.Gather(ysmall, y, root=0)

if rank == 0:
    print(np.concatenate(y))
    print(ytarget)
