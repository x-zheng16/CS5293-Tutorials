#include <stdio.h>

int main()
{
    int count = 0;

    printf("Hello %.100x%n\n", 1, &count);
    printf("The value of count is %d\n", count);
    return 1;
}