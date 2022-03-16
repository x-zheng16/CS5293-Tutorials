# Race Condition Attack

## Questions after tut8

1. `sudo ln -sf /bin/zsh /bin/sh` does not take effect. You should log out and log in to make the default shell changed.

2. Notice the buffer name. Sometimes it is not `buffer` but `target_str` or something.

3. Hints on Task 4.5 in Assignment 2. X stands for the offset of the first argument of `system()`. Y is the offset of the return address of `unsafe_copy()`. And Z is optional, which should be the offset of the return address of `system()`

## Step 1: Compile the vulnerable and attack programs

```bash
sudo sysctl -w fs.protected_symlinks=0

# sudo sysctl fs.protected_regular

sudo cp /etc/passwd /etc/passwd.original

gcc -o vulp vulp.c
sudo chown root vulp && sudo chmod 4755 vulp

gcc -o test_symlink test_symlink.c
gcc -o test_unlink test_unlink.c
gcc -o attack_process attack_process.c
```

## Step 2: Launch the attack

In Terminal 1, run

```bash
./attack_process
```

In Terminal 2, run

```bash
bash target_process.sh
```

## Step 3: Improved attack

```bash
sudo cp /etc/passwd.original /etc/passwd
gcc -o new_attack_process new_attack_process.c
```
