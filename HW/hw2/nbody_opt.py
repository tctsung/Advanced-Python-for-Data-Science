"""
    N-body simulation.
    modification to reduce function call overhead
"""
from itertools import combinations
def advance(dt, bodies, iterations):
    '''
        advance the system one timestep
    '''
    for _ in range(iterations):
        its = combinations(bodies, 2)
        for b1, b2 in its:
            ([x1, y1, z1], v1, m1) = bodies[b1]
            ([x2, y2, z2], v2, m2) = bodies[b2]
            # (dx, dy, dz) = (x1-x2, y1-y2, z1-z2)
            (dx, dy, dz) = (x1-x2, y1-y2, z1-z2)
            # dxyz2 = dt*sum(map(lambda x: (x**2), dxyz))**(-1.5)
            # this part not good enough
            cp_b_1 = m2 * dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
            cp_b_2 = m1 * dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
            # v1[0], v1[1], v1[2] = list(v1[i]-dxyz[i]*cp_b_1 for i in range(3)) 
            # v2[0], v2[1], v2[2] = list(v2[i]+dxyz[i]*cp_b_2 for i in range(3))
            v1[0] -= dx * cp_b_1
            v1[1] -= dy * cp_b_1
            v1[2] -= dz * cp_b_1
            v2[0] += dx * cp_b_2
            v2[1] += dy * cp_b_2
            v2[2] += dz * cp_b_2
        for body in bodies.keys():
            r,v,m = bodies[body]
            r[0],r[1],r[2] = list(r[i]+(dt*v[i]) for i in range(3)) 

def report_energy(bodies, e=0.0):
    '''
    compute the energy and return it so that it can be printed
    '''
    its = combinations(bodies, 2)
    for b1, b2 in its:
        ([x1, y1, z1], v1, m1) = bodies[b1]
        ([x2, y2, z2], v2, m2) = bodies[b2]
        (dx, dy, dz) = (x1-x2, y1-y2, z1-z2)
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)
    # e += sum(map(lambda body:(bodies[body][2]*(bodies[body][1][0]**2+bodies[body][1][1]**2+bodies[body][1][2]**2) / 2), bodies))
    for body in bodies.keys():
        (r, [vx, vy, vz], m) = bodies[body]
        e += m * (vx * vx + vy * vy + vz * vz) / 2.
        
    return e

def offset_momentum(reference, bodies, px=0.0, py=0.0, pz=0.0):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''
    ref = bodies[reference]
    for body in bodies.keys():
        (r, [vx, vy, vz], m) = bodies[body]
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m


def nbody(loops, reference, iterations):
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
    '''
    # Set up global state
    pi = 3.14159265358979323
    solar_mass = 4 * pi * pi
    days_per_year = 365.24
    bodies = {
        'sun': ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], solar_mass),

        'jupiter': ([4.84143144246472090e+00,
                     -1.16032004402742839e+00,
                     -1.03622044471123109e-01],
                    [1.66007664274403694e-03 * days_per_year,
                     7.69901118419740425e-03 * days_per_year,
                     -6.90460016972063023e-05 * days_per_year],
                    9.54791938424326609e-04 * solar_mass),

        'saturn': ([8.34336671824457987e+00,
                    4.12479856412430479e+00,
                    -4.03523417114321381e-01],
                   [-2.76742510726862411e-03 * days_per_year,
                    4.99852801234917238e-03 * days_per_year,
                    2.30417297573763929e-05 * days_per_year],
                   2.85885980666130812e-04 * solar_mass),

        'uranus': ([1.28943695621391310e+01,
                    -1.51111514016986312e+01,
                    -2.23307578892655734e-01],
                   [2.96460137564761618e-03 * days_per_year,
                    2.37847173959480950e-03 * days_per_year,
                    -2.96589568540237556e-05 * days_per_year],
                   4.36624404335156298e-05 * solar_mass),

        'neptune': ([1.53796971148509165e+01,
                     -2.59193146099879641e+01,
                     1.79258772950371181e-01],
                    [2.68067772490389322e-03 * days_per_year,
                     1.62824170038242295e-03 * days_per_year,
                     -9.51592254519715870e-05 * days_per_year],
                    5.15138902046611451e-05 * solar_mass)}
    offset_momentum(reference, bodies)

    for _ in range(loops):
        report_energy(bodies)
        advance(0.01, bodies, iterations)
        print(report_energy(bodies))

if __name__ == '__main__':
    nbody(100, 'sun', 20000)
    # nbody(10, 'sun', 20)