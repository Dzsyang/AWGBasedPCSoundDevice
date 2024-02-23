__all__ = ['decorate']
import numpy as np


def decorate(interval=0.05, tol=1):
    """
    函数修饰器
    interval：分点间隔
    tol：将在不连续点检测区间内斜率大于tol处视为不连续点
    """
    interval *= 2 * np.pi

    def ww(func):
        def wrap(x):
            for _a, _b, _fa, _k in tt:
                if _a < x <= _b:
                    return _fa + _k * (x - _a)
            return func(x)

        tt = []  # 记录不连续点数据
        xs = np.arange(-np.pi, np.pi, interval)  # 不连续点检测区间端点
        x0 = -np.pi
        f0 = func(x0)
        for i in range(1, len(xs)):
            x1 = xs[i]
            f1 = func(x1)
            k = (f1 - f0) / interval
            if abs(k) > tol:
                tt.append((x0, x1, f0, k))
            x0 = x1
            f0 = f1
        # 检测最后一个区间
        x1 = np.pi
        f1 = func(-np.pi)
        k = (f1 - f0) / (x1 - x0)
        tt.append((x0, x1, f0, k))
        return wrap

    return ww
