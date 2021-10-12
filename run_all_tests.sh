#!/usr/bin/bash

export RAMFS_MOUNT='/tmp/mount'

run_test() {
  echo "---------------------------------------------------"
  echo "Running... $*"

  "$@"

  if [[ $? -ne 0 ]]; then
    echo "Failed..."
  else
    echo "Success..."
  fi

  echo "---------------------------------------------------"
  echo
}

mount -t ramfs -o size=1m ramfs "${RAMFS_MOUNT}"

run_test python3 /rust_test_scripts/mknod.py

umount "${RAMFS_MOUNT}"
