import sys
import numpy as np


freq_table = {
        "E": 56.88,
        "M": 15.36,
        "A": 43.31,
        "H": 15.31,
        "R": 38.64,
        "G": 12.59,
        "I": 38.45,
        "B": 10.56,
        "O": 36.51,
        "F": 9.24,
        "T": 35.43,
        "Y": 9.06,
        "N": 33.92,
        "W": 6.57,
        "S": 29.23,
        "K": 5.61,
        "L": 27.98,
        "V": 5.13,
        "C": 23.13,
        "X": 1.48,
        "U": 18.51,
        "Z": 1.39,
        "D": 17.25,
        "J": 1.00,
        "P": 16.14,
        "Q": 1,
}

diff_list = []

if len(sys.argv) < 2:
    print("Usage: python3 classifier.py <dictionary>")
    exit(1)

with open(sys.argv[1]) as f:
    words = filter(lambda s: s.isalpha() and all(ord(c) < 128 for c in s), f.read().split('\n'))
    for word in words:
        score = sum([(1/freq_table[c.upper()]) for c in word])
        diff_list.append((word, score))

scores = list(map(lambda t: t[1], diff_list))
scores_as_nparray = np.asarray(scores, dtype=np.float32)

median = np.median(scores_as_nparray)
stddev = np.std(scores_as_nparray)

easy_ends = median - stddev/2
hard_start = median + stddev/2
print("{},{}".format(easy_ends, hard_start))
for (word, score) in diff_list:
    print("{},{}".format(word, score))
