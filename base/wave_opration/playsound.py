__all__ = ['play_sound']
from pygame import mixer


def play_sound(filename):
    """传入.wav文件名，播放音频，对返回对象使用.stop()方法停止播放"""
    if not mixer.get_init():
        mixer.init()
    s = mixer.Sound(filename)
    s.play(-1)
    return s
