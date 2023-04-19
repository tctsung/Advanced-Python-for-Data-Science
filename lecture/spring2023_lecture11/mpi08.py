#####
# Finding the piece-wise hermite polynomial interpolation of a set of points
# MPI version
#####
from time import time
import numpy as np
import matplotlib.pyplot as plt
import numpy
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
status = MPI.Status()

ts = time()
numx = 10_000
rank_interval_size = 20 / size
numx_per_rank = int(np.floor(numx / size))

m = np.zeros((numx_per_rank,))

def hermite(data):
    A = np.zeros((4, 4))
    pts = []

    A[0:2]=np.array([np.power(data[0:2], 3),np.power(data[0:2],2),data[0:2],np.array([1,1])]).T
    A[2:4]=np.array([3*np.power(data[0:2],2),2*data[0:2],np.array([1,1]),np.array([0,0])]).T
    b = data[2:]
    coefs = np.linalg.solve(A,b)
    t = np.linspace(data[0], data[1], 100)
    pts.extend(np.polyval(coefs,t))
    return(pts)


if rank == 0:
    l = []
    x = np.linspace(0, rank_interval_size, numx_per_rank)
    y = np.random.uniform(low=-1, high=1, size=numx_per_rank) + 100 * np.sin(x)
    for i in range(numx_per_rank-1):
        data = np.array([x[i], x[i+1], y[i], y[i+1], m[i], m[i+1]])
        l.extend(hermite(data))
        
    # Process 0 serves also as receiver
    pts = np.zeros((np.asarray(l).shape[0], ))
    for p in range(1, size):
        comm.Recv(pts, source=p)
        l.extend(np.ndarray.tolist(pts))
        
    np.save('mpi_hermite_cpt.npy', np.asarray([x, y]))
    np.save('mpi_hermite.npy', np.asarray(l))

else:
    l = []
    x = np.linspace(rank*rank_interval_size,(rank + 1)*rank_interval_size, numx_per_rank)
    y = np.random.uniform(low=-1,high=1, size=numx_per_rank) + 100 * np.sin(x)
    for i in range(numx_per_rank-1):
        data = np.array([x[i], x[i+1], y[i], y[i+1], m[i], m[i+1]])
        l.extend(hermite(data))
    
    pts = np.asarray(l) 
    comm.Send(pts,dest=0)
    
print('Rank ',rank,' Took {}s'.format(time() - ts))
