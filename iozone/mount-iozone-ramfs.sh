#!/bin/bash

mname="ramfs"
mdir=$(dirname $(realpath $0))/${mname}

# create the mounting point if it doesn't exit
if [ ! -d ${mdir} ]; then
    mkdir ${mdir}
fi

# mount it!
mount -t ramfs -o size=2G ramfs ${mdir}

