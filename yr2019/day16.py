from util import getlines

day = "16"

sequence = [int(c) for c in getlines(day)[0]]


def fft(sequence):
    ret = []
    length = len(sequence)
    for i in range(length):
        pattern1 = [0] * (i + 1) 
        pattern3 = [-1] * (i + 1)
        pattern2 = [1] * (i + 1)
        overallpattern = pattern1 + pattern2 + pattern1 + pattern3
        mod = (i + 1) * 4
        num = 0
        for j in range(length):
            k = (j + 1) % mod
            num += overallpattern[k] * sequence[j]
        ret.append(abs(num) % 10)
    return ret
print(fft([1,2,3,4,5,6,7,8]))

for i in range(100):
    sequence = fft(sequence)
print("".join(str(x) for x in sequence))