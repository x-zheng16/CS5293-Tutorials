#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void unsafe_copy(char *input_str)
{
    char target_str[100];
    strcpy(target_str, input_str);

    /* Debug Tool

    Uncomment the following codes to directly get the needed address info.
    Refer to the following sites for extra details if interested.
        "https://www.cristal.univ-lille.fr/~marquet/ens/ctx/doc/l-ia.html"
        "https://dmalcolm.fedorapeople.org/gcc/2015-08-31/rst-experiment/how-to-use-inline-assembly-language-in-c-code.html#defining-global-register-variables"
    */
    // printf("Address of buffer is %p\n", target_str);

    // register char *ebp asm("ebp");
    // printf("Frame Pointer of unsafe_copy is %p\n", ebp);
    // printf("Offset of return address is %d\n", ebp + 4 - target_str);

    // char *value = (char *)getenv("TUT8");
    // printf("Value of TUT8: %s\n", value);
    // printf("Address of TUT8: %p\n", value);
    // printf("Address of system: %p\n", system);
}

int main()
{
    char input_str[500];
    FILE *badfile;
    badfile = fopen("badfile", "r");
    fread(input_str, sizeof(char), 500, badfile);
    unsafe_copy(input_str);
    printf("Return properly!\n");
    return 1;
}
