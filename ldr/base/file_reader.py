import re
import numpy as np


def read_file(filename):
    # 读取文件内容
    with open(filename, 'rb') as f:
        data = f.read().decode()

    # 删除注释内容
    for row in re.findall(r'(#.*?)\n', data):  # 注释内容以#开头到\n结尾
        data = data.replace(row, '')
    data = data.replace('\r', '')

    waves = []
    analyser = _WaveAnalyse()  # 生成解析器
    for template in re.findall(r'/\*\*\n(.*?)\*\*/', data, re.S):
        analyser.feed_template(template)  # 加载模板
    for wave in re.findall(r'/\*\n(.*?)\*/', data, re.S):  # 遍历每个波的数据内容（/* */中间的内容）
        waves.append(analyser.analyse(wave))
    waves = list(filter(lambda item: 'wave' in item, waves))  # 删除没有波数据的内容
    print(analyser.templates)
    return waves


# 单位换算
unit_operator = {
    's': lambda x: x,
    'ms': lambda x: x / 1000,
    'hz': lambda x: 1 / x,
    'khz': lambda x: 1 / x / 1000,
}

functions = {
    'square': lambda t: t,
    'sin': lambda t: np.sin(t * 2 * np.pi),
}


class _WaveAnalyse:
    def __init__(self):
        self.data = None
        self.templates = {
            'default': {
                'persist': '1',
                'type': 'square',
                'volume': '1000',
                'waveUnit': 'ms',
            }
        }

    def analyse(self, wave):
        """解析一个 /* */ 内部的内容，输出为dict类型"""
        self.data = wave
        self._split_order()  # 将内容解析为键值对
        self._wrap_wave()  # 修饰wave的内容
        return self.data

    def feed_template(self, data):
        """登记模板数据"""
        self.data = data
        self._split_order()
        self._wrap_template()

    def __getitem__(self, item):
        if item in self.data:
            return self.data[item]
        else:
            return ''

    def __setitem__(self, key, value):
        self.data[key] = value

    def _split_order(self):
        orders = {}
        flag = 0
        for row in self.data.split('\n'):
            if ':' in row:  # 键的标志
                flag = 0
                order, content = row.split(':')
                content = content.strip()
                if content:  # 单行指令
                    orders[order] = content
                else:  # 多行指令
                    flag = order  # 将后面的内容抛到 elif flag
                    orders[order] = []
            elif flag:  # 当前读取的为多行命令的内容，键为flag
                content = row.strip()
                if content:
                    orders[flag].append(content.split(','))
        self.data = orders

    def _wrap_wave(self):
        """修饰wave"""
        # 加载模板
        template = self.templates[self['template'] or 'default']
        for item in ['persist', 'type', 'volume', 'waveUnit']:
            if not self[item]:
                self[item] = template[item]

        self['start'] = eval(self['start'] or '0')
        self['end'] = eval(self['end'] or str(self['start'] + eval(self['persist'])))
        self['volume'] = eval(self['volume'])
        self['type'] = functions[self['type']]

        unit = self['waveUnit']  # 默认单位为ms
        for i, row in enumerate(self['wave']):
            self['wave'][i] = self._trans_data_by_unit(row, unit.lower())  # 单位换算

    def _wrap_template(self):
        """修饰template"""
        name = self['name']
        del self.data['name']
        for item in ['persist', 'type', 'volume', 'waveUnit']:
            if not self[item]:
                self[item] = self.templates['default'][item]
        self.templates[name] = self.data

    @staticmethod
    def _trans_data_by_unit(row, unit):
        row[0] = eval(row[0])
        row[1] = unit_operator[unit](eval(row[1]))
        return row


if __name__ == '__main__':
    w = read_file('../set.txt')
    print(w)
