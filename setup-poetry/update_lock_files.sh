#!/bin/bash
# Requirements:
# - Poetry 2.3 or later
# - poetry-plugin-export

for i in versions/*; do
    pushd $i
    poetry lock
    poetry export -f pylock.toml -o pylock.toml
    popd
done