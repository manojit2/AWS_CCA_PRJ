

from math import log

k1 = 100
k2 = 100
b = 0.5
R = 0.0


def score_BM25(weight, n, f, qf, r, N, dl, avdl):
    K = compute_K(dl, avdl)
    first = log(((r + 0.5) / (R - r + 0.5)) / ((n - r + 0.5) / (N - n - R + r + 0.5)))
    second = ((k1 + 1) * f) / (K + f)
    third = qf*weight
        #((k2+1) * qf) / (k2 + qf)
        # print(round(first, 2), round(second, 2), round(third, 2))
        #original = round(first*second*third, 2)
    upgraded = round(first*second*third, 2)
    return upgraded


def compute_K(dl, avdl):
    return k1 * ((1-b) + b * (float(dl)/float(avdl)) )