import resource

def better_grouper(inputs, n):
    iters = [iter(inputs)] * n
    return zip(*iters)


for _ in better_grouper(range(100000000), 10):
    pass

## Comment out this line if on Linux machine
print("Memory Used(kB): ", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)