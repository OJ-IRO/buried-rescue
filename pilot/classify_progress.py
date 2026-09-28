#!/usr/bin/env python3
"""Live progress for the full-corpus classification (macOS)."""
import json, os, re, subprocess, sys, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))
order = list(json.load(open("data_full/fetch_log.json")).keys()); pos = {p: i + 1 for i, p in enumerate(order)}; total = len(order)
def pid():
    out = subprocess.run(["pgrep", "-f", "[Pp]ython.*rescue_pilot.py classify"], capture_output=True, text=True).stdout.split()
    return out[0] if out else None
p = pid()
if not p: print("Classification is not running (finished or not started)."); sys.exit()
t0 = time.time() - 0; last = 0
print(f"Classifying attachments of {total:,} papers. Updates every 5 seconds. Ctrl-C closes this view only.\n")
while pid():
    lsof = subprocess.run(["lsof", "-p", p], capture_output=True, text=True).stdout
    m = re.findall(r"(PMC\d+)\.zip", lsof)
    if m: last = max(last, pos.get(m[-1], 0))
    et = subprocess.run(["ps", "-o", "etime=", "-p", p], capture_output=True, text=True).stdout.strip()
    parts = [int(x) for x in re.split(r"[-:]", et)] if et else [0]
    secs = sum(v * m for v, m in zip(reversed(parts), [1, 60, 3600, 86400]))
    eta = int(secs * (total - last) / last / 60) if last else 0
    bar = "#" * int(30 * last / total) + "-" * (30 - int(30 * last / total))
    print(f"\r{time.strftime('%H:%M:%S')}  [{bar}] paper {last:,} of {total:,} ({100*last//total}%)  elapsed {secs//60}m  about {eta}m left   ", end="", flush=True)
    time.sleep(5)
print("\n\nClassification finished.")
