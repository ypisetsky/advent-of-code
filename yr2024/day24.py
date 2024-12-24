from collections import defaultdict
from util import getlines, tokenedlines, Tuple
day = "24"

def parse_line(line):
    if ':' in line:
        parts = line.split(': ')
        return ('VALUE', parts[0], int(parts[1]), None)
    elif '->' in line:
        parts = line.split(' ')
        return (parts[1], parts[4], parts[0], parts[2])
    

data = [parse_line(line) for line in getlines(day)]
values = {}
queue = []
blocked = defaultdict(set)
blockercount = {}
byresult = {}
for op, result, op1, op2 in data:
    byresult[result] = (op, op1, op2)
    if op != 'VALUE':
        blocked[op1].add(result)
        blocked[op2].add(result)
        blockercount[result] = 2
    else:
        queue.append(result)

def flushqueue():
    while len(queue) > 0:
        var = queue.pop(0)
        op, op1, op2 = byresult[var]
        print(f"      Evaluating {op1} {op} {op2} -> {var}")
        if op == 'VALUE':
            values[var] = op1
        elif op == 'AND':
            values[var] = values[op1] & values[op2]
        elif op == 'OR':
            values[var] = values[op1] | values[op2]
        elif op == 'XOR':
            values[var] = values[op1] ^ values[op2]
        for blockee in blocked[var]:
            blockercount[blockee] -= 1
            if blockercount[blockee] == 0:
                queue.append(blockee)

previous = set(values)
queue = []

def analyze_new_values(processed, i, carry):
    x = f"x{i:02}"
    y = f"y{i:02}"
    if i == 0:
        return 'gtb'
    if x not in processed:
        print("Missing x", i)
    if y not in processed:
        print("Missing y", i)
    local_xor = None
    local_and = None
    second_xor = None
    second_and = None
    final_or = None
    if len(processed) != 7:
        print("Processed wrong number")
    for value in processed:
        if byresult[value][0] == 'XOR':
            if x in byresult[value] and y in byresult[value]:
                local_xor = value
            elif second_xor is None:
                second_xor = value
            else:
                print(f"Strange xors {value} {second_xor}")
        elif byresult[value][0] == 'AND':
            if x in byresult[value] and y in byresult[value]:
                local_and = value
            elif second_and is None:
                second_and = value
            else:
                print(f"Strange ands {value} {second_xor}")
        elif byresult[value][0] == 'VALUE':
            if value != x and value != y:
                print(f"Strange constant {value}")
        elif byresult[value][0] == 'OR':
            if final_or is None:
                final_or = value
    
    if carry not in byresult[second_xor]:
        print(f"{carry} not used by second xor {second_xor}")
    if carry not in byresult[second_and]:
        print(f"{carry} not used by second and {second_and}")    
    if local_xor not in byresult[second_xor]:
        print(f"{local_xor} not used by second xor {second_xor}")
    if local_xor not in byresult[second_and]:
        print(f"{local_xor} not used by second xor {second_and}")
    if local_and not in byresult[final_or]:
        print(f"{local_and} not used by or {final_or}")
    if second_and not in byresult[final_or]:
        print(f"{second_and} not used by or {final_or}")
    return final_or

carry = None
for i in range(45):
    queue.append(f"x{i:02}")
    queue.append(f"y{i:02}")
    flushqueue()
    print("    new values: ", set(values.keys()).difference(previous))
    carry = analyze_new_values(set(values.keys()).difference(previous), i, carry)
    previous = set(values)



sortedvars = sorted(values.keys(), reverse=True)
num = 0
for var in sortedvars:
    if var[0] == 'z':
        num *= 2
        num += values[var]
print(sorted(values.items()))
print(num)
