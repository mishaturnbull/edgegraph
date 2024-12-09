#!/bin/bash

if [ -z "$1" ]
then
    echo "Must specify an argument; can be 'real' or 'test'."
    exit 1
fi

if [ -e lib ]
then
    echo "ERROR: lib/ exists.  This is *probably* from PyVis output usage"
    echo "(it creates this folder for JavaScript libraries), but I don't want"
    echo "to remove it automatically.  It will prevent the build process from"
    echo "running correctly -- save any important contents in that folder,"
    echo "remove it, then retry the build."
    exit 1
fi
if [ -e prof ]
then
    echo "ERROR: prof/ exists.  This is *probably* from running profile unit"
    echo "tests; but I don't want to remove it automatically.  It will prevent"
    echo "the build process from running correctly -- save any contents in"
    echo "that folder, remove it, then retry the build."
    exit 1
fi

python -m build

if [ "$(ls -1b dist | wc -l)" -gt 2 ]
then
    echo
    echo "ERROR: more than 2 files detected in dist/ !  This likely means an"
    echo "old build is still lurking around.  Please clean the directory; I"
    echo "will not attempt to upload with old files potentially present."
    echo
    ls -lah dist
    exit 1
fi


timeout=20
echo
echo
echo "Build complete and ready for upload! I will wait for $timeout seconds"
echo "before uploading; use ctrl-C to interrupt.  The following files will"
echo "be uploaded:"
echo
ls -lh dist

echo
echo
if [ $1 = "real" ]
then
    echo "+-----------------------------------------------------------+"
    echo "| +-------------------------------------------------------+ |"
    echo "| | These files will be uploaded to the REAL PyPI repo!!! | |"
    echo "| +-------------------------------------------------------+ |"
    echo "+-----------------------------------------------------------+"

elif [ $1 = "test" ]
then
    echo "These files will be uploaded to the testing PyPi repo."
else
    echo "Unrecognized repository specifier '$1'; aborting."
    echo "Valid options are 'real' or 'test'."
    exit 1
fi

echo
echo
(
    while [[ $timeout -gt 0 ]]; do
        echo -n "$timeout "
        sleep 1
        timeout=$(( timeout - 1 ))
    done
)
echo
echo
echo "Beginning upload!!"
echo

if [ $1 = "real" ]
then
    python -m twine upload dist/*
elif [ $1 = "test" ]
then
    python -m twine upload --repository testpypi dist/*
fi

