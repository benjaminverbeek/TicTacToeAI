# Simple implementation of 3x3 tic-tac-toe

class Board:
    """Define Tic-Tac-Toe board"""
    def __init__(self, sz, disp = True) -> None:
        self.sz = sz
        self.turn = 0
        self.decode = {0:" ", 1:"X", 2:"O"}
        self.encode = {" ":0, "X":1, "O":2}
        self.markers = ['X','O']
        if disp == True:
            self.state = list(range(1, sz**2 + 1))
        else:    
            self.state = [" "]*(sz**2)
        self.disp = disp
        
    def __str__(self) -> str:
        sz = self.sz
        out = ""
        for i in range(sz**2):
            if i != 0 and i % sz == 0:
                out = out[:-1] + "\n-" + "+-"*(sz-1) + "\n"
            out += str(self.state[i]) + "|"
        return out[:-1] + "\n"

    def move(self, pos) -> None:
        assert(pos in list(range(1,self.sz**2+1)))
        pos = pos-1 # list offset
        assert(self.state[pos] not in self.markers)  # if spot is taken, raise error
        self.state[pos] = self.decode[self.turn % 2 + 1] # automatic turn calculator
        self.turn += 1
        print(self)
    
    def win(self) -> bool:
        state = self.state
        sz = self.sz
        # Horizontal
        for row in range(sz):
            first = state[sz*row] # first element in row
            if first not in self.markers:
                continue
            for col in range(sz):   # column
                if state[sz*row + col] != first:
                    same = False
                    break
                else:
                    same = True
            if same:
                return True

        # Vertical
        for col in range(sz):
            first = state[col] # first element in col
            if first not in self.markers:
                continue
            for row in range(sz):   # rows
                if state[sz*row + col] != first:
                    same = False
                    break
                else:
                    same = True
            if same:
                return True

        # Diagonal \
        first = state[0] # first element on diag
        for diag in range(sz):
            row, col = diag, diag
            if first not in self.markers:
                same = False
                break
            if state[sz*row + col] != first:
                same = False
                break
            else:
                same = True
        if same:
            return True

        # Diagonal /
        first = state[sz-1] # first element in diag
        for diag in range(sz):
            row, col = diag, diag
            if first not in self.markers:
                same = False
                break
            if state[sz*(row+1) - (col+1)] != first:
                same = False
                break
            else:
                same = True
        if same:
            return True
        return False    # no winner found

def ticTacToe():
    sz = 3  # board dimension
    b = Board(sz, disp=True)
    print("Welcome to Tic-Tac-Toe!")
    print(b)
    print("Encoding is 1-9 top-left to bottom right. Quit anytime by entering 'q'.")

    while b.turn < 9:   # full board
        print(f"{b.decode[b.turn%2 + 1]}'s turn")
        m = input("Enter a position to place: ")
        if m == 'q':
            break
        try:
            b.move(int(m))
        except:
            print("Invalid move, try again!")
            continue
        if b.win() == True:
            print(f"{b.decode[(b.turn-1)%2 + 1]} won!")
            break
        elif b.turn == 9:
            print("It's a draw.")
    print("Thank you for playing!")


# TESTS
ticTacToe()
while input("Play again? Type 'y' for yes: ") == "y":
    ticTacToe()
