#!/bin/bash
# Requirements:
# - Poetry 2.3 or later
# - poetry-plugin-export

for i in versions/*; do
    pushd $i
    poetry lock
    # After we drop Python 3.9, consider switching to pylock.toml format.
    # (pip 26.1 added pylock.toml support, but it also dropped Python 3.9 support.)
    poetry export -o requirements.txt
    popd
done