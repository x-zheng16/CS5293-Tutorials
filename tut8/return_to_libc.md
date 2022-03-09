# Hands-on Stack-based Return_to_Libc

## Frequently Asked Questions about tut6

1. `gdb_mem_addr_stack - gdb_mem_addr_buffer` is the offset of $epb, not the offset of return address.

2. Running env (e.g. run program directly in terminal by typing `./runnable_program`) and debugging env (e.g. run program in gdb by typing `r`) might be different.

3. Offset of return address is around the buffer size.

4. Step into the vulnerable function by `n` or `s` to get the correct `$ebp`

5. 32-bit and 64-bit programs use different registers so that the shellcodes are different for them.

6. Uncomment the lines in stack.c to get real ebp and buffer address. This is just a trick for your homework; in practice, you cannot modify the vulnerable source code.

7. Choice of shellcode: all of the provided shellcodes have been tested by call_sh_32.c or call_sh_64.c. However, when you choose one and encounter an error "illegal hardware instruction", try others.

8. Cannot get root shell. Remember to change your default shell into zsh by typing `sudo ln -sf /bin/zsh /bin/sh` in terminal

## Setup Lab Environment

```bash
# install python3
sudo apt install python3 python3-dev

# use bash or zsh as sh
sudo ln -sf /bin/zsh /bin/sh

# set environment variable
export TUT8="/bin/sh"

# restart the terminal and check the shell version
echo $SHELL

# turn off Address Space Layout Randomization (ASLR) (2 for default)
sudo sysctl -w kernel.randomize_va_space=0

# check the randomization status
sudo sysctl kernel.randomize_va_space

# compile call_sh to test if the shellcode is correct
# refer to https://gcc.gnu.org/onlinedocs/gcc for more details about gcc options
# -Wall for useful warning
# -g for gdb
# -m32 for 32-bit assembly
# -z execstack for executable shellcode
# -fno-stack-protector for turning off compiler protector
gcc -Wall -g -m32 -z execstack -o call_sh_32 call_sh_32.c
./call_sh_32

# turn on “non executable stack” countermeasure (supported by hardware) to see the change
gcc -Wall -g -m32 -o call_sh_32_safe call_sh_32.c
./call_sh_32_safe

# compile the vulnerable program stack
gcc -Wall -g -m32 -fno-stack-protector -o stack_32 stack.c
# gcc -Wall -g -fno-stack-protector -o stack_64 stack.c

# test slack with an empty badfile
touch badfile
./stack
```

## Write shellcode (optional)

Shellcode to launch a shell has been provided in call_sh_32.c. If you are interested in how the shellcode is written, please refer to generate_shellcode.ipynb or [Writing shellcode for Linux and \*BSD](http://www.kernel-panic.it/security/shellcode/index.html)

## Find the offset and the address of stack frame (ebp or rbp)

Use debugger **gdb** to get `&buffer` and `$ebp`(`$rbp` if 64-bit),

!!! note: _VS Code_ is not recommend which will re-compile the source code.

!!! note: Please ensure the badfile is empty when debugging stack

```bash
# enter gdb, use -n to close peda, use -q to remove copyright message
gdb -n -q stack_32

# gdb commands
b unsafe_copy # insert a breakpoint in unsafe_copy()
r # run
n # !!! note: step inside unsafe_copy()
p system
x/s *(char**)environ # get the address of "/bin/sh", see https://visualgdb.com/gdbreference/commands/x for usage of x
p &target_str
p $ebp # # frame pointer of main function
c # run remaining code
q # quit
```

or you can directly run the following command.

```bash
gdb -n -q -x gdb_get_infos.txt stack_32
```

## Attack stack

```bash
/usr/bin/python3 exploit.py # generate badfile
gdb -n -q -x gdb_run.txt stack_32

sudo chown root stack_32 && sudo chmod 4755 stack_32
gdb -n -q -x gdb_run.txt stack_32
```
