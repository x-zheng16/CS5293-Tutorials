# Hands-on Stack-based Buffer Overflow

## Setup Lab Environment

```bash
# install python3
sudo apt install python3 python3-dev

# use bash or zsh as sh
sudo ln -sf /bin/zsh /bin/sh

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
gcc -Wall -g -m32 -z execstack -fno-stack-protector -o call_sh_32 call_sh_32.c

# launch a shell
./call_sh_32

# compile the vulnerable program stack
gcc -Wall -g -m32 -z execstack -fno-stack-protector -o stack_32 stack.c

# test slack with an empty badfile
touch badfile
./stack
```

## Write shellcode (optional)

Shellcode to launch a shell has been provided in call_sh_32.c. If you are interested in how the shellcode is written, please refer to generate_shellcode.ipynb or [Writing shellcode for Linux and \*BSD](http://www.kernel-panic.it/security/shellcode/index.html)

## Find the offset and the address of stack frame (ebp or rbp)

Use debugger **gdb** to get `&buffer` and `$ebp`(`$rbp` if 64-bit).

!!! note: _VS Code_ is not recommend which will re-compile the source code.

!!! note: Please ensure the badfile is empty when debugging stack

```bash
# enter gdb, use -n to close peda, use -q to remove copyright message
gdb -nh -q stack_32

# gdb commands
b unsafe_copy # insert a breakpoint in unsafe_copy()
r # run
n # !!! note: step inside unsafe_copy()
info locals # check local variables
p &target_str
p $ebp # # frame pointer of main function
continue # run remaining code
q # quit
```

## Attack stack

```python
/usr/bin/python3 exploit.py # generate badfile
```

Please try the following methods to see the difference.

### launch attack in shell

```bash
./stack_32
whoami
id
exit

# change stack into a set-uid program
sudo chown root stack_32 && sudo chmod 4755 stack_32

# re-run stack to see the change of the shell owner
./stack_32
whoami
id
```

### launch attack in gdb

```bash
gdb -nh -q stack_32

# gdb commands
r
```
