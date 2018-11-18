# -*- coding: utf-8 -*-
"""
将wav文件中的PCM波形转换为C语言数组代码
"""

import wave

import numpy as np

# 晶振频率(Hz)
CRYSTAL_FREQUENCY = 11059200
# 计数周期(s)
COUNT_PERIOD = 1 / (CRYSTAL_FREQUENCY / 12)


def wav_to_code(wav_path, output_path):
    with wave.open(wav_path, 'rb') as f:
        n_channels, sample_width, frame_rate, n_frames, _, _ = f.getparams()
        assert sample_width in (1, 2), '只支持8位或16位采样'
        frame_period = 1 / frame_rate
        pcm = f.readframes(n_frames)

    th0 = 256 - int(frame_period / COUNT_PERIOD)
    assert th0 >= 0, '采样率太低'  # 最低频率3600Hz

    if sample_width == 1:
        pcm = np.fromstring(pcm, np.int8)
        # 取第一个声道
        pcm = pcm.reshape(n_frames, n_channels)[:, 0]
        pcm += 128
    else:
        pcm = np.fromstring(pcm, np.int16)
        pcm = pcm.reshape(n_frames, n_channels)[:, 0]
        pcm = (pcm + 32768).astype(np.float) / 256
        pcm = pcm.astype(np.int32)
        # 防溢出
        for index in np.where(pcm < 0):
            pcm[index] = 0
        for index in np.where(pcm > 255):
            pcm[index] = 255

    with open(output_path + '.h', 'w') as f:
        f.write(f"""#define INIT_TH0 {th0}
#define PCM_DATA_LEN {len(pcm)}
extern const unsigned char code pcmData[];
""")

    with open(output_path + '.c', 'w') as f:
        f.write('const unsigned char code pcmData[] = (\n')
        for i in range(0, len(pcm), 32):
            f.write('\t"')
            for sample in pcm[i: i + 32]:
                f.write(f'\\x{sample:02X}')
            f.write('"\n')
        f.write(');\n')


def main():
    wav_to_code('flower dance.wav', '../dac/music_data')


if __name__ == '__main__':
    main()
