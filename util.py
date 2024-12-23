from collections import defaultdict

e = enumerate


def getlines(day):
    with open(f"data/day{day}.txt") as f:
        return [line.strip() for line in f.readlines() if len(line) > 1]


def getblankseparated(day):
    with open(f"data/day{day}.txt") as f:
        return f.read().split("\n\n")


def tokenedlines(day, collapse=True, sep=" ", tuplify=True):
    lines = getlines(day)
    ret = []
    for line in lines:
        parts = [p for p in line.strip().split(sep) if not (collapse and p == "")]
        parsed_parts = []
        for part in parts:
            try:
                parsed_parts.append(int(part))
            except:
                try:
                    parsed_parts.append(float(part))
                except:
                    parsed_parts.append(part)
        ret.append(parsed_parts)
    return tuple(ret) if tuplify else ret 


def as_ints(arr):
    return tuple(int(x) for x in arr)


def in_range(i, j, max_i, max_j):
    return i >= 0 and j >= 0 and i < max_i and j < max_j

def in_range2(tuple, grid):
    return in_range(tuple[0], tuple[1], len(grid[0]), len(grid))

class Tuple:
    @staticmethod
    def in_range(tuple, grid):
        return in_range(tuple[0], tuple[1], len(grid[0]), len(grid))
    
    @staticmethod
    def negate(tuple):
        return Tuple.multiply(tuple, -1)
    
    @staticmethod
    def add(t1, t2):
        return tuple([a + b for a, b in zip(t1, t2)])
    
    @staticmethod
    def subtract(t1, t2):
        return tuple([a - b for a, b in zip(t1, t2)])
    
    @staticmethod
    def multiply(tup, scalar):
        return tuple([x * scalar for x in tup])
    
    @staticmethod
    def idivide(tup, scalar):
        return tuple([x // scalar for x in tup])


def neighbors4(i, j, max_i, max_j=None):
    return neighbors_helper(
        max_i, max_j, [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
    )


def neighbors8(i, j, max_i, max_j=None):
    return neighbors_helper(
        max_i,
        max_j,
        [
            (i - 1, j),
            (i + 1, j),
            (i, j - 1),
            (i, j + 1),
            (i - 1, j - 1),
            (i - 1, j + 1),
            (i + 1, j - 1),
            (i + 1, j + 1),
        ],
    )


def neighbors_helper(max_i, max_j, candidates):
    if max_j is None and isinstance(max_i, list):
        max_j = len(max_i[0])
        max_i = len(max_i)
    return [(i, j) for i, j in candidates if in_range(i, j, max_i, max_j)]


def printgrid(points):
    maxX = max(p[0] for p in points)
    minX = min(p[0] for p in points)
    maxY = max(p[1] for p in points)
    minY = min(p[1] for p in points)
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            if (x, y) in points:
                print("*", end="")
            else:
                print(" ", end="")
        print("")

def printgrid2(points):
    maxX = max(p[0] for p in points)
    minX = min(p[0] for p in points)
    maxY = max(p[1] for p in points)
    minY = min(p[1] for p in points)
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            if (x, y) in points:
                print(points[(x, y)], end="")
            else:
                print(" ", end="")
        print("")

def factorize(num):
    primefact = defaultdict(int)
    while num % 2 == 0:
        num /= 2
        primefact[2] += 1
    i = 3
    while num >= i:
        if num % i == 0:
            primefact[i] += 1
            num /= i
        else:
            i += 2
    return primefact


def lcm(nums):
    res = {}
    for num in nums:
        for prime, exp in factorize(num).items():
            res[prime] = max(exp, res.get(prime, 0))
    x = 1
    for p, e in res.items():
        x *= pow(p, e)
    return int(x + 0.01)
