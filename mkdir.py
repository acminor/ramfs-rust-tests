#!/usr/bin/env python3

# A simple python test script to test ramfs_mkdir().
# ramfs_mkdir() is invoked when a directory file is created.
#
#   Connor Shugg

from pathlib import Path
import os

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

# TEST 1: directory 1
dpath = mpath / "ramfs_mkdir_test1"
req_perms = 0o777
dpath.mkdir(mode=req_perms)

assert dpath.exists(), "TEST 1: mkdir failed."
dstat = dpath.stat()
perms = get_perms(req_perms, dstat.st_mode)
assert perms[0] == perms[1], "TEST 1: expected 0o%o, found 0o%o" % (perms[0], perms[1])

# TEST 2: directory 2
dpath = mpath / "ramfs_mkdir_test2"
req_perms = 0o642
dpath.mkdir(mode=req_perms)

assert dpath.exists(), "TEST 2: mkdir failed."
dstat = dpath.stat()
perms = get_perms(req_perms, dstat.st_mode)
assert perms[0] == perms[1], "TEST 2: expected 0o%o, found 0o%o" % (perms[0], perms[1])

