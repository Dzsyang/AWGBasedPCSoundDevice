from base import *
import numpy as np
import os


@decorate(0.05, 1)
def target(x):
    if x < -np.pi + 2 * np.pi * 0.3 / 3:
        return 1
    elif x < -np.pi + 2 * np.pi / 3:
        return -1
    elif x < -np.pi / 3 + 2 * np.pi * 0.5 / 3:
        return 1
    elif x < np.pi / 3:
        return -1
    elif x < np.pi / 3 + 2 * np.pi * 0.7 / 3:
        return 1
    else:
        return -1

    # return np.sin(x) + np.sin(3 * x)
    # return x / np.pi / 2 + 0.5  # 锯齿波
    # return 1 if x < -np.pi + 2 * np.pi * 0.7 else 0
    # return -1 if x < 0 else 1  # 方波
    # return 1 + x / np.pi if x < 0 else 1 - x / np.pi  # 三角波


f = 100  # 频率
n = 30  # 谐波数
t = 10  # 时长
rate = 44100  # 采样率

t = np.linspace(0, t, rate * t)  # 时间轴
c = func_to_c(target, n)  # 目标函数坐标

data = c_to_data(f, [1, 0] * n, t)
wave_write(data, 'tmp.wav', rate)
sound = play_sound('tmp.wav')
input('请录入数据')
sound.stop()

print('正在解析数据')
result = analyse('data.csv', f, [1, 0] * n)
os.remove('data.csv')
os.remove('tmp.wav')
print('解析完成，正在进行逆变换')

data1 = inv_wrap(c, f, t, result)
wave_write(data1, 'result.wav', rate)
sound = play_sound('result.wav')
input('数据生成成功')
sound.stop()
