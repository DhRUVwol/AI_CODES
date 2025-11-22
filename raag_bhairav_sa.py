# raag_bhairav_sa.py
import random, math

NOTES = {'S':60,'r':61,'G':64,'M':65,'P':67,'d':68,'N':71,"S'":72}
scale = list(NOTES.keys())
durations = [0.25,0.5,1.0]

def random_melody(L=16):
    return [(random.choice(scale), random.choice(durations)) for _ in range(L)]

def fitness(mel):
    score = 0
    motifs = [['S','r','G'], ['r','G','M'], ['d','N',"S'"]]
    notes = [n for n,_ in mel]
    # motif rewards
    for motif in motifs:
        for i in range(len(notes)-len(motif)+1):
            if notes[i:i+len(motif)] == motif:
                score += 10
    # start/end
    if notes[0] == 'S': score += 5
    if notes[-1] == "S'": score += 5
    # penalties
    for i in range(1,len(notes)):
        if abs(NOTES[notes[i]] - NOTES[notes[i-1]]) > 7: score -= 3
        if notes[i] == notes[i-1]: score -= 1
    # emphasis notes
    for n in notes:
        if n in ('S','r','G','d'): score += 0.5
    return score

def neighbor(m):
    idx = random.randrange(len(m))
    if random.random()<0.5:
        # mutate note
        m2 = m.copy(); m2[idx] = (random.choice(scale), m2[idx][1])
    else:
        m2 = m.copy(); m2[idx] = (m2[idx][0], random.choice(durations))
    return m2

def sa(L=16, T0=100.0, alpha=0.99, Tmin=0.1):
    cur = random_melody(L); curf = fitness(cur)
    best, bestf = cur, curf
    T = T0
    while T > Tmin:
        cand = neighbor(cur)
        cf = fitness(cand)
        if cf > curf or random.random() < math.exp((cf-curf)/T):
            cur, curf = cand, cf
            if cf > bestf: best, bestf = cand, cf
        T *= alpha
    return best, bestf

if __name__ == "__main__":
    melody, score = sa()
    print("Score:", score)
    print("Melody (note,duration):")
    print(melody)
