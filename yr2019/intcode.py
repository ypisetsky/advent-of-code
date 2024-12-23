from collections import defaultdict
from copy import copy

def execute_one_inst(ip, mem, input_stream, output_stream):
    new_ip, state = execute_impl(ip, mem, input_stream, output_stream)
    if state == "Runnable":
        return new_ip
    else:
        return None

def execute_impl(ip, mem, input_stream, output_stream):
    op, modes = parse_opcode(mem[ip])

    if op == 1: # add
        dest = store_arg(ip, mem, modes, 3)
        mem[dest] = fetch_arg(ip, mem, modes, 1) + fetch_arg(ip, mem, modes, 2)
        return ip + 4, "Runnable"
    elif op == 2: # mul
        dest = store_arg(ip, mem, modes, 3)
        mem[dest] = fetch_arg(ip, mem, modes, 1) * fetch_arg(ip, mem, modes, 2)
        return ip + 4, "Runnable"
    elif op == 3: # input
        dest = store_arg(ip, mem, modes, 1)
        if len(input_stream) == 0:
            return ip, "Stalled"
        else:
            mem[dest] = input_stream.pop(0)
            return ip + 2, "Runnable"
    elif op == 4: # output
        output_stream.append(fetch_arg(ip, mem, modes, 1))
        return ip + 2, "Runnable"
    elif op == 5: # jump if true
        if fetch_arg(ip, mem, modes, 1) != 0:
            return fetch_arg(ip, mem, modes, 2), "Runnable"
        else:
            return ip + 3, "Runnable"
    elif op == 6: # jump if false
        if fetch_arg(ip, mem, modes, 1) == 0:
            return fetch_arg(ip, mem, modes, 2), "Runnable"
        else:
            return ip + 3, "Runnable"
    elif op == 7: # lt
        dest = store_arg(ip, mem, modes, 3)
        if fetch_arg(ip, mem, modes, 1) < fetch_arg(ip, mem, modes, 2):
            mem[dest] = 1
        else:
            mem[dest] = 0
        return ip + 4, "Runnable"
    elif op == 8: # eq
        dest = store_arg(ip, mem, modes, 3)
        if fetch_arg(ip, mem, modes, 1) == fetch_arg(ip, mem, modes, 2):
            mem[dest] = 1
        else:
            mem[dest] = 0
        return ip + 4, "Runnable"
    elif op == 9:
        mem["BASE"] += fetch_arg(ip, mem, modes, 1)
        return ip + 2, "Runnable"
    elif op == 99: # halt
        return None, "Halted"
    else:
        print(f"Weird inst {op} at {ip}")
        raise NotImplementedError
    
def fetch_arg(ip, mem, modes, idx):
    for _ in range(idx - 1):
        modes //= 10
    if modes % 10 == 0:
        return mem[mem[ip + idx]]
    elif modes % 10 == 1:
        return mem[ip + idx]
    elif modes % 10 == 2:
        rel_base = mem["BASE"]
        return mem[rel_base + mem[ip + idx]]
    else:
        print(f"Weird mode {modes} at {ip}")
        raise NotImplementedError
    
def store_arg(ip, mem, modes, idx):
    for _ in range(idx - 1):
        modes //= 10
    if modes % 10 == 0:
        return mem[ip + idx]
    elif modes % 10 == 1:
        print(f"Attempting to write to immediate at {ip, idx}")
        raise NotImplementedError
    elif modes % 10 == 2:
        rel_base = mem["BASE"]
        return rel_base + mem[ip + idx]
    else:
        print(f"Weird mode {modes} at {ip}")
        raise NotImplementedError

def get_all_output(bytecode, input):
    proc = Processor(bytecode, input)
    return proc.consume_output()


class Processor:
    def __init__(self, bytecode, input):
        self.memory = defaultdict(int)
        for i, v in enumerate(bytecode):
            self.memory[i] = v
        self.ip = 0
        self.status = "Runnable"
        self.output = []
        self.input = input[:]
        self.run()

    def feed_input(self, input):
        self.input.extend(input)
        if self.status == "Stalled":
            self.status = "Runnable"
        self.run()

    def done(self):
        return self.status == "Halted"

    def run(self):
        while self.status == "Runnable":
            self.ip, self.status = execute_impl(self.ip, self.memory, self.input, self.output)
    
    def consume_output(self):
        ret = self.output
        self.output = []
        return ret
    
    def clone(self):
        target = Processor([99], [])
        target.ip = self.ip
        target.memory = copy(self.memory)
        target.status = self.status
        target.output = self.output[:]
        target.input = self.input[:]
        return target
        

def parse_opcode(encoded):
    return encoded % 100, encoded // 100