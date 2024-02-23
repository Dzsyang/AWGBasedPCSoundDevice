from base import *
import numpy as np
import matplotlib.pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.rcParams['axes.unicode_minus'] = False
# font = {'family': 'SimSong', 'size': 22}
font = {}

def read_csv(filename):
    """读取picoscope输出的.csv文件，输出时间和强度数组"""
    with open(filename) as f:
        data = f.read().split('\n')[3:-1]
    data = [[float(i) for i in line.split(',')] for line in data]
    t = [row[0] for row in data]
    y = [row[1] for row in data]
    t = np.array(t) / 1000
    y = np.array(y)
    return t, y


def target(x):
    # x = (x + np.pi / 2) % (2 * np.pi)
    # return x / np.pi - 2 * (x > np.pi) * (x - np.pi) / np.pi - 1 / 2

    x = x % (2 * np.pi)
    if x < 2 * np.pi * 0.3 / 3:
        return 1
    elif x < 2 * np.pi / 3:
        return -1
    elif x < 2 * np.pi / 3 + 2 * np.pi * 0.5 / 3:
        return 1
    elif x < 4 * np.pi / 3:
        return -1
    elif x < 4 * np.pi / 3 + 2 * np.pi * 0.7 / 3:
        return 1
    else: return -1
    # return 1 - 2 * (x < 0.6 * np.pi)

    # x = (x + np.pi) % (2 * np.pi)
    # return x / np.pi - 1

t, y = read_csv('data.csv')
plt.figure(figsize=(16, 8), dpi=600)
plt.plot(t * 1000, y - 0.05, label='Experimental')
plt.plot(t * 1000, [target((i) * 2 * np.pi * 100) * 1.35 for i in t],
         label='Theoretical', linewidth=2, linestyle='--')
plt.ylabel('Amplitude(V)', font=font)
plt.xlabel('Time(ms)', font=font)
plt.legend(loc='upper right', prop=font)
plt.show()
