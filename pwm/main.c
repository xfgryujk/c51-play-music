#include <AT89X51.H>

#include "music_data.h"

// 引脚定义
#define pwmOut P1_0

unsigned int iPwmData = 0;

void Init() {
	// 开启中断
	EA = 1;
	ET0 = 1;
	ET1 = 1;
	// 定时器0工作方式2（8位自动重载定时器）
	// 定时器1工作方式1（16位定时器）
	TMOD = 0x12;
	
	TH0 = TL0 = INIT_TL0;
	TH1 = 255;
	TL1 = pwmData[iPwmData];
	
	pwmOut = 1;
	// 开启定时器
	TR0 = 1;
	TR1 = 1;
}

int main() {
	Init();
	while (1);
	
	return 0;
}

// 定时器0，输出高电平，周期为PWM载波周期
void HandleTimer0() interrupt 1 {
	pwmOut = 1;
	if (++iPwmData >= PWM_DATA_LEN)
		iPwmData = 0;
	
	TH1 = 255;
	TL1 = pwmData[iPwmData];
	
	TR1 = 1;
}

// 定时器1，输出低电平，周期根据占空比定
void HandleTimer1() interrupt 3 {
	pwmOut = 0;
	TR1 = 0;
}
