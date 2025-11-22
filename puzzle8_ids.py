# puzzle8_ids.py
from collections import deque

# state is a tuple of length 9, 0 denotes blank
GOAL = (1,2,3,4,5,6,7,8,0)

def moves(state):
    s = list(state)
    i = s.index(0)
    swaps = []
    r, c = divmod(i,3)
    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    for dr,dc in dirs:
        nr, nc = r+dr, c+dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr*3 + nc
            ns = s.copy()
            ns[i], ns[j] = ns[j], ns[i]
            swaps.append(tuple(ns))
    return swaps

def dls(start, limit):
    # depth-limited DFS
    def dfs(node, depth, visited):
        if node == GOAL: return [node]
        if depth == 0: return None
        for nxt in moves(node):
            if nxt not in visited:
                visited.add(nxt)
                res = dfs(nxt, depth-1, visited)
                if res: return [node] + res
                visited.remove(nxt)
        return None
    return dfs(start, limit, set([start]))

def ids(start, max_depth=20):
    for d in range(max_depth+1):
        path = dls(start, d)
        if path: return path
    return None

if __name__ == "__main__":
    start = (1,2,3,4,5,6,0,7,8)  # depth 2 example
    path = ids(start, max_depth=20)
    print("Found path length:", len(path)-1)
    for p in path:
        print(p)
