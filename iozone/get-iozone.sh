#!/bin/bash
# Downloads IOZone and unpacks it into ioz/.

url="https://www.iozone.org/src/current/iozone3_492.tgz"
fname1="$(basename ${url})"
fname2="ioz"

# check for the command-line argument - the destination location
dpath=./
if [ $# -lt 1 ]; then
    echo "Usage: $0 /path/to/extract_destination"
    exit 1
fi
dpath=$1

# download the file and move it
wget ${url}
if [ ! -f ./${fname1} ]; then
    echo "Failed to download."
    exit 1
fi

# unpack and rename
tar -xf ./${fname1}
mv ./${fname1%.*} ${dpath}/${fname2}
rm ./${fname1}

