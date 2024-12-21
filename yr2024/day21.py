from collections import defaultdict
from functools import cache
import itertools
from util import tokenedlines, getlines

day = "21"
# day = "ex"

data = getlines(day)

finalgrid = tuple(["789", "456", "123", " 0A"])
directiongrid = tuple([" ^A", "<v>"])
DIRS = {
    '^': (-1, 0),
    'v': (1, 0),
    '<': (0, -1),
    '>': (0, 1),
}

def get_pos(grid, ch):
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == ch:
                return (y, x)
    print(f"Trying to find {ch} in {grid}")

MEMO = {
    'A': {
        'A': ['A'],
        '^': ['<A'],
        'v': ['<vA'],
        '<': ['v<<A'],
        '>': ['vA'],
    },
    '^': {
        'A': ['>A'],
        '^': ['A'],
        'v': ['vA'],
        '<': ['v<A'],
        '>': ['v>A'],
    },
    'v': {
        'A': ['^>A'],
        '^': ['^A'],
        'v': ['A'],
        '<': ['<A'],
        '>': ['>A'],
    },
    '<': {
        'A': ['>>^A'],
        '^': ['>^A'],
        'v': ['>A'],
        '<': ['A'],
        '>': ['>>A'],
    },
    '>': {
        'A': ['^A'],
        '^': ['<^A'],
        'v': ['<A'],
        '<': ['<<A'],
        '>': ['A'],
    }
}

def run(path):
    res = ""
    pos = get_pos(directiongrid, 'A')
    for c in path:
        if directiongrid[pos[0]][pos[1]] == ' ':
            return None
        elif c == 'A':
            res += directiongrid[pos[0]][pos[1]]
        else:
            pos = (pos[0] + DIRS[c][0], pos[1] + DIRS[c][1])
    return res


@cache
def instruct(target_grid, pattern, perm=[0,1,2,3], src='A'):
    if target_grid == directiongrid:
        # Use a hard-coded path on the direction grid
        ret = []
        for c in pattern:
            ret.append(MEMO[src][c][0])
            src = c
        ret = "".join(ret)
        if run(ret) != pattern:
            print("WTF", pattern, src, ret)
        return ret
    y, x = get_pos(target_grid, src)
    steps = []
    valid = True
    for ch in pattern:
        newy, newx = get_pos(target_grid, ch)
        for dir in perm:
            if dir == 0:
                while y > newy:
                    steps.append('^')
                    y -= 1
                    if target_grid[y][x] == ' ':
                        valid = False
            elif dir == 1:
                while y < newy:
                    steps.append('v')
                    y += 1
                    if target_grid[y][x] == ' ':
                        valid = False
            elif dir == 2:
                while x > newx:
                    steps.append('<')
                    x -= 1
                    if target_grid[y][x] == ' ':
                        valid = False
            elif dir == 3:
                while x < newx: 
                    steps.append('>')
                    x += 1
                    if target_grid[y][x] == ' ':
                        valid = False
        steps.append('A')
    if not valid:
        return None
    return "".join(steps)

def mysplit(pattern):
    ret = []
    current = ""
    for ch in pattern:
        if ch != 'A' and current.endswith('A'):
            ret.append(current)
            current = ""
        current += ch
    if current != "":
        if not current.endswith('A'):
            print("WTF", pattern)
        ret.append(current)
    return ret

@cache
def expand_patterns(grid, patterns):
    ret = defaultdict(int)
    for pattern, count in patterns:
        result = instruct(grid, pattern)
        if result is None:
            return None
        for token in mysplit(result):
            ret[token] += count
    return frozenset(ret.items())

def mylen(pattern):
    return sum(len(p) * c for p, c in pattern)

@cache
def get_length_for_single_pattern(pattern, steps):
    patterns = frozenset([(pattern, 1)])
    best = None
    for perm in itertools.permutations(range(4)):
        newpatterns = expand_patterns(directiongrid, patterns)
        if newpatterns is None:
            continue
        score = get_length(newpatterns, steps - 1)
        if best is None or best > score:
            best = score
    return best
    
@cache
def get_length(patterns, steps):
    if steps == 0:
        return mylen(patterns)
    score = 0
    for p, c in patterns:
        n = get_length_for_single_pattern(p, steps)
        if n is None:
            score = None
            break
        score += n * c
    return score

def solve(pattern, count):
    sofars = ['']
    pos = 'A'
    for ch in pattern:
        nexts = set([])
        for perm in itertools.permutations(range(4)):
            path = instruct(finalgrid, ch, perm=perm, src=pos)
            if path is not None:
                nexts = nexts.union([sofar + path for sofar in sofars])
        sofars = nexts
        pos = ch
        
    best = None
    possibilities = {frozenset([(p, 1)]) for p in sofars}
    for p in possibilities:
        s = get_length(p, count)
        if best is None or best > s:
            best = s

    return best    

for depth in (2, 25):
    score = 0
    for pattern in data:
        a = solve(pattern, depth)
        # b = multinstruct(pattern, depth)
        print(pattern, a * int(pattern[:3]))
        score += a * int(pattern[:3])
    print(score)

