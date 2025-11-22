# sat_local_search.py
import random
from collections import defaultdict

def eval_assignment(clauses, assignment):
    satisfied = 0
    for c in clauses:
        if any((lit>0 and assignment[abs(lit)]) or (lit<0 and not assignment[abs(lit)]) for lit in c):
            satisfied += 1
    return satisfied

def random_assignment(n):
    return {i: random.choice([False, True]) for i in range(1, n+1)}

def neighbors_flip(assignment):
    for i in assignment:
        new = assignment.copy(); new[i] = not new[i]
        yield new

def hill_climb(clauses, n, max_steps=1000):
    s = random_assignment(n)
    best = eval_assignment(clauses, s)
    for _ in range(max_steps):
        improved = False
        for nb in neighbors_flip(s):
            val = eval_assignment(clauses, nb)
            if val > best:
                s, best = nb, val
                improved = True
                break
        if not improved: break
    return s, best

def beam_search(clauses, n, width=3, max_steps=200):
    # population of assignments
    pool = [random_assignment(n) for _ in range(width)]
    for _ in range(max_steps):
        candidates = []
        for s in pool:
            candidates.append((eval_assignment(clauses,s), s))
            for nb in neighbors_flip(s):
                candidates.append((eval_assignment(clauses,nb), nb))
        candidates.sort(reverse=True, key=lambda x:x[0])
        pool = [c for _,c in candidates[:width]]
        if candidates[0][0] == len(clauses): break
    return pool[0][1], eval_assignment(clauses, pool[0])

def vnd(clauses, n, max_rounds=10):
    s = random_assignment(n)
    best = eval_assignment(clauses,s)
    neighborhoods = [neighbors_flip]
    for _ in range(max_rounds):
        improved = False
        for N in neighborhoods:
            for nb in N(s):
                val = eval_assignment(clauses, nb)
                if val > best:
                    s, best = nb, val
                    improved = True
                    break
            if improved: break
        if not improved: break
    return s, best

if __name__ == "__main__":
    random.seed(1)
    clauses = [(1,-3,4),(-2,3,-4),(1,-2,3),(-1,3,-4),(1,2,-3)]
    n = 4
    print("Hill-climb:", hill_climb(clauses,n))
    print("Beam:", beam_search(clauses,n,width=3))
    print("VND:", vnd(clauses,n))
