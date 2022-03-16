# Race Condition Attack

## Step 1: Compile the vulnerable and attack programs

```bash
sudo sysctl -w fs.protected_symlinks=0

sudo sysctl fs.protected_regular

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
./target_process.sh
```

## Step 3: Improved attack

```bash
sudo cp /etc/passwd.original /etc/passwd
gcc -o new_attack_process new_attack_process.c
```
