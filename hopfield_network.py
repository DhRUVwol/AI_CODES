# hopfield.py
import numpy as np

def hebbian_weights(patterns):
    N = patterns[0].size
    W = np.zeros((N,N))
    P = len(patterns)
    for p in patterns:
        x = p.reshape(-1,1)
        W += x @ x.T
    np.fill_diagonal(W, 0)
    return W

def recall(W, init, steps=100):
    s = init.copy()
    for _ in range(steps):
        for i in range(len(s)):
            s[i] = 1 if W[i,:].dot(s) >= 0 else -1
    return s

def eight_rook_solution():
    # encode 8x8 board as 64 neurons; produce one valid configuration by heuristic then use hopfield to refine
    # here simply produce one-hot per row
    board = np.zeros((8,8), dtype=int)
    for r in range(8): board[r, r] = 1
    pattern = board.flatten()*2 - 1  # bipolar {+1,-1}
    W = hebbian_weights([pattern])
    noisy = pattern.copy()
    # flip 20% bits
    idx = np.random.choice(len(noisy), size=int(0.2*len(noisy)), replace=False)
    noisy[idx] *= -1
    recovered = recall(W, noisy, steps=10)
    return recovered.reshape(8,8)

if __name__ == "__main__":
    sol = eight_rook_solution()
    print(sol)
