#####
# this code is similar to mpi3.py, 
# but it uses Wait to block the processes
#####

import numpy
from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()

randNum = numpy.zeros(1)

if rank == 1:
        randNum = numpy.random.random_sample(1)
        print("Process", rank, "drew the number", randNum[0])
        
        req = comm.Isend(randNum, dest=0)    # I = immediate, don't care about when to send
        # req.Wait()    # wait until sth is received by another node
        
        print('something here')
        
if rank == 0:
        print("Process", rank, "before receiving has the number", randNum[0])
        
        req = comm.Irecv(randNum, source=1)  # I = immediate, don't care about receive or not
        # req.Wait() # wait until receive sth
        while not req.Test():
            print('waiting')
        
        print("Process", rank, "received the number", randNum[0])
