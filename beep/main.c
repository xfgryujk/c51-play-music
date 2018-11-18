#include <AT89X51.H>

#include "music_data.h"

// 引脚定义
#define beepOut P1_0

int main() {
	beepOut = 0;
	while (1) {
		unsigned int i, j, k;
		for (i = 0; i < NOTES_LEN; ++i) {
			if (notes[i][0] == DELAY_COUNT) // 延时
				for (j = 0; j < notes[i][1]; ++j);
			else {
				for (j = 0; j < notes[i][1]; ++j) {
					for (k = 0; k < notes[i][0]; ++k);
					beepOut = 1;
					for (k = 0; k < notes[i][0]; ++k);
					beepOut = 0;
				}
			}
		}
	}
	
	return 0;
}
