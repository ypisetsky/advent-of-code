from math import gcd, lcm
from util import tokenedlines, getlines, Tuple

day = "ex"
def apply_gravity(moon1, moon2):
    pos1, vel1 = moon1
    pos2, vel2 = moon2

    delta1 = []
    delta2 = []
    for i in range(len(pos1)):
        if pos1[i] < pos2[i]:
            delta1.append(1)
            delta2.append(-1)
        elif pos1[i] > pos2[i]:
            delta1.append(-1)
            delta2.append(1)
        else:
            delta1.append(0)
            delta2.append(0)   
    return (pos1, Tuple.add(vel1, delta1)), (pos2, Tuple.add(vel2, delta2))

def apply_velocity(moon):
    pos, vel = moon
    return (Tuple.add(pos, vel), vel)

def step_time(moons):
    moons = list(moons)
    for i in range(len(moons)):
        for j in range(i + 1, len(moons)):
            moons[i], moons[j] = apply_gravity(moons[i], moons[j])
    for i in range(len(moons)):
        moons[i] = apply_velocity(moons[i])
    return tuple(moons)

def parse_line(line):
    line = line.strip("<>").split(", ")
    return ([int(x.split("=")[1]) for x in line], [0, 0, 0])

def energy(moons):
    ret = 0
    for moon in moons:
        pos, vel = moon
        ret += sum([abs(x) for x in pos]) * sum([abs(x) for x in vel])
    return ret

def find_period(moons, dim):
    current = tuple(((moon[0][dim],), (moon[1][dim],)) for moon in moons)
    visited = {}
    count = 1
    while current not in visited:
        visited[current] = count
        current = step_time(current)
        count += 1
    return count, count - visited[current]


moons = [parse_line(line) for line in getlines(day)]
nums = find_period(moons, 0), find_period(moons, 1), find_period(moons, 2)
print(nums, lcm(*[ret[0] for ret in nums]), lcm(*[ret[1] for ret in nums]))
# print((nums[0] * nums[1] * nums[2]) / gcd(nums[0], gcd(nums[1], nums[2]))) 
# print(gcd(find_period(moons, 0), gcd(find_period(moons, 1), find_period(moons, 2))))



for i in range(1000):
    moons = step_time(moons)

print(energy(moons))