#include <stdio.h>
#include <stdlib.h>

int target_3 = 0x55667788;

int fmtstr()
{
    char input[1000];
    int target_1 = 0x11223344;

    char shellcode[] =
        "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50"
        "\x53\x89\xe1\xb0\x0b\xcd\x80";

    // helpful info
    // register char *ebp asm("ebp");
    // printf("frame pointer of fmtstr is %p\n", ebp);
    printf("Address of input: %p\n", &input);
    printf("Address of target_1: %p\n", &target_1);
    printf("Address of shellcode: %p\n", &shellcode);
    printf("Value of target_1 (old): %d %.8x\n", target_1, target_1);
    printf("Please enter a string: ");

    fgets(input, sizeof(input) - 1, stdin);
    printf("Value of input (new): %s\n", input);

    // vulnerable call of printf
    printf(input);

    printf("\n");
    printf("Value of target_1 (new): %d %.8x\n", target_1, target_1);
    // helpful info
    register char *ebp asm("ebp");
    printf("frame pointer of fmtstr is %p\n", ebp);
    printf("value of return address is %.8x\n", *(ebp + 4));
    return 1;
}

int main()
{
    int target_2 = 0x55667788;

    int *target_4 = (int *)malloc(2 * sizeof(int));
    target_4[0] = 0x11223344;
    target_4[1] = 0x55667788;

    printf("(Optional) Address of target_2: %p\n", &target_2);
    printf("(Optional) Value of target_2 (old): %d %.8x\n", target_2, target_2);
    printf("(Optional) Address of target_3: %p\n", &target_3);
    printf("(Optional) Value of target_3 (old): %d %.8x\n", target_3, target_3);
    printf("(Optional) Address of target_4[0]: %p\n", target_4);
    printf("(Optional) Value of target_4[0] (old): %d %.8x\n", target_4[0], target_4[0]);
    printf("(Optional) Address of target_4[1]: %p\n", target_4 + 1);
    printf("(Optional) Value of target_4[1] (old): %d %.8x\n", target_4[1], target_4[1]);

    fmtstr();

    printf("(Optional) Value of target_2 (new): %d %.8x\n", target_2, target_2);
    printf("(Optional) Value of target_3 (new): %d %.8x\n", target_3, target_3);
    printf("(Optional) Value of target_4[0] (new): %d %.8x\n", target_4[0], target_4[0]);
    printf("(Optional) Value of target_4[1] (new): %d %.8x\n", target_4[1], target_4[1]);

    free(target_4);
    return 1;
}