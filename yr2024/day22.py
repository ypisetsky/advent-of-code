from collections import defaultdict
import itertools
from util import getlines, tokenedlines, Tuple
from functools import cache

day = "22"
# day = "ex"

BATCH = 1
@cache
def evolve(num):
    for i in range(0, BATCH):
        num = ((num << 6) ^ num) & 16777215
        num = num ^ (num >> 5 ) & 16777215
        num = ((num << 11) ^ num) & 16777215
        # print(num)
    return num

def mevolve(num, steps):
    for i in range(steps // BATCH):
        num = evolve(num)
    return num

data = [int(r) for r in getlines(day)]
print(data)

ret = 0
for row in data:
    a = mevolve(row, 2000)
    # print(row, a)
    ret += a
print(ret)

monkeys = [[r] for r in data]
deltas = [[] for r in data]
for i in range(2001):
    for monkey, delta in zip(monkeys, deltas):
        monkey.append(evolve(monkey[-1]))
        delta.append(monkey[-1] % 10 - (monkey[-2] % 10))

def check_window(window):
    score = 0
    for monkey, delta in zip(monkeys, deltas):
        for i in range(2000):
            if window[0] == delta[i] and window[1] == delta[i+1]:
                if window == delta[i:i+4]:
                    score += monkey[i+4] % 10
                    break
    return score
best = 0
count = 0

alldeltas = defaultdict(int)
for i in range(2000 - 4):
    for delta in deltas:
        alldeltas[tuple(delta[i:i+4])] += 1
print(len(alldeltas))

alldeltas = list((v, k) for k, v in alldeltas.items())
alldeltas.sort(reverse=True)
n = 0
for count, window in alldeltas:
    window = list(window)
    
    bestval = -1
    for num in range(10):
        for d in window:
            num += d
            if num < 0 or num > 9:
                break
        if 0 <= num <= 9:
            bestval = num
                
    n += 1
    if n % 100 == 0:
        print(n)
    
    if bestval * count <= best:
        continue
    best = max(check_window(window), best)
    
print(best)