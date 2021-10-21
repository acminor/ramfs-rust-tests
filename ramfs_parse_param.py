import contextlib
import subprocess as sp
import os
import shlex
from pathlib import Path

RAMFS_MOUNT = Path(os.getenv('RAMFS_MOUNT')) / Path('test_mount')


def mode_to_oct(mode):
    return int(oct(mode)[3:])  # only care about last four digits


class MountManager(contextlib.AbstractContextManager):
    def __init__(self, parameters):
        self.parameters = parameters

    def mount(self):
        sp.run(shlex.split(f'mkdir -p "{RAMFS_MOUNT}"'))

        if self.parameters:
            res = sp.run(shlex.split(f'mount -t ramfs -o {",".join(self.parameters)} ramfs "{RAMFS_MOUNT}"'),
                         stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            res = sp.run(shlex.split(f'mount -t ramfs ramfs "{RAMFS_MOUNT}"'), stdout=sp.PIPE, stderr=sp.PIPE)

        if res.returncode != 0:
            raise Exception('')

    @staticmethod
    def umount():
        sp.run(shlex.split(f'umount "{RAMFS_MOUNT}"'))
        sp.run(shlex.split(f'rm -rf "{RAMFS_MOUNT}"'))

    def __enter__(self):
        self.mount()

        return super().__enter__()

    def __exit__(self, __exc_type, __exc_value, __traceback):
        self.umount()

        return super().__exit__(__exc_type, __exc_value, __traceback)


DEFAULT_MODE = 755
with MountManager([]):
    mode = mode_to_oct(RAMFS_MOUNT.stat().st_mode)
    assert mode == DEFAULT_MODE, 'default mode is not set correctly'

with MountManager(['mode=755']):
    mode = mode_to_oct(RAMFS_MOUNT.stat().st_mode)
    assert mode == 755, 'mode is not set correctly'

with MountManager(['mode=644']):
    mode = mode_to_oct(RAMFS_MOUNT.stat().st_mode)
    assert mode == 644, 'mode is not set correctly'

exception = False
try:
    with MountManager(['mode=888']):
        pass
except:
    exception = True
assert exception, 'exception was not thrown for invalid mode parameter'

with MountManager(['mode=777,size=10m,unknown=3,something=5']):
    mode = mode_to_oct(RAMFS_MOUNT.stat().st_mode)
    assert mode == 777, 'mode is not set correctly when having other unknown parameters'
