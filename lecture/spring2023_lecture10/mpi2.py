
from mpi4py import MPI
rank = MPI.COMM_WORLD.Get_rank()

a = 8.0
b = 4.0

print('Process rank',rank)
# ways to do different things in one parallel computing
if rank == 0:
        print("addition:", a + b)

if rank == 1:
        print("multiplication:", a * b)

if rank == 2:
        print("maximum:", max(a,b))
        
if rank == 3:
        print("doing nothing:")
