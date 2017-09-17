import random
import math

class Puzzle:

    def __init__(self, **kwargs):
        if 'board' in kwargs:
            self.board, self.n, self.cx, self.cy = kwargs['board'], kwargs['n'], kwargs['cx'], kwargs['cy']
        elif 'str' in kwargs:
            self.board, self.n, self.cx, self.cy = self.str_to_matrix(kwargs['str'], kwargs['blank'])
        else:
            pass # Exception
        self.parent = None
        self.g = 0
        self.h = 0

    def str_to_matrix(self, s, c):
        n = int(math.sqrt(len(s)))
        matrix = [[s[i] for i in range(k, k+n)] for k in range(0, len(s), n)]
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == c: return (matrix, n, i, j)
        return (matrix, n, -1, -1)

    def blank_swap(self, x, y):
        aux = self.board[self.cx][self.cy]
        self.board[self.cx][self.cy] = self.board[x][y]
        self.board[x][y] = aux
        self.cx, self.cy = x, y

    def clone(self):
        board = [[c for c in row] for row in self.board]
        return Puzzle(board=board, n=self.n, cx=self.cx, cy=self.cy)

    def move_up(self):
        self.blank_swap(self.cx + 1, self.cy)
        return self

    def move_down(self):
        self.blank_swap(self.cx - 1, self.cy)
        return self

    def move_right(self):
        self.blank_swap(self.cx, self.cy - 1)
        return self

    def move_left(self):
        self.blank_swap(self.cx, self.cy + 1)
        return self

    def get_children(self):
        possibilities = []
        if self.cy > 0: # Move right
            child = self.clone().move_right()
            child.parent = self
            possibilities.append(child)
        if (self.cy+1) < self.n: # Move left
            child = self.clone().move_left()
            child.parent = self
            possibilities.append(child)
        if (self.cx+1) < self.n: # Move up
            child = self.clone().move_up()
            child.parent = self
            possibilities.append(child)
        if self.cx > 0: # Move down
            child = self.clone().move_down()
            child.parent = self
            possibilities.append(child)
        return possibilities

    def hash_code(self):
        str = ""
        for row in self.board:
            for c in row:
                str += c
        return str

    def __str__(self):
        str = ''
        for i in range(self.n):
            str += ("%s %s %s\n" % (self.board[i][0], self.board[i][1], self.board[i][2]))
        return str[0:-1]

    def __gt__(self, other):
        return self.f() > other.f()

    def positions_map(self):
        positions = {}
        for i in range(self.n):
            for j in range(self.n):
                positions[self.board[i][j]] = (i, j)
        return positions

    """
    Manhattan Distance
    """
    def distance_to(self, positions):
        dist = 0
        for i in range(self.n):
            for j in range(self.n):
                if i != self.cx or j != self.cy:
                    x, y = positions[self.board[i][j]]
                    dist += abs(i - x) + abs(j - y)
        return dist

    def is_equal(self, other):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

    def mix(self, times):
        while times > 0:
            f = random.randint(0, 3)
            if f == 0 and self.cy > 0: # Move right
                self.move_right()
                times -= 1
            if f == 1 and (self.cy+1) < self.n: # Move left
                self.move_left()
                times -= 1
            if f == 2 and (self.cx+1) < self.n: # Move up
                self.move_up()
                times -= 1
            if f == 3 and self.cx > 0: # Move down
                self.move_down()
                times -= 1

    def f(self):
        return self.g + self.h

    def path_to(self, goal):

        positions = goal.positions_map()
        self.h = self.distance_to(positions)
        open_list = [self]
        closed_set = set()
        found = False
        last = None

        while not found and len(open_list) > 0:

            curr = open_list.pop(len(open_list) - 1)
            closed_set.add(curr.hash_code())

            if curr.is_equal(goal):
                found = True
                last = curr

            else:

                children = curr.get_children()

                # Update g and h value for the children
                for child in children:
                    child.g = curr.g + 1
                    child.h = child.distance_to(positions)
                    for opened in open_list: # Check on open list
                        if child.is_equal(opened) and opened.g > child.g: # If on the open list
                            opened.g = child.g
                            opened.parent = curr
                    open_list.append(child)

                # Sort the open list
                open_list.sort(reverse=True)

        # Building the path
        if last is None:
            return []

        s = last.g
        path = [1] * (s+1)
        for i in range(s, -1, -1):
            path[i] = last
            last = last.parent

        return path

goal = Puzzle(str='12345678 ', blank=' ')
initial = Puzzle(str='12345678 ', blank=' ')
initial.mix(times=500)

print 'Input:'
print initial

print '\n\nSolving...'
path = initial.path_to(goal)

if len(path) == 0:
    print 'Impossible to solve!'
else:
    print '\n\nSolution:'
    ls = []
    for p in path:
        ls.append(p.__str__())
    print '\n-----\n'.join(ls)
