#####
# writing the code in the mpi1.py file
#####

from mpi4py import MPI

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
print('hello world: size = {}, rank = {}'.format(size, rank))
