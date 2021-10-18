#!/usr/bin/env python3

from pathlib import Path
import subprocess as sp
import os
import stat
import shlex


def mode_to_oct(mode):
    return int(oct(mode)[3:])  # only care about last four digits


# NOTE: for now just test that new files have the correct default mode
RAMFS_DEFAULT_MODE = 755  # 0755

RAMFS_MOUNT = os.getenv('RAMFS_MOUNT')
assert RAMFS_MOUNT is not None, 'RAMFS_MOUNT undeclared. Failure.'
assert Path(RAMFS_MOUNT).exists(), 'RAMFS_MOUNT does not exist in FS. Failure.'

ramfs_mnt = Path(RAMFS_MOUNT)
mnt_stat = ramfs_mnt.stat()
mnt_perms = mode_to_oct(mnt_stat.st_mode)

assert mnt_perms == RAMFS_DEFAULT_MODE, "directory default mode is wrong"
