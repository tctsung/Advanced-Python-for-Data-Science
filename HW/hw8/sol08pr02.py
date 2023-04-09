import numpy
import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD    # global communicator
rank = comm.Get_rank()   # current rank
T = 10 # 10 task

# MPI:
if rank == 0:
    # read standard inputs:
    for line in sys.stdin:
        x = float(line)        
        if x != 0.0:
            break
    for line in sys.stdin:
        y = float(line)        
        if y != 0.0:
            break
    comm.send(y, dest=1, tag=100)  # send y to 2nd process
    p = 1                          # initiate value p as 1
    for i in range(T//2):    # 5 task in process 0
        p *= x  
        comm.send(p, dest=1) # send message 00, 02, 04, 06, 08
        p = comm.recv(source=1) # receive message 01, 03, 05, 07, 09
    print(f"Final output of p using input {x} & {y}: {p}")
elif rank == 1:
    y = comm.recv(source=0, tag=100)
    for i in range(T//2):    # 5 task in process 1
        p = comm.recv(source=0) # receive message 00, 02, 04, 06, 08
        p /= y 
        comm.send(p, dest=0)    # send message 01, 03, 05, 07, 09
    
