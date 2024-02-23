__all__ = ['get_matrix_X', 'read_csv', 'cal_beta', 'beta_to_uv', 'inv_wrap_c', 'c_to_data']
import numpy as np


def get_matrix_X(f, t, n):
    """生成X=[sin(2pif1t), cos(2pif1t), ..., sin(2pifnt), cos(2pifnt)]"""
    m = len(t)
    X = np.zeros((m, n * 2))
    for i in range(n):
        X[:, 2 * i] = np.sin(2 * np.pi * f * (i + 1) * t).flatten()
        X[:, 2 * i + 1] = np.cos(2 * np.pi * f * (i + 1) * t).flatten()
    return X


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


def cal_beta(X, y):
    """解正规方程，返回系数矩阵beta"""
    beta = np.linalg.solve(X.T @ X, X.T @ y)
    return beta


def beta_to_uv(beta):
    """将beta转为uv格式：[[beta11, beta12], [beta21, beta22], ...]"""
    nn = beta.size
    rr = []
    for i in range(nn // 2):
        rr.append([float(beta[2 * i]), float(beta[2 * i + 1])])
    return rr


def inv_wrap_c(c, f, uv):
    """做逆变换，f为基函数的频率，c为这组基函数下的坐标，返回逆变换后的坐标"""
    c1 = np.zeros_like(c)  # 逆变换后的坐标
    for i in range(len(uv)):
        u, v = uv[i]
        A = np.array([[u, v], [-v, u]]) / (u ** 2 + v ** 2)
        c1[2 * i:2 * i + 2] = A @ c[2 * i:2 * i + 2]
    return c1


def c_to_data(f, c, t):
    """将坐标转为音频数据，c为坐标，f为基函数的频率，t为时间轴"""
    X = get_matrix_X(f, t, len(c) // 2)
    y = X @ c
    return y
