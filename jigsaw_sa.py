# jigsaw_sa.py
import numpy as np, random, math

def mismatch_score(pieces, arrangement, piece_size):
    # strip: simple boundary mismatch - use edge pixel sums (toy example)
    total = 0
    N = len(arrangement)
    side = int(math.sqrt(N))
    # pieces: dict idx->array (piece_size, piece_size)
    grid = np.array(arrangement).reshape(side,side)
    for r in range(side):
        for c in range(side):
            idx = grid[r,c]
            if c+1 < side:
                right_idx = grid[r,c+1]
                total += np.sum((pieces[idx][:,-1] - pieces[right_idx][:,0])**2)
            if r+1 < side:
                down_idx = grid[r+1,c]
                total += np.sum((pieces[idx][-1,:] - pieces[down_idx][0,:])**2)
    return total

def simulated_anneal_jigsaw(pieces, init_arrangement, T0=1000, alpha=0.99, Tmin=0.1):
    arr = init_arrangement.copy()
    best = arr.copy(); best_cost = mismatch_score(pieces, arr, None)
    T = T0
    while T > Tmin:
        i,j = random.sample(range(len(arr)),2)
        cand = arr.copy(); cand[i], cand[j] = cand[j], cand[i]
        cost = mismatch_score(pieces, cand, None)
        dE = cost - mismatch_score(pieces, arr, None)
        if dE < 0 or random.random() < math.exp(-dE/T):
            arr = cand
            if cost < best_cost:
                best, best_cost = arr.copy(), cost
        T *= alpha
    return best, best_cost

if __name__ == "__main__":
    # Toy: create 9 pieces (3x3) of small arrays with random noise around a base image to simulate scrambled pieces
    base = np.arange(9*9).reshape(9,9)
    pieces = {i: base + np.random.randn(3,3)*10 for i in range(9)}
    init = list(range(9)); random.shuffle(init)
    best, cost = simulated_anneal_jigsaw(pieces, init)
    print("Final cost:", cost)
    print("Arrangement:", best)
