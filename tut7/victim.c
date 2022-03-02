#include <stdio.h>

char shellcode[] =
    "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50"
    "\x53\x89\xe1\xb0\x0b\xcd\x80";

int fmtstr()
{
    char input[1000];
    int target_1 = 0x11223344;

    register char *ebp asm("ebp");
    printf("frame pointer of fmtstr is %p\n", ebp);

    printf("Address of shellcode is %p\n", &shellcode);
    printf("Address of input: %p\n", &input);
    printf("Address of target_1: %p\n", &target_1);
    printf("Value of target_1 (old): %d %.8x\n", target_1, target_1);
    printf("Please enter a string: ");

    fgets(input, sizeof(input) - 1, stdin);

    printf(input);

    printf("Value of target_1 (new): %d %.8x\n", target_1, target_1);
    return 1;
}

int main()
{
    // int target_2 = 0x55667788;

    // printf("Address of target_2: %p\n", &target_2);
    // printf("Value of target_2 (old): 0x%x\n", target_2);

    fmtstr();

    // printf("Value of target_2 (new): 0x%x\n", target_2);
    return 1;
    return 1;
}