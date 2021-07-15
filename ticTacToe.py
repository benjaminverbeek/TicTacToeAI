# Simple implementation of n x n tic-tac-toe
# Addition: a simple reinforcement-learning bot.
# Benjamin Verbeek, 2021-07-15, Sala, Sweden

import random
import matplotlib.pyplot as plt

class Board:
    """Define Tic-Tac-Toe board
    Set nums = False to hide numbers on playing board.
    Set disp = False to hide prints during play
    """
    def __init__(self, sz, nums = True, disp = True) -> None:
        self.sz = sz
        self.turn = 0
        self.decode = {0:" ", 1:"X", 2:"O"}
        self.encode = {" ":0, "X":1, "O":2}
        self.markers = ['X','O']
        self.state = [" "]*(sz**2)
        self.nums = nums
        self.disp = disp
        
    def __str__(self) -> str:
        sz = self.sz
        out = ""
        for i in range(sz**2):
            if i != 0 and i % sz == 0:
                out = out[:-1] + "\n-" + "+-"*(sz-1) + "\n"
            if self.nums == True and self.state[i] in self.markers:
                out += str(self.state[i]) + "|"
            elif self.nums == True:
                out += str(i+1) + "|"
            else:
                out += str(self.state[i]) + "|"
        return out[:-1] + "\n"

    def move(self, pos) -> None:
        """Occupies a spot."""
        assert(pos in list(range(1,self.sz**2+1)))
        pos = pos-1 # list offset
        assert(self.state[pos] not in self.markers)  # if spot is taken, raise error
        self.state[pos] = self.decode[self.turn % 2 + 1] # automatic turn calculator
        self.turn += 1
        if self.disp:
            print(self)
    
    def win(self) -> bool:
        """Checks if win-conditions are met."""
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
    b = Board(sz, nums=False)
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
'''
ticTacToe()
while input("Play again? Type 'y' for yes: ") == "y":
    ticTacToe()
'''

positions = {}  # THE TRAINING! NOTE!
progress = [0]   # keeps track of wins (1), losses (-1), and draws (0)

# rotational symmetry not taken into account
# the real value is stored in variable "positions". NOTE: Careful not to clear it
# NOTE: must clear "moves" though
def NNticTacToe(playAs='X', nums=True, disp=True, manual=True):
    sz = 3  # board dimension
    reinforceWin = 2    # how much should winning moves be boosted?
    reinforceDraw = 1   # draw?
    reinforceLoss = -2  # loss?
    
    b = Board(sz, nums=nums, disp=disp)
    if disp: print("Welcome to NN Tic-Tac-Toe!")
    
    moves = []      # Just needed temporary
    # when finding new position (that is, string of encoded position),
    # add 2 of each available position to the list
    
    # must keep track of played moves.

    while b.turn < 9:   # full board
        player = b.decode[b.turn%2 + 1]
        if disp: print(f"{player}'s turn")

        if player == playAs:
            # NN plays
            state = b.state.copy()
            if disp: print(state)
            if str(state) not in positions or positions[str(state)] == []: # if all cases deleted, just retry
                # adds two copies of each legal move (legal moves are empty positions of state)
                # i+1 due to offset in enumeration vs list index
                positions[str(state)] = [i+1 for i, x in enumerate(state) if x not in b.markers] * 2
            # Select a random value from positions[state]
            choice = random.choice(positions[str(state)])
            #print(choice)
            # Store state & played move for evaluation
            moves.append((str(state), choice))
            b.move(choice)
        elif manual == True:
            # human plays
            m = input("Enter a position to place: ")
            if m == 'q':
                break
            try:
                b.move(int(m))
            except:
                print("Invalid move, try again!")
                continue
        else:   
            legal = [i+1 for i, x in enumerate(b.state.copy()) if x not in b.markers]    # legal moves in current positon
            choice = random.choice(legal)   # random legal move
            b.move(choice)

        if b.win() == True: # check win condition
            if disp: print(f"{player} won!")
            winner = player
            break
        elif b.turn == 9:
            if disp: print("It's a draw.")
            winner = None

    #print(moves)
    #print()
    #print(positions)

    if disp: print("REINFORCEMENT")
    # REINFORCEMENT:
    if winner == playAs:
        progress[-1] += 1
        progress.append(progress[-1])
        # NN won! Reinforce the moves made by increasing odds of picking them
        for k, v in moves:
            positions[k] += [v]*reinforceWin
    elif winner == None:
        progress[-1] += 1
        progress.append(progress[-1])
        # it was a draw
        for k, v in moves:
            positions[k] += [v]*reinforceDraw
    else:
        progress[-1] += -1
        progress.append(progress[-1])
        # NN lost.
        for k, v in moves:
            for _ in range(abs(reinforceLoss)):
                try:
                    positions[k].remove(v)
                except: # all removed
                    break


    if disp: print("Thank you for playing!")


def trainNN(nIter, disp=False, manual=False):
    print(f"Running {nIter} iterations...")
    for i in range(nIter):
        #print(f"Iteration no: {i}")
        NNticTacToe(disp=disp, manual=manual)
    print("Done.")

nIter = 100_000
xOffset = 10_000
trainNN(nIter)

perfect = [i for i in range(len(progress[:-1]))]
perfectOffset = [i+xOffset for i in range(len(progress[:-1]))]
plt.plot(perfect, progress[:-1], label = "NN progress")
plt.plot(perfect, perfect, label = "100% winrate")
plt.plot(perfectOffset, perfect, label = "100% winrate (x offset 5000)")
plt.plot(perfect, [0]*len(progress[:-1]), label = "50% winrate/draws")
plt.ylabel('wins')
plt.title(f'total wins over {nIter} iterations (win: +1, draw: 0, loss: -1)')
plt.legend()
plt.show()
print(len(positions))

NNticTacToe()
while input("Continue? y/n: ") != 'n':
    NNticTacToe()


# WORKING!! needs to practise