import random

class Puzzle:

    def __init__(self, board=list('12345678X'), x=8):
        self.board = board
        self.x = x

    def board_swap(self, y):
        self.board[self.x], self.board[y] = self.board[y], self.board[self.x]
        self.x = y

    def clone(self):
        board = [c for c in self.board]
        return Puzzle(board=board, x=int(self.x))

    def move_up(self):
        self.board_swap(self.x + 3)
        return self

    def move_down(self):
        self.board_swap(self.x - 3)
        return self

    def move_right(self):
        self.board_swap(self.x - 1)
        return self

    def move_left(self):
        self.board_swap(self.x + 1)
        return self

    def get_possibilities(self):
        possibilities = []
        if self.x > 0 and self.x % 3 != 0: # Move right
            possibilities.append(self.clone().move_right())
        if (self.x+1) % 3 != 0: # Move left
            possibilities.append(self.clone().move_left())
        if (self.x+3) <= 8: # Move up
            possibilities.append(self.clone().move_up())
        if (self.x-3) >= 0: # Move down
            possibilities.append(self.clone().move_down())
        return possibilities

    def hash_code(self):
        str = ""
        for i in self.board:
            str += i
        return str

    def __str__(self):
        str = ""
        for i in range(0, len(self.board), 3):
            str += ("%s %s %s\n" % (self.board[i], self.board[i+1], self.board[i+2]))
        return str[0:-1]

    def is_done(self):
        for i in range(1, 9):
            if str(i) != self.board[i-1]: return False
        return True

    def mix(self, times):
        while times > 0:
            f = random.randint(0, 3)
            if f == 0 and self.x > 0 and self.x % 3 != 0: # Move right
                self.move_right()
                times -= 1
            if f == 1 and (self.x+1) % 3 != 0: # Move left
                self.move_left()
                times -= 1
            if f == 2 and (self.x+3) <= 8: # Move up
                self.move_up()
                times -= 1
            if f == 3 and (self.x-3) >= 0: # Move down
                self.move_down()
                times -= 1


def dfs(puzzle, visited, path):
    visited.add(puzzle.hash_code())
    path.append(puzzle)
    if puzzle.is_done():
        return True
    possibilities = puzzle.get_possibilities()
    for poss in possibilities:
        if not poss.hash_code() in visited:
            d = dfs(poss, visited, path)
            if d: return True
    path.pop()
    return False

def solve(puzzle):
    path = []
    visited = set()
    dfs(puzzle, visited, path)
    return path

puzzle = Puzzle()
puzzle.mix(times=500)
print puzzle

path = solve(puzzle)
if len(path) == 0:
    print 'Impossible to solve!'
else:
    print 'Solution:'
    for p in path:
        print "%s\n" % p
