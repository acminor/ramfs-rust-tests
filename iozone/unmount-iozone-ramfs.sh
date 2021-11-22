#!/bin/bash

mname="ramfs"
mdir=$(dirname $(realpath $0))/${mname}

# ummount it!
umount ${mdir}

# remove the directory
rm -rf ${mdir}

