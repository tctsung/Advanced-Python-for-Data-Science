
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD

my_rank = comm.Get_rank()
p = comm.Get_size()

n = 100

if my_rank == 0:
    data = np.random.random(n).astype('f')       
    data = data.reshape(p, int(n/p))    
    
else:
    data = None

recvbuf = np.empty(int(n/p),dtype='f')

#Scatter the numbers to all processes
comm.Scatter(data,recvbuf, root = 0)

local_sum = sum(recvbuf)
print('Process {}, local sum = {:.4f}'.format(my_rank, local_sum))

#Reduce local sums into a global sum to calculate the mean
global_sum = comm.allreduce(local_sum, MPI.SUM)
mean = global_sum/n

#Compute the local sum of squared differences from the mean

local_sq_diff = sum((num-mean)**2 for num in recvbuf)

#Reduce the global sum of the squared differences to the root process
global_sq_diff = comm.reduce(local_sq_diff, MPI.SUM, 0)

if my_rank == 0:
    stddev = np.sqrt(global_sq_diff / n)
    print('\nMean: {:.4f}, Standard deviation: {:.4f}'.format(mean, stddev))
    print('Standard deviation using numpy: {:.4f}'.format(np.std(data)))
