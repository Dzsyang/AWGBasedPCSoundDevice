from .file_reader import read_file
from .generate_wave import Generator


def generate(input_filename, output_filename, rate=40000, channels=1, width=2, draw=False):
    """
    input_filename: 配置文件名
    output_filename: 输出音频文件名(以.wav为后缀)
    rate: 采样率
    channels: 声道数
    width: 采样宽度，使用int32类型，宽度为2
    draw: 是否作图
    """
    waves = read_file(input_filename)  # 读取配置文件
    generator = Generator(rate, channels, width)  # 初始化声波生成器
    generator.generate(waves)  # 生成波的数据
    generator.save(output_filename)  # 保存波的数据到output文件
    if draw:
        generator.draw()  # 作图
