#!/bin/bash

echo Working directory: ${pwd}

if [ -d "prof" ]
then
    rm -rf prof
fi

if [ -e "docs/_build/combined.svg" ]
then
    rm docs/_build/combined.svg
fi

python3 -m pytest \
    --profile-svg \
    -m perf \
    -o log_cli=true \
    -vv

mv prof/combined.svg docs/_build/

echo Done!

