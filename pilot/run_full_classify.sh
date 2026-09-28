#!/bin/zsh
cd "$(dirname "$0")"
export PILOT_DATA=data_full
echo "retrying failed downloads..."
../.venv/bin/python rescue_pilot.py fetch --workers 4 > data_full/retry.log 2>&1
tail -1 data_full/retry.log
echo "classifying every file..."
../.venv/bin/python rescue_pilot.py classify 2>&1 | grep --line-buffered -v -i warn
../.venv/bin/python rescue_pilot.py report > data_full/REPORT.txt 2>&1
echo "ALL DONE"
