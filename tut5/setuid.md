# setuid

When the **setuid** or **setgid** attributes are set on an executable file, then any users able to execute the file will automatically execute the file with the privileges of the file's owner (commonly root) and/or the file's group, depending upon the flags set. This allows the system designer to permit trusted programs to be run which a user would otherwise not be allowed to execute. Refer to [setuid](https://en.wikipedia.org/wiki/Setuid) for details.

```bash
# copy file cat
cp /bin/cat mycat

# change owner
sudo chown root mycat

# show current previledge
# should be `-rwxr-xr-x 1 root seed`
ls -l

# test if mycat can show content of /etc/shadow
# should be no
./mycat /etc/shadow

# set setuid flag
sudo chmod 4755 mycat

# test if mycat can show content of /etc/shadow
# should be yes now
./mycat /etc/shadow

# check effective uid (euid)
cp /bin/id myid
sudo chown root myid && sudo chmod 4755 myid
./myid
```
