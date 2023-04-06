import time
import threading
import numpy as np
import multiprocessing as mp

def factorial_upto(n):
    res = [1]
    
    for i in range(1, n + 1):
        res.append(res[-1] * i)
    return res

def taylor_exp(x,n=1000):
    
    factorials = factorial_upto(n)
    
    res = 0
    for i in range(n):
        res += x**i / factorials[i]
    
    return res

if __name__ == '__main__':
    arr = np.random.randint(0, 10, size=[5000])
    data = arr.tolist()
    results = []
    for x in data:
        results.append(taylor_exp(x))
    start = time.time()
    pool = mp.Pool(mp.cpu_count())
    results_mp = pool.map(taylor_exp, [x for x in data])
    pool.close()
    print(f'Finished in {(time.time() - start):.4f} seconds')

    assert (results_mp == results)