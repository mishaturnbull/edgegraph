#!/bin/bash

if [ ! -e dist ]
then
    rm -rf dist
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

python -m build
twine upload dist/*

