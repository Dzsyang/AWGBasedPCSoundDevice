"""wav文件操作模块"""
__all__ = ['wave_write', 'wave_read']

import numpy as np
import wave


def wave_write(content: np.ndarray, filename: str, rate=44100, strength=16000):
    """
    content: 音频数据数组
    filename: str，输出的文件名，'.wav'结尾
    rate: 采样率，默认44100
    strength: 强度单位，默认16000
    """
    if abs(strength) > 32767:
        raise ValueError
    content = strength * content / max(abs(content))
    content = np.array(content, dtype=np.int16)
    #  写入wav文件
    f = wave.open(filename, 'wb')
    f.setnchannels(1)
    f.setsampwidth(2)
    f.setframerate(rate)
    f.writeframes(content.tobytes())
    f.close()


def wave_read(filename):
    """读取wav文件，输出音频数据、采样率、声道数、采样宽度"""
    f = wave.open(filename, 'rb')
    rate = f.getframerate()
    channels = f.getnchannels()
    width = f.getsampwidth()
    frame = f.getnframes()
    data = f.readframes(frame)
    data = np.frombuffer(data, dtype=np.int32)
    return data, rate, channels, width
