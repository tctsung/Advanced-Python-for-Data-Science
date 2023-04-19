
from mpi4py import MPI
import numpy as np
import timeit

comm = MPI.COMM_WORLD

my_rank = comm.Get_rank()
p = comm.Get_size()

def merge(L, R):

    f=[]
    i = j = 0
          
    # Copy data to temp arrays L[] and R[] 
    while i < len(L) and j < len(R): 
        if L[i] < R[j]: 
            f.append(L[i] )
            i+=1
        else: 
            f.append(R[j]) 
            j+=1

    # Checking if any element was left 
    while i < len(L): 
        f.append(L[i]) 
        i+=1

    while j < len(R): 
        f.append(R[j]) 
        j+=1
    
    return f

def merge_sort(l):
    
    if len(l) <= 1:
        return l
    
    left = merge_sort(l[: len(l)//2])
    right = merge_sort(l[len(l)//2 :])
    
    
    return merge(left, right)


n = 10000


def serial_mergesort():
    data = np.random.randint(0, n, n).astype('f')
    sorted_data = merge_sort(data)
        

def par_mergesort():
    if my_rank == 0:
        data = np.random.randint(0, n, n).astype('f')
        data = data.reshape(p, int(n/p))    
        print(data.shape)
    else:
        data = None

    sub_array = np.empty(int(n/p),dtype='f')
    print(sub_array.shape)
    #Send subarrays to each process
    comm.Scatter(data,sub_array, root = 0)

    sorted_arr = merge_sort(sub_array)

    data = comm.gather(sorted_arr,root=0)
    
    if my_rank == 0:
        j = len(data)-1

        while j != 0:
            i = 0
            while i<j:
                data[i] = merge(data[i], data[j])
                i += 1
                j -= 1

        l = data[0]
        assert all(l[i] <= l[i+1] for i in range(len(l)-1))

        
tp = timeit.Timer("par_mergesort()","from __main__ import par_mergesort")
ts = timeit.Timer("serial_mergesort()","from __main__ import serial_mergesort")

parallel_time = tp.timeit(number=10)


if my_rank == 0:
    serial_time = ts.timeit(number=10)
    
    print ('Parallel time: {:.4f} sec'.format(parallel_time)) 
    print ('Serial time: {:.4f} sec'.format(serial_time)) 

