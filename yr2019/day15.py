from util import Tuple, printgrid, printgrid2, tokenedlines
from yr2019.intcode import Processor
from heapq import heappop, heappush

day = "15"

bytecode = tokenedlines(day, sep=",")[0]

grid = {}



DELTAS = {
    (-1, 0): 1,
    (0, -1): 3,
    (1, 0): 2,
    (0, 1): 4
}
start_interpreter = Processor(bytecode, [])

def floodfill(interpreter, part2):
    
    queue = []
    queue.append((0, (0, 0), interpreter))
    visited = {(0, 0): 'S'}
    enqueued = set([(0, 0)])
    while len(queue) > 0:
        dist, point, interpreter = queue.pop(0)
        for dir, command in DELTAS.items():
            newinterpreter = interpreter.clone()
            newinterpreter.feed_input([command])
            result = newinterpreter.consume_output()
            newpoint = Tuple.add(point, dir)
            if result == [0]:
                visited[newpoint] = '#'
                continue
            elif result == [1]:
                if newpoint not in enqueued:
                    queue.append((dist + 1, newpoint, newinterpreter))
                    enqueued.add(newpoint)
                    visited[newpoint] = '.'
            elif result == [2]:
                visited[newpoint] = '*'
                if not part2:
                    print("Done part 1")
                    printgrid2(visited)
                    return newinterpreter, dist + 1
    if part2:
        print("Done part 2")
        printgrid2(visited)
        return dist 

p2_interpreter, p1_answer = floodfill(start_interpreter, False)
p2_answer = floodfill(p2_interpreter, True)
print(p1_answer, p2_answer)