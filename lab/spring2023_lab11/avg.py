
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD

my_rank = comm.Get_rank()
p = comm.Get_size()

n = 100

if my_rank == 0:
    data = np.arange(n,dtype='f')       #shape: (100)
    data = data.reshape(p, int(n/p))    #shape: (4,25), each process gets 25
    recvbuf = np.empty(int(n/p),dtype='f')
    comm.Scatter(data,recvbuf, root = 0)    
    
else:
    recvbuf = np.empty(int(n/p),dtype='f')
    data = None

# recvbuf = np.empty(int(n/p),dtype='f')

#Scatter the numbers to all processes
# comm.Scatter(data,recvbuf, root = 0)    

#Compute the average of subset
sub_avg = np.mean(recvbuf)             

print('Process {}, sub array average is {}'.format(my_rank,sub_avg))

sub_avgs = None

if my_rank == 0:
    sub_avgs = np.empty(p,dtype='f')

#Gather the partial averages down to the root process
#Comm.Gather(sendbuf, recvbuf, root=0)
comm.Gather(sub_avg, sub_avgs, root=0)
    
#Compute the total average of all numbers
if my_rank == 0:
    avg = np.mean(sub_avgs)
    print('Average is',avg)
