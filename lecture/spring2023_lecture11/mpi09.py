import numpy
from math import sin
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def integral(a_r, h, n):
    integ = 0.0
    for j in range(n):
        t = a_r + (j + 0.5) * h
        integ += sin(t) * h
    return integ


a = 0.0
b = numpy.pi / 2
dest = 0
my_int = numpy.zeros(1)
integral_sum = numpy.zeros(1)

# Initialize value of n only if this is rank 0
if rank == 0:
    n = numpy.full(1, 500, dtype=int) # default value
else:
    n = numpy.zeros(1, dtype=int)

# Broadcast n to all processes
print("Process ", rank, " before n =", n[0])
comm.Bcast(n, root=0)
print("Process ", rank, " after n =", n[0])

# Compute partition
h = (b - a) / (n * size) # calculate h *after* we receive n
a_r = a + rank * h * n
my_int[0] = integral(a_r, h, n[0])

# Send partition back to root process, computing sum across all partitions
print("Process ", rank, " has the partial integral ", my_int[0])
comm.Reduce(my_int, integral_sum, MPI.SUM, dest)

# Only print the result in process 0
if rank == 0:
    print('The Integral Sum =', integral_sum[0])
