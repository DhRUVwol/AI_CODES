# plagiarism_a_star.py
import heapq
import numpy as np
import re
from difflib import SequenceMatcher

def tokenize_sentences(text):
    # simple sentence split by punctuation
    sents = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sents if s.strip()]

def edit_distance(a,b):
    # use ratio -> convert to a cost between 0..1, lower is better
    return 1 - SequenceMatcher(None, a, b).ratio()

def align(sents1, sents2, penalty=0.5):
    N, M = len(sents1), len(sents2)
    start = (0,0)
    pq = []
    heapq.heappush(pq, (0, 0, start, []))  # (f,g,(i,j),path)
    visited = {}
    while pq:
        f,g,(i,j),path = heapq.heappop(pq)
        if (i,j) in visited and visited[(i,j)] <= g: continue
        visited[(i,j)] = g
        if i==N and j==M:
            return path, g
        # align i and j
        if i < N and j < M:
            cost = edit_distance(sents1[i], sents2[j])
            heapq.heappush(pq, (g+cost, g+cost, (i+1,j+1), path+[(i,j,'align')]))
        if i < N:
            heapq.heappush(pq, (g+penalty, g+penalty, (i+1,j), path+[(i,None,'skip1')]))
        if j < M:
            heapq.heappush(pq, (g+penalty, g+penalty, (i,j+1), path+[(None,j,'skip2')]))
    return None, float('inf')

if __name__ == "__main__":
    doc1 = "This is a test. It has some sentences. Some are similar."
    doc2 = "This is a test. It has some changes. Some are similar."
    s1 = tokenize_sentences(doc1)
    s2 = tokenize_sentences(doc2)
    path, cost = align(s1,s2)
    print("Total edit-cost:", cost)
    print("Alignment:")
    for step in path:
        print(step)
