#include <unistd.h>

int main()
{
    symlink("hello_world.sh", "tmp");

    return 0;
}