#include <stdio.h>
#include <stdlib.h>
#include <time.h> 
#include <windows.h>
#include <mmintrin.h>//mmx
#include <xmmintrin.h>//sse
#include <emmintrin.h>//sse2

__m128i *buffer_ptr;
__m128i a;
void sendMessage(int x) {
	int startTime, endTime;
	__m128i *ptr; 
	if(x) {
		startTime = clock();
		ptr = buffer_ptr;
		do {		 
			_mm_stream_si128(ptr, a);
			ptr = ptr + 1;
			endTime = clock();			
		}while(endTime - startTime < 500);
		printf("Send 1: %d ms\n", endTime - startTime);
	} else {
		startTime = clock();
		Sleep(500);
		endTime = clock();
		printf("Send 0: %d ms\n", endTime - startTime);
	}
}
int main(void) {
	buffer_ptr = (__m128i*)malloc(5120000000);
	__declspec(align(16)) float num[4] = {1.0, 2.0, 3.0, 4.0};
	a = (__m128i)_mm_load_ps(num);
	printf("%d %d\n", buffer_ptr, (buffer_ptr+1));
	while(1) {
		sendMessage(1);
		sendMessage(1);
		sendMessage(0);
		sendMessage(0);
	}
    return 0;
}
