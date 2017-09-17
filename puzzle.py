import random
import math

class NPuzzle:

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
        return NPuzzle(board=board, n=self.n, cx=self.cx, cy=self.cy)

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
        children = []
        if self.cy > 0: # Move right
            child = self.clone().move_right()
            children.append(child)
        if (self.cy+1) < self.n: # Move left
            child = self.clone().move_left()
            children.append(child)
        if (self.cx+1) < self.n: # Move up
            child = self.clone().move_up()
            children.append(child)
        if self.cx > 0: # Move down
            child = self.clone().move_down()
            children.append(child)
        return children

    def hash_code(self):
        str = ""
        for row in self.board:
            for c in row:
                str += c
        return str

    def __str__(self):
        str = ''
        for i in range(self.n):
            str += ' '.join(self.board[i])
            str += '\n'
        return str[0:-1]

    def __eq__(self, other):
        for i in range(self.n):
            for j in range(self.n):
                if self.board[i][j] != other.board[i][j]:
                    return False
        return True

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
        closed_list = []
        found = False
        last = None

        while not found and len(open_list) > 0:

            # Get the lowest from the open list
            min_index = 0
            for i in range(0, len(open_list)):
                if open_list[i].f() < open_list[min_index].f():
                    min_index = i
            curr = open_list.pop(min_index)

            # Found the solution
            if curr == goal:
                found = True
                last = curr

            else:

                # Get sucessor nodes
                children = curr.get_children()

                for child in children:

                    child.g = curr.g + 1

                    # Check opened list
                    open_index = -2
                    for i in range(len(open_list)): # Check on open list
                        opened = open_list[i]
                        if child == opened: # If on the open list
                            if opened.g <= child.g: # Worse
                                open_index = -1
                                break
                            else: # Better path found
                                open_index = i
                                break
                    if open_index == -1: # On open list and worse
                        continue

                    # Check closed list
                    close_index = -2
                    for i in range(len(closed_list)):
                        closed = closed_list[i];
                        if child == closed: # If on the closes list
                            if closed.g <= child.g: # Worse
                                close_index = -1
                                break
                            else:
                                close_index = i
                                break
                    if close_index == -1: # On closed list and worse
                        continue


                    # Remove from open list
                    if open_index >= 0:
                        open_list.pop(open_index)

                    # Remove from closed list
                    if close_index >= 0:
                        closed_list.pop(close_index)

                    # Apply heuristic function
                    child.h = child.distance_to(positions)
                    child.parent = curr

                    # Add to open list
                    open_list.append(child)

            closed_list.append(curr)

        # Building the path
        if last is None:
            return []

        s = last.g
        path = [1] * (s+1)
        for i in range(s, -1, -1):
            path[i] = last
            last = last.parent

        return path




initial = NPuzzle(str='ABCDEFGH ', blank=' ')
goal = initial.clone()
initial.mix(times=75)

print 'Initial State:'
print initial

print '\nGoal:'
print goal

print '\nSolving...'
path = initial.path_to(goal)

if len(path) == 0:
    print '\nImpossible to solve!'
else:
    print '\nSolution:'
    ls = []
    for p in path:
        ls.append(p.__str__())
    print '\n-----\n'.join(ls)
