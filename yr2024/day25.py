from util import getblankseparated, tokenedlines, getlines, Tuple

day = "25"
# day = "ex"

data = getblankseparated(day)

def parse_pattern(grid):
    heights = []
    for col in range(len(grid[0])):
        height = 0
        for row in grid:
            if row[col] != '#':
                heights.append(height - 1)
                break
            height += 1
    return heights

def parse_key_or_lock(grid):
    grid = grid.split("\n")
    if grid[0][0] == '#':
        return ('LOCK', parse_pattern(grid))
    else:
        return ('KEY', parse_pattern(grid[::-1]))
    
locks = []
keys = []
for grid in data:
    t, k = parse_key_or_lock(grid)
    if t == 'LOCK':
        locks.append(k)
    else:
        keys.append(k)

print(locks, keys)
ret = 0
for lock in locks:
    for key in keys:
        for l, k in zip(lock, key):
            if l + k > 5:
                break
        else:
            ret += 1
print(ret)