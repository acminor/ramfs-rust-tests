#!/usr/bin/env python3

from pathlib import Path
import time
import os

RAMFS_MOUNT = os.getenv('RAMFS_MOUNT')
assert RAMFS_MOUNT is not None, 'RAMFS_MOUNT undeclared. Failure.'
assert Path(RAMFS_MOUNT).exists(), 'RAMFS_MOUNT does not exist in FS. Failure.'

ramfs_mnt = Path(RAMFS_MOUNT)

mknod_dir = ramfs_mnt / '__mknode__'
mknod_dir.mkdir()

assert mknod_dir.exists(), 'mkdir failed'
start_stat = mknod_dir.stat()

# sleep to make sure we do not run into a clock accuracy is low issue
# - which would make both times appear to be the same
time.sleep(0.2)

mknod_file = mknod_dir / '__file__'
mknod_file.touch(exist_ok=False)

assert mknod_file.exists(), 'touch failed'
end_stat = mknod_dir.stat()

assert start_stat.st_ctime_ns < end_stat.st_ctime_ns, 'Time not updated correctly'
assert start_stat.st_mtime_ns < end_stat.st_mtime_ns, 'Time not updated correctly'
assert end_stat.st_mtime_ns == end_stat.st_mtime_ns, 'Time not updated correctly'

# clean-up
mknod_file.unlink()
mknod_dir.rmdir()
