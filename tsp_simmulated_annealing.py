# tsp_simulated_annealing.py
import random, math
import numpy as np

def dist(a,b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def tour_length(tour, coords):
    return sum(dist(coords[tour[i]], coords[tour[(i+1)%len(tour)]]) for i in range(len(tour)))

def neighbor_swap(tour):
    a,b = sorted(random.sample(range(len(tour)),2))
    nt = tour.copy()
    nt[a:b+1] = reversed(nt[a:b+1])
    return nt

def simulated_annealing(coords, T0=1000, alpha=0.995, Tmin=1e-3, max_iter=20000):
    n = len(coords)
    tour = list(range(n))
    random.shuffle(tour)
    best = tour.copy(); best_cost = tour_length(tour, coords)
    T = T0
    it = 0
    while T > Tmin and it < max_iter:
        cand = neighbor_swap(tour)
        dE = tour_length(cand, coords) - tour_length(tour, coords)
        if dE < 0 or random.random() < math.exp(-dE/T):
            tour = cand
            cur_cost = tour_length(tour, coords)
            if cur_cost < best_cost:
                best, best_cost = tour.copy(), cur_cost
        T *= alpha
        it += 1
    return best, best_cost

if __name__ == "__main__":
    # 20 sample coordinates (Rajasthan tourist approx positions)
    coords = [(random.uniform(0,100), random.uniform(0,100)) for _ in range(20)]
    best, cost = simulated_annealing(coords)
    print("Best cost:", cost)
    print("Tour:", best)
