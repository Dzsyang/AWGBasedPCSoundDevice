import numpy as np
from .wave_operate import write_wave
import matplotlib.pyplot as plt


class Generator:
    def __init__(self, rate=44100, channels=1, width=2):
        self.data = None
        self.length = 0
        self.rate, self.channels, self.width = rate, channels, width
        self.ns = int(rate * channels * width / 4)  # 一秒的数据长度

    def draw(self):
        plt.plot(np.linspace(0, self.length / self.ns, self.length), self.data)
        plt.show()

    def save(self, filename):
        write_wave(self.data, filename, self.rate, self.channels, self.width)

    def generate(self, waves):
        self._get_length(waves)  # 获取数据的总长度
        for wave in waves:
            self._add_wave_data(wave)  # 添加每一个wave数据
        return self.data

    def _get_length(self, waves):
        for wave in waves:  # 最大的end时间
            if wave['end'] > self.length:
                self.length = wave['end']
        self.length *= self.ns  # 数据长度=时间*每秒的长度
        self.data = np.zeros(self.length)  # 初始化数据

    def _add_wave_data(self, wave):
        start = int(wave['start'] * self.ns)
        end = int(wave['end'] * self.ns)

        period_length = int(sum(item[1] for item in wave['wave']) * self.ns)  # 一个周期的数据长度
        period_data = np.zeros(period_length)  # 一个周期的数据

        pin = 0
        for item in wave['wave']:
            length = int(item[1] * self.ns)
            item_data = np.linspace(0, 1, length)
            period_data[pin:pin + length] += item[0] * wave['type'](item_data) * wave['volume']
            pin += length

        wave_length = end - start  # 一个wave的长度
        one_wave = np.zeros(wave_length)  # 一个wave的数据
        # 按周期填充数据
        pin = 0
        while True:
            length = period_length
            if pin + length > wave_length:
                one_wave[pin:wave_length] += period_data[:wave_length - pin]
                break
            else:
                one_wave[pin:pin+length] += period_data
                pin += length

        self.data[start:end] = one_wave
