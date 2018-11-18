#include <AT89X51.H>

#include "music_data.h"

// 引脚定义
#define wavOut P2

unsigned int iPcmData = 0;

void Init() {
	// 开启中断
	EA = 1;
	ET0 = 1;
	// 定时器0工作方式2（8位自动重载定时器）
	TMOD = 0x2;
	TH0 = TL0 = INIT_TH0;
	wavOut = pcmData[iPcmData];
	// 开启定时器
	TR0 = 1;
}

int main() {
	Init();
	while (1);
	
	return 0;
}

void HandleTimer0() interrupt 1 {
	wavOut = pcmData[iPcmData];
	if (++iPcmData >= PCM_DATA_LEN)
		iPcmData = 0;
}
