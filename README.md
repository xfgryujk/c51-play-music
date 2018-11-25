# c51-play-music
51单片机播放音乐

## 相关博客
* [51单片机播放音乐（一）：蜂鸣器](https://blog.csdn.net/xfgryujk/article/details/84309970)
* [51单片机播放音乐（二）：DA转换播放任意波形](https://blog.csdn.net/xfgryujk/article/details/84349735)
* [51单片机播放音乐（三）：PWM播放任意波形](https://blog.csdn.net/xfgryujk/article/details/84479505)

## 编译方法
### 蜂鸣器
1. 将[蜂鸣器乐谱](https://github.com/xfgryujk/mml2beep)放到`scripts/beep.json`
2. 运行`scripts/tone_to_loop_count.py`
3. 编译`beep/beep.uvproj`

### DA转换
1. 将音频文件剪辑到大约10秒，重采样到大约5000Hz采样率，保存到`scripts/flower dance.wav`
2. 运行`scripts/wav_to_code.py`
3. 编译`dac/dac.uvproj`

### PWM
1. 将音频文件剪辑到大约10秒，重采样到大约5000Hz采样率，保存到`scripts/flower dance.wav`
2. 运行`scripts/wav_to_pwm.py`
3. 编译`pwm/pwm.uvproj`
