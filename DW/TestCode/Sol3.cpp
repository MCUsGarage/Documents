#include <stdio.h>

int main() 
{
    unsigned char chars[] = {0x49, 0x60, 0x67, 0x74, 0x63, 0x67, 0x42, 0x66, 0x80, 0x78,
     0x69, 0x69, 0x7B, 0x99, 0x6D, 0x88, 0x68, 0x94, 0x9F,0x8D, 0x4D, 0xA5, 0x9D, 0x45, 0x00};

    for(int i = 0; i < 24; i++)
    {
        printf("%c", ((chars[i] - (2 * i)) ^ i));
    }

    return 0;
}