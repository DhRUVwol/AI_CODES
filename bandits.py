# bandits.py
import numpy as np, random, matplotlib.pyplot as plt

def run_epsilon_greedy(arms, eps=0.1, steps=1000):
    Q = np.zeros(len(arms)); N = np.zeros(len(arms))
    rewards = []
    for t in range(steps):
        if random.random() < eps:
            a = random.randrange(len(arms))
        else:
            a = np.argmax(Q)
        r = arms[a]()  # arms are callables
        N[a] += 1
        Q[a] += (r - Q[a]) / N[a]
        rewards.append(r)
    return rewards, Q

def run_nonstationary(arms_mu, eps=0.1, alpha=0.1, steps=1000):
    k = len(arms_mu)
    Q = np.zeros(k)
    mu = np.array(arms_mu)
    rewards = []
    for t in range(steps):
        if random.random() < eps:
            a = random.randrange(k)
        else:
            a = np.argmax(Q)
        r = np.random.normal(mu[a],1)
        Q[a] += alpha*(r - Q[a])
        mu += np.random.normal(0,0.01,k)  # drift
        rewards.append(r)
    return rewards, Q

if __name__ == "__main__":
    # stationary two-armed bandit example
    arm0 = lambda: np.random.binomial(1, 0.3)
    arm1 = lambda: np.random.binomial(1, 0.7)
    rewards, Q = run_epsilon_greedy([arm0, arm1], eps=0.1, steps=1000)
    print("Estimated Q:", Q)
    # nonstationary 10-armed
    rewards_ns, Qns = run_nonstationary(np.zeros(10), eps=0.1, alpha=0.1, steps=5000)
    print("Final Q (nonstationary):", Qns)
