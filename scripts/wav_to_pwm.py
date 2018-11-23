# -*- coding: utf-8 -*-
"""
将wav文件中的PCM波形转换为PWM高电平持续时间C语言数组代码
"""

import wave

import numpy as np

# 晶振频率(Hz)
CRYSTAL_FREQUENCY = 11059200
# 计数周期(s)
COUNT_PERIOD = 1 / (CRYSTAL_FREQUENCY / 12)


def wav_to_pwm(wav_path, output_path):
    with wave.open(wav_path, 'rb') as f:
        n_channels, sample_width, frame_rate, n_frames, _, _ = f.getparams()
        assert sample_width in (1, 2), '只支持8位或16位采样'
        frame_period = 1 / frame_rate
        pcm = f.readframes(n_frames)

    # 定时器0初始计数，影响PWM载波频率。载波频率越高越好，这里只取载波频率 = 采样频率
    init_count = 65536 - int(frame_period / COUNT_PERIOD)
    init_th0 = init_count // 256
    # 如果采样周期太长，每个周期需要2字节编码，浪费空间。最低频率3600Hz
    assert init_th0 == 255, '采样率太低'
    init_tl0 = init_count % 256

    if sample_width == 1:
        pcm = np.fromstring(pcm, np.int8).astype(np.float)
        # 取第一个声道
        pcm = pcm.reshape(n_frames, n_channels)[:, 0]
        # 方波下的面积在本周期占的比例，作为PWM方波占空比
        duty_cycles = (pcm + 128) / 256
    else:
        pcm = np.fromstring(pcm, np.int16).astype(np.float)
        pcm = pcm.reshape(n_frames, n_channels)[:, 0]
        duty_cycles = (pcm + 32768) / 65536
    # 定时器1在每个周期的初始计数，影响高电平时间
    init_tl1s = 256 - (duty_cycles * (frame_period / COUNT_PERIOD)).astype(np.int32)
    # 防溢出
    for index in np.where(init_tl1s < 0):
        init_tl1s[index] = 0
    for index in np.where(init_tl1s > 255):
        init_tl1s[index] = 255

    with open(output_path + '.h', 'w') as f:
        f.write(f"""#define SAMPLE_RATE {frame_rate}
// #define INIT_TH0 {init_th0}
#define INIT_TL0 {init_tl0}
#define PWM_DATA_LEN {len(init_tl1s)}
extern const unsigned char code pwmData[];
""")

    with open(output_path + '.c', 'w') as f:
        f.write('const unsigned char code pwmData[] = (\n')
        for i in range(0, len(init_tl1s), 32):
            f.write('\t"')
            for init_tl1 in init_tl1s[i: i + 32]:
                f.write(f'\\x{init_tl1:02X}')
            f.write('"\n')
        f.write(');\n')


def main():
    wav_to_pwm('flower dance.wav', '../pwm/music_data')


if __name__ == '__main__':
    main()
