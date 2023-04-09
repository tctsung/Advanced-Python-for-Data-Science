import numpy
from mpi4py import MPI

comm = MPI.COMM_WORLD    # global communicator
N = comm.Get_size()     # num of process
rank = comm.Get_rank()   # current rank
data = numpy.array([0], dtype='i')   # initialize with 0; this is the buffer


if rank == 0:   # 1st node
    comm.Send([data, MPI.INT], dest=1)  
    comm.Recv([data, MPI.INT], source=(N-1))
    print(data)
elif rank == (N-1): # last node
    comm.Recv([data, MPI.INT], source=(rank-1)) # receive info from previous rank
    data = rank**2 + data
    comm.Send([data, MPI.INT], dest=0) 
else: 
    comm.Recv([data, MPI.INT], source=(rank-1)) # receive info from previous rank
    data = rank**2 + data                       # update info
    comm.Send([data, MPI.INT], dest=(rank+1))   # send to next dest
    
    
