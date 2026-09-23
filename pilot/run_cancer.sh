#!/bin/zsh
# usage: run_cancer.sh "breast cancer"   -> pilot/data_breast_cancer/
set -e
cd "$(dirname "$0")"
C="$1"; D="data_$(echo "$C" | tr ' ' '_')"
export PILOT_DATA="$D"
mkdir -p "$D"
../.venv/bin/python rescue_pilot.py sample --cancer "$C" --n 300 --seed 20260923
../.venv/bin/python rescue_pilot.py fetch --workers 6
../.venv/bin/python rescue_pilot.py classify
../.venv/bin/python rescue_pilot.py report > "$D/REPORT.txt"
echo "DONE $C"
