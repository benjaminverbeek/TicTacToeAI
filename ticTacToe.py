# Simple implementation of 3x3 tic-tac-toe
sz = 3 # board dimension

class Board:
    """Define Tic-Tac-Toe board"""
    def __init__(self, sz) -> None:
        self.sz = sz
        self.turn = 1
        self.decode = {0:" ", 1:"X", 2:"O"}
        self.state = [0]*(sz**2)
        

    def __str__(self) -> str:
        sz = self.sz
        decode = self.decode
        out = ""
        for i in range(sz**2):
            if i != 0 and i % sz == 0:
                out = out[:-1] + "\n-" + "+-"*(sz-1) + "\n"
            out += decode[self.state[i]] + "|"
        return out[:-1] + "\n"

    def move(self, pos) -> None:
        pos = pos-1 # list offset
        self.state[pos] = (self.turn-1)%2 + 1
        self.turn += 1
        print(self)
            
            

# TESTS
b = Board(sz)
print(b)
b.move(1)
b.move(2)
