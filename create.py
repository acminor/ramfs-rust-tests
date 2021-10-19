#!/usr/bin/env python3

# A simple python script to test ramfs_create().
# ramfs_create() is invoked when a regular file (not a directory) is created.
#
#   Connor Shugg

from pathlib import Path
import os

# grab the process' umask so we know what file permissions *should* be when
# creating new files
umask = os.umask(0)
os.umask(umask)

# Helper function that checks file permissions and returns a pair:
#   [expected, actual]
def check_perms(requested, actual):
    # take what was requested and compute what should have been created,
    # based on the umask
    expected = requested & (~umask)
    # extract the low 9 bits from the stat st_mode result (actual)
    actual_lowbits = actual & 0x1ff
    return [expected, actual_lowbits]

# attempt to find the RAMFS_MOUNT environment variable
mount = os.getenv("RAMFS_MOUNT")
assert mount is not None, "RAMFS_MOUNT undeclared. Failure."
mpath = Path(mount)
assert mpath, "RAMFS_MOUNT doesn't exist. Failure."

# TEST 1: regular file 1
fpath = mpath / "ramfs_create_test_empty1"
requested_perms = 0o777
fpath.touch(mode=requested_perms, exist_ok=False)

assert fpath.exists(), "TEST 1: touch failed."
fstat = fpath.stat()
perms = check_perms(requested_perms, fstat.st_mode)
assert perms[0] == perms[1], "TEST 1: expected 0o%o, found 0o%o" % (perms[0], perms[1])

# TEST 2: regular file 2
fpath = mpath / "ramfs_create_test_empty2"
requested_perms = 0o644
fpath.touch(mode=requested_perms, exist_ok=False)

assert fpath.exists(), "TEST 2: touch failed."
fstat = fpath.stat()
perms = check_perms(requested_perms, fstat.st_mode)
assert perms[0] == perms[1], "TEST 2: expected 0o%o, found 0o%o" % (perms[0], perms[1])


