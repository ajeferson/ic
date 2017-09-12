class State:

    def __init__(self, left = [0, 0], right = [3, 3], side = 'right', initial = None):
        self.left = left
        self.right = right
        self.side = side
        if initial is None:
            self.initial = self.side
        else:
            self.initial = initial

    def is_left(self):
        return self.side == 'left'

    def is_right(self):
        return not self.is_left()

    def get_possibilities(self):

        result = []

        if self.is_right():
            a = self.right
            b = self.left
            s = 'left'
        else:
            a = self.left
            b = self.right
            s = 'right'

        if a[0] > 0:
            result.append([b[0]+1, b[1]])
            result.append([a[0]-1, a[1]])
        if a[0] > 1:
            result.append([b[0]+2, b[1]])
            result.append([a[0]-2, a[1]])
        if a[1] > 0:
            result.append([b[0], b[1]+1])
            result.append([a[0], a[1]-1])
        if a[1] > 1:
            result.append([b[0], b[1]+2])
            result.append([a[0], a[1]-2])
        if a[0] > 0 and a[1] > 0:
            result.append([b[0]+1, b[1]+1])
            result.append([a[0]-1, a[1]-1])

        possibilities = []
        for i in range(0, len(result), 2):
            if self.is_right():
                possibilities.append(State(left=result[i], right=result[i+1], side=s, initial=self.initial))
            else:
                possibilities.append(State(left=result[i+1], right=result[i], side=s, initial=self.initial))

        return possibilities

    def is_done(self):
        return self.side != self.initial and \
               ((self.left[0] == 3 and self.left[1] == 3) or \
               (self.right[0] == 3 and self.right[1] == 3))

    def is_game_over(self):
        return (self.left[1] > 0 and self.left[0] > self.left[1]) or (self.right[1] > 0 and self.right[0] > self.right[1])

    def to_hash(self):
        return "%d%d%d%d%s" % (self.left[0], self.left[1], self.right[0], self.right[1], self.side[0])

    def __str__(self):
        return "Left: %s Right: %s Side: %s" % (str(self.left), str(self.right), self.side)


def dfs(state, visited, path):

    visited.add(state.to_hash())
    if state.is_game_over():
        return False

    path.append(state)
    if state.is_done():
        return True

    possibilities = state.get_possibilities()
    for poss in possibilities:
        if not poss.to_hash() in visited:
            d = dfs(poss, visited, path)
            if d:
                return True

    path.pop()
    return False


def solve(state):
    path = []
    visited = set()
    dfs(state, visited, path)
    return path

state = State()
path = solve(state)
if len(path) == 0:
    print "Imposssible to solve!"
else:
    for p in path:
        print p
