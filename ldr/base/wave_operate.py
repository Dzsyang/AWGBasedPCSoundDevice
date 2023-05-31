import wave
import numpy as np


def write_wave(content: list, filename: str, rate=40000, channels=1, width=2):
    """
    content: [int,...]
    filename: str
    channels: 声道数
    width: 样本宽度
    rate: 采样率
    """
    content = np.array(content, dtype=np.int32)
    #  写入wav文件
    f = wave.open(filename, 'wb')
    f.setnchannels(channels)
    f.setsampwidth(width)
    f.setframerate(rate)
    f.writeframes(content.tostring())
    f.close()
