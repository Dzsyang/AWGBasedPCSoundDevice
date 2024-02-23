__all__ = ['func_to_c']

from scipy.integrate import quad
import numpy as np


def inner_product(f1, f2):
    """函数内积"""
    return quad(lambda x: f1(x) * f2(x), -np.pi, np.pi)[0]


def func_to_c(func, n=50):
    """func为[-pi,pi]上的函数，返回func的坐标"""
    c = []
    for k in range(1, n + 1):
        ak = inner_product(func, lambda x: np.cos(k * x)) / np.pi
        bk = inner_product(func, lambda x: np.sin(k * x)) / np.pi
        c += [bk, ak]
    return c
