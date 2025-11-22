# mdp_grid_gbike.py
import numpy as np

# Value Iteration for 4x3 grid similar to Sutton & Barto example
def value_iteration(states, actions, P, R, gamma=0.99, theta=1e-6):
    V = {s:0.0 for s in states}
    while True:
        delta = 0
        for s in states:
            if not actions[s]: continue
            v = V[s]
            V[s] = max(sum(P(s,a,s2)*(R(s,a,s2) + gamma*V[s2]) for s2 in states) for a in actions[s])
            delta = max(delta, abs(v - V[s]))
        if delta < theta: break
    return V

# For Gbike: simplified policy iteration for small capacity (example)
def gbike_policy_iteration(max_bikes=5, gamma=0.9):
    # small scale example: states (i,j) 0..max_bikes
    states = [(i,j) for i in range(max_bikes+1) for j in range(max_bikes+1)]
    # actions: move a bikes from 1->2: -max_move..max_move
    actions = {s: list(range(-2,3)) for s in states}
    # dummy transition & reward functions (to be replaced by Poisson model)
    def P(s,a,s2): return 1.0 if s2==s else 0.0
    def R(s,a,s2): return -abs(a)*2  # cost per move
    # policy iteration
    pi = {s:0 for s in states}
    V = {s:0.0 for s in states}
    is_policy_stable = False
    while not is_policy_stable:
        # policy evaluation (simple iterative)
        for _ in range(100):
            for s in states:
                a = pi[s]
                V[s] = sum(P(s,a,s2)*(R(s,a,s2) + gamma*V[s2]) for s2 in states)
        is_policy_stable = True
        for s in states:
            old_a = pi[s]
            # greedy improvement
            best_a, best_v = old_a, -1e9
            for a in actions[s]:
                val = sum(P(s,a,s2)*(R(s,a,s2) + gamma*V[s2]) for s2 in states)
                if val > best_v:
                    best_v, best_a = val, a
            pi[s] = best_a
            if best_a != old_a: is_policy_stable = False
    return pi, V

if __name__ == "__main__":
    pi, V = gbike_policy_iteration()
    print("Sample policy entries:", list(pi.items())[:5])
