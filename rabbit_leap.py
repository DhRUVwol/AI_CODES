# missionaries_cannibals.py
from collections import deque

def valid(state):
    ml, cl, boat, mr, cr = state
    # each bank: missionaries >= cannibals unless missionaries == 0
    def ok(m, c):
        return m == 0 or m >= c
    return 0 <= ml <= 3 and 0 <= cl <= 3 and 0 <= mr <= 3 and 0 <= cr <= 3 and ok(ml, cl) and ok(mr, cr)

def successors(state):
    ml, cl, boat, mr, cr = state
    moves = [(2,0),(0,2),(1,1),(1,0),(0,1)]
    succs = []
    if boat == 'L':
        for dm, dc in moves:
            nml, ncl = ml - dm, cl - dc
            nmr, ncr = mr + dm, cr + dc
            ns = (nml, ncl, 'R', nmr, ncr)
            if valid(ns): succs.append(ns)
    else:
        for dm, dc in moves:
            nml, ncl = ml + dm, cl + dc
            nmr, ncr = mr - dm, cr - dc
            ns = (nml, ncl, 'L', nmr, ncr)
            if valid(ns): succs.append(ns)
    return succs

def bfs(start, goal):
    q = deque([start])
    parent = {start: None}
    while q:
        s = q.popleft()
        if s == goal:
            path = []
            while s is not None:
                path.append(s); s = parent[s]
            return list(reversed(path))
        for nxt in successors(s):
            if nxt not in parent:
                parent[nxt] = s
                q.append(nxt)
    return None

def dfs(start, goal, limit=10000):
    stack = [start]
    parent = {start: None}
    visited = set([start])
    while stack:
        s = stack.pop()
        if s == goal:
            path = []
            while s is not None:
                path.append(s); s = parent[s]
            return list(reversed(path))
        for nxt in successors(s):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = s
                stack.append(nxt)
    return None

if __name__ == "__main__":
    start = (3,3,'L',0,0)
    goal  = (0,0,'R',3,3)
    print("BFS solution:")
    sol = bfs(start, goal)
    for s in sol:
        print(s)
    print("\nDFS (may be non-optimal) solution:")
    sol2 = dfs(start, goal)
    for s in sol2:
        print(s)
