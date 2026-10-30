import json, subprocess, sys, time
LIMIT = float(sys.argv[1]); SCALE = 0.683; NAME = 'sc4-claude'
def est():
    p = subprocess.run(['docker', 'exec', NAME, 'bash', '-c', 'cat /root/.claude/projects/*/*.jsonl 2>/dev/null'], capture_output=True, text=True, encoding='utf-8', errors='replace')
    u = {'in': 0, 'cw': 0, 'cr': 0, 'out': 0}; seen = set()
    for l in p.stdout.splitlines():
        try: r = json.loads(l)
        except Exception: continue
        m = r.get('message') or {}
        us = m.get('usage') if isinstance(m, dict) else None
        if not us or m.get('id') in seen: continue
        seen.add(m.get('id'))
        u['in'] += us.get('input_tokens', 0); u['cw'] += us.get('cache_creation_input_tokens', 0)
        u['cr'] += us.get('cache_read_input_tokens', 0); u['out'] += us.get('output_tokens', 0)
    return SCALE * (u['in'] * 3 + u['cw'] * 3.75 + u['cr'] * 0.30 + u['out'] * 15) / 1e6
while True:
    running = NAME in subprocess.run(['docker', 'ps', '--format', '{{.Names}}'], capture_output=True, text=True).stdout.split()
    if not running:
        print('container gone; last estimate', round(last, 4) if 'last' in dir() else None); break
    last = est()
    print(time.strftime('%H:%M:%S'), round(last, 4), flush=True)
    if last > LIMIT:
        print('GUARD: over', LIMIT, '-> docker kill', flush=True)
        subprocess.run(['docker', 'kill', NAME]); break
    time.sleep(8)
