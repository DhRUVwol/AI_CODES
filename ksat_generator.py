# ksat_generator.py
import random

def generate_k_sat(k, m, n, allow_neg=True):
    clauses = []
    vars_list = list(range(1, n+1))
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            v = random.choice(vars_list)
            sign = -1 if allow_neg and random.random() < 0.5 else 1
            lit = sign * v
            # avoid contradictory lit in same clause like x and -x, and duplicates
            if -lit in clause: continue
            clause.add(lit)
        clauses.append(tuple(clause))
    return clauses

def print_cnf(clauses):
    for c in clauses:
        print("(" + " OR ".join([f"{('~' if lit<0 else '')}x{abs(lit)}" for lit in c]) + ")")

if __name__ == "__main__":
    random.seed(0)
    clauses = generate_k_sat(3, 5, 4)
    print_cnf(clauses)
