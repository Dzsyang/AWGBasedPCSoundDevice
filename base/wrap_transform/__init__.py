__all__ = ['analyse', 'inv_wrap', 'c_to_data']
from .method import *


def analyse(filename, f, c):
    """解析picoscope输出的.csv的结果，基函数的频率为f，坐标c"""
    t, y = read_csv(filename)
    X = get_matrix_X(f, t, len(c) // 2)
    beta = cal_beta(X, y)
    uv = beta_to_uv(beta)
    return uv


def inv_wrap(c, f, t, uv):
    """做逆变换，f为基函数的频率，c为这组基函数下的坐标，t为时间轴"""
    c1 = inv_wrap_c(c, f, uv)
    y = c_to_data(f, c1, t)
    return y
