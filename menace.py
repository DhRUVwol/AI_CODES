# menace.py
import random, collections

class MENACE:
    def __init__(self):
        self.matchboxes = collections.defaultdict(lambda: collections.Counter())
    def encode(self, board):
        # board: 9-length list with 'X','O','.'; encode canonical string
        return ''.join(board)
    def add_matchbox(self, state, moves):
        # initialize beads
        for m in moves:
            self.matchboxes[state][m] = self.matchboxes[state].get(m,1)
    def choose(self, state):
        c = self.matchboxes[state]
        total = sum(c.values())
        r = random.randint(1,total)
        s=0
        for move, count in c.items():
            s += count
            if r <= s: return move
    def update(self, history, result):
        # result: 'win','draw','loss'
        for state, move in history:
            if result == 'win':
                self.matchboxes[state][move] += 3
            elif result == 'draw':
                self.matchboxes[state][move] += 1
            else:
                self.matchboxes[state][move] = max(1, self.matchboxes[state][move]-1)

# tiny demo: not full tic-tac-toe game here; integrate into a game engine to train
if __name__ == "__main__":
    m = MENACE()
    s = "........."
    m.add_matchbox(s, list(range(9)))
    print("Beads for start:", m.matchboxes[s])
    choice = m.choose(s)
    print("Chosen move:", choice)
