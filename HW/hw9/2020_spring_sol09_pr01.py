from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD    # global communicator
rank = comm.Get_rank()   # current rank
sz = comm.Get_size()     # -n
n = 256000
# MPI:
if rank == 0:
    
    data = np.random.uniform(0,1, size=[sz,int(n/sz)]).astype('f')  
else:
    data = None

recvbuf = np.empty(int(n/sz), dtype="f")  # buffer to receive
comm.Scatter(data,recvbuf, root = 0)    # scatter data evenly to each worker
local_sum = sum(recvbuf)
global_sum = comm.allreduce(local_sum, MPI.SUM)   # gather sum from all process
global_mean = global_sum/n
local_sq_diff = sum((num-global_mean)**2 for num in recvbuf) 
global_sq_diff = comm.reduce(local_sq_diff, MPI.SUM, 0)
if rank == 0:
    global_sd = (global_sq_diff/n)**0.5
    print(f"Mean by MPI: {global_mean:.5f}, SD by MPI: {global_sd:.5f}")
    print(f"Mean by numpy built-in: {np.mean(data):.5f}, SD numpy built-in: {np.std(data):.5f}")
