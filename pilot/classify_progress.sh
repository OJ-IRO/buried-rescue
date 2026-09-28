#!/bin/zsh
# Live progress for the full-corpus classification: which paper it is on, out of how many, and elapsed time.
cd "$(dirname "$0")"
ORDER=$(../.venv/bin/python -c "import json;print('\n'.join(json.load(open('data_full/fetch_log.json')).keys()))")
TOTAL=$(echo "$ORDER" | wc -l | tr -d ' ')
PID=$(pgrep -f 'rescue_pilot.py classify' | head -1)
[ -z "$PID" ] && { echo "Classification is not running (finished or not started)."; exit 0; }
START=$(ps -o lstart= -p $PID)
echo "Classifying all attachments. Started: $START"
while kill -0 $PID 2>/dev/null; do
  CUR=$(lsof -p $PID 2>/dev/null | grep -o 'PMC[0-9]*\.zip' | tail -1 | sed 's/\.zip//')
  if [ -n "$CUR" ]; then N=$(echo "$ORDER" | grep -n -x "$CUR" | cut -d: -f1); PCT=$(( N * 100 / TOTAL ))
    ELAPSED=$(ps -o etimes= -p $PID | tr -d ' '); ETA=$(( N > 0 ? ELAPSED * (TOTAL - N) / N / 60 : 0 ))
    printf "\r%s  paper %s of %s  (%s%%)  elapsed %sm  est. %sm left      " "$(date +%H:%M:%S)" "$N" "$TOTAL" "$PCT" "$((ELAPSED/60))" "$ETA"
  fi
  sleep 5
done
echo; echo "Classification finished."
