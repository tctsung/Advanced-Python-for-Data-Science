from mpi4py import MPI
import numpy as np
comm = MPI.COMM_WORLD    # global communicator
rank = comm.Get_rank()   # current rank
N = comm.Get_size()     # -n 16
def I(M, k, n=10000):   
    """
    M: upperbound of the integration
    k: the kth momentum
    n: number of splits for trapezoidal rule, default=10000
    """
    bounds = np.linspace(0,M,n)  # split M to n pieces
    interval = M/n               # the interval(x-axis length) of each partial sum
    sums = 0                     # buffer to calculate integration
    for i in range(n):
        x = bounds[i]
        fx = np.exp(-x)     # f(x)
        y = x**k * fx
        sums += interval*y
    return sums
if rank==0:
    M=np.array([1000])
else:
    M=np.zeros(1, dtype=int)

comm.Bcast(M, root=0)
M += 1000*rank   # add 1000 per rank
Jk = I(M[0], rank, n=10000)
Jks = comm.gather(Jk, root=0)
if rank==0:
    for i in range(N):
        print(f"The {i}-th moment approximation(J{i}): {Jks[i]}")
        
        
    
    
