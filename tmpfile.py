#!/usr/bin/env python3

from pathlib import Path
import os
import tempfile


def mode_to_oct(mode):
    return int(oct(mode)[3:])  # only care about last four digits


RAMFS_MOUNT = os.getenv('RAMFS_MOUNT')
assert RAMFS_MOUNT is not None, 'RAMFS_MOUNT undeclared. Failure.'
assert Path(RAMFS_MOUNT).exists(), 'RAMFS_MOUNT does not exist in FS. Failure.'

ramfs_mnt = Path(RAMFS_MOUNT)
os.chdir(ramfs_mnt)

with tempfile.TemporaryFile() as file:
    file.write(b'a')
    file.flush()
    file.seek(0)
    a = file.read()
    assert a == b'a', 'tmpfile readwrite broken. Failure.'

with tempfile.NamedTemporaryFile() as file:
    file.write(b'a')
    file.flush()
    file.seek(0)
    a = file.read()
    assert a == b'a', 'tmpfile readwrite broken. Failure.'

    # looking at the Python source code 600 is the permission used
    # in the Python source code for tempfile, not sure if this changes
    # between versions, but it makes sense as 600 is write and read only
    # for users only (which makes this a more secure to use file)
    assert mode_to_oct(Path(file.name).stat().st_mode) == 600, \
        'tmpfile perms wrong. Failure.'
