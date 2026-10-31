"""Lesson 6 live cost guard (amended after run B1, before B2: out/l6/prereg.json "amendments"). The same estimate as
costguard.py (the container's Claude Code session log: tokens x list prices x 0.683), sampled every 4 s. Above SOFT it
presses Esc once in Claude Code's terminal (Claude stops; the run goes on, filmed, read and sent by our script) and
leaves /tmp/guard-stopped in the container; above HARD it kills the container (a backstop).
    python costguard6.py SOFT HARD CONTAINER"""
import json
import subprocess
import sys
import time

SOFT, HARD, NAME = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
SCALE = 0.683


def est():
    p = subprocess.run(['docker', 'exec', NAME, 'bash', '-c', 'cat /root/.claude/projects/*/*.jsonl 2>/dev/null'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    u = {'in': 0, 'cw': 0, 'cr': 0, 'out': 0}
    seen = set()
    for line in p.stdout.splitlines():
        try:
            r = json.loads(line)
        except ValueError:
            continue
        m = r.get('message') or {}
        us = m.get('usage') if isinstance(m, dict) else None
        if not us or m.get('id') in seen:
            continue
        seen.add(m.get('id'))
        u['in'] += us.get('input_tokens', 0)
        u['cw'] += us.get('cache_creation_input_tokens', 0)
        u['cr'] += us.get('cache_read_input_tokens', 0)
        u['out'] += us.get('output_tokens', 0)
    return SCALE * (u['in'] * 3 + u['cw'] * 3.75 + u['cr'] * 0.30 + u['out'] * 15) / 1e6, u


def running():
    return NAME in subprocess.run(['docker', 'ps', '--format', '{{.Names}}'], capture_output=True, text=True).stdout.split()


last, soft_done = None, False
while True:
    if not running():
        print('container gone; last estimate', last and round(last, 4), flush=True)
        break
    last, u = est()
    print(time.strftime('%H:%M:%S'), round(last, 4), u, flush=True)
    if last > HARD:
        print('GUARD: over', HARD, '-> docker kill', flush=True)
        subprocess.run(['docker', 'kill', NAME])
        break
    if last > SOFT and not soft_done:
        print('GUARD: over', SOFT, '-> Esc in Claude Code (soft stop)', flush=True)
        subprocess.run(['docker', 'exec', NAME, 'bash', '-c', 'touch /tmp/guard-stopped; tmux send-keys -t cc Escape'])
        soft_done = True
    time.sleep(4)
