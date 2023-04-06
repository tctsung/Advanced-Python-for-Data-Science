import math
import numpy as np
import multiprocessing as mp
import time


def f(x): #Doesnot releast GIL
    print (x)
    y = [1]*5000000
    [math.exp(i) for i in y]
    
def g(x):   #Releases GIL
    print (x)
    y = np.ones(5000000)
    np.exp(y)
            
if __name__ == "__main__":
    start = time.time()
    pool = mp.Pool(4)

    results_mp = pool.map(f, [x for x in range(10)])

    pool.close()
    print(f'Finished in {(time.time() - start):.4f} seconds')