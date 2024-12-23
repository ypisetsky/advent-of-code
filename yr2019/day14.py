

from collections import defaultdict
from math import ceil

from util import getlines

day = "14"
data = getlines(day)

def compute_ore(reactions, fuel=1):
    need = defaultdict(int)
    need["FUEL"] = fuel
    finished = {}
    while need != {}:
        for item, quantity in need.items():
            if is_ready(item, finished, reactions):
                if item == "ORE":
                    return quantity
                outquant, demanded = reactions[item]
                recipequant = ceil(quantity / outquant)
                for demand, demandnum in demanded.items():
                    need[demand] += demandnum * recipequant
                del need[item]
                finished[item] = recipequant * outquant
                break

def is_ready(item, finished, reactions):
    for dest, recipe in reactions.items():
        if dest in finished:
            continue
        if item in recipe[1]:
            return False
    return True

def parse_reagent(reagentstr):
    quant, reagent = reagentstr.split(" ")
    return reagent, int(quant)

def parse_recipe(line):
    reagents, target = line.split(" => ")
    targetitem, recipequant = parse_reagent(target)
    reagents = dict([parse_reagent(reagent) for reagent in reagents.split(", ")])
    return targetitem, recipequant, reagents

reactions = {}
for line in data:
    targetitem, recipequant, reagents = parse_recipe(line)
    reactions[targetitem] = recipequant, reagents

print(compute_ore(reactions, 1))

TRILLION = 1_000_000_000_000
lowest = 1
highest = TRILLION
while lowest < highest:
    target = (lowest + highest) // 2
    if compute_ore(reactions, target) < TRILLION:
        lowest = target + 1
    else:
        highest = target
print(lowest, highest)
if compute_ore(reactions, lowest) < TRILLION:
    print(lowest)
else:
    print(lowest - 1)