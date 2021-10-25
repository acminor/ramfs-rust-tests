#!/usr/bin/env python3

# A simple python test script to test ramfs_symlink().
# ramfs_symlink() is invoked when a symbolic link file is made.
#
#   Connor Shugg

# https://docs.python.org/3/library/pathlib.html 
from pathlib import Path
import os
import subprocess

# retrieve process' umask
umask = os.umask(0)
os.umask(umask)

# Helper that takes in the file permissions *requested* by fpath.touch()
# and uses the umask found above to return a pair of permissions for
# comparison:
#   [expected, actual]
def get_perms(requested, actual):
    # take what was requested and compute what should have been created,
    # based on the umask
    expected = requested & (~umask)
    # extract the low 9 bits from the stat st_mode result (actual)
    actual_lowbits = actual & 0x1ff
    return [expected, actual_lowbits]

# find the ramfs mounting point
mount = os.getenv("RAMFS_MOUNT")
assert mount is not None, "RAMFS_MOUNT undeclared. Failure."
mpath = Path(mount)
assert mpath.exists(), "RAMFS_MOUNT: %s doesn't exist. Failure." % mpath

# for simplicity's sake, we'll assume there are binaries at '/bin/ls' and '/bin/echo'
ls_bin = Path("/bin/ls")
echo_bin = Path("/bin/echo")

# TEST 1: link to ls
lpath = mpath / "ls-link1"
lpath.symlink_to(ls_bin)

assert lpath.exists(), "TEST 1: symlink failed."
lstat = lpath.stat()
perms = get_perms(0o777, lstat.st_mode)
assert perms[0] == perms[1], "TEST 1: symlink permissions are incorrect: 0o%o vs 0o%o" % (perms[0], perms[1])
completed_proc = subprocess.run(str(lpath), stdout=subprocess.DEVNULL)
assert completed_proc.returncode == 0, ("TEST 1: executing %s failed. (return code = %d)" %
                                        (lpath, completed_proc.returncode))

# TEST 2: link to echo
lpath = mpath / "echo-link1"
lpath.symlink_to(echo_bin)
assert lpath.exists(), "TEST 1: symlink failed."
lstat = lpath.stat()
perms = get_perms(0o777, lstat.st_mode)
assert perms[0] == perms[1], "TEST 1: symlink permissions are incorrect: 0o%o vs 0o%o" % (perms[0], perms[1])
completed_proc = subprocess.run([str(lpath), "echo-test"], stdout=subprocess.DEVNULL)
assert completed_proc.returncode == 0, ("TEST 2: executing %s failed. (return code = %d)" %
                                        (lpath, completed_proc.returncode))



