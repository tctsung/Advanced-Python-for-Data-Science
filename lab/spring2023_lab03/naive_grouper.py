import resource

def naive_grouper(inputs, n):
    num_groups = len(inputs) // n
    return [tuple(inputs[i*n:(i+1)*n]) for i in range(num_groups)]

for _ in naive_grouper(range(100000000), 10):
    pass

## Comment out this line if on Linux machine
print("Memory Used(kB): ", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)