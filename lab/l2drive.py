"""L2-Q4: drive one Claude Code session in its real terminal (tmux inside an xterm on the filmed display).
It types each message the way a person would (one character at a time into the TUI), presses Enter, then only waits:
it reads the screen (tmux capture-pane) to see when Claude is working or asks for an approval (answered with the
prompt's own "Yes"), and tails the logging proxy's transcript to mark each tool call. Events go to events.jsonl in
seconds since the recording started (T0), so the footage can be cut by event.
No mouse input is needed for the window to show Claude's changes: in 0.25.0 a change through the plug repaints the window
by itself (lab out/l2/probe/repaint.json). L2_NUDGE=1 would move the mouse a few pixels over the viewport while a turn
runs (off by default; each turn logs its nudge count, 0 when off).
    python3 l2drive.py RUN_DIR T0_EPOCH "message 1" ["message 2" ...]"""
import json
import math
import os
import subprocess
import sys
import time
from datetime import datetime

sys.path.insert(0, '/work')
from client import tui  # noqa: E402

PANE = 'cc'
TURN_LIMIT_S = 420
QUIET_S = 4.0
NUDGE_AT = (1330, 640)
NUDGE_R = 5


def pane(full=False):
    a = ['tmux', 'capture-pane', '-p', '-t', PANE] + (['-S', '-3000'] if full else [])
    return subprocess.run(a, capture_output=True, text=True).stdout


def keys(*k, literal=False):
    subprocess.run(['tmux', 'send-keys', '-t', PANE] + (['-l'] if literal else []) + list(k), check=True)


class Run:
    def __init__(self, out, t0):
        self.out, self.t0 = out, t0
        self.ev = open(os.path.join(out, 'events.jsonl'), 'a')
        self.tpath = os.path.join(out, 'transcript.jsonl')
        self.tpos = 0
        self.calls = {}

    def mark(self, what, **kw):
        row = {'t': round(time.time() - self.t0, 3), 'event': what}
        row.update(kw)
        self.ev.write(json.dumps(row) + '\n')
        self.ev.flush()

    def tail(self):
        """New proxy rows: mark tools/call requests and their replies (with the proxy's own UTC time)."""
        if not os.path.exists(self.tpath):
            return
        with open(self.tpath, encoding='utf-8') as f:
            f.seek(self.tpos)
            for line in f:
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                m = r.get('msg')
                if not isinstance(m, dict):
                    continue
                t = datetime.fromisoformat(r['t']).timestamp() - self.t0
                if r.get('dir') == 'client->server' and m.get('method') == 'tools/call':
                    name = (m.get('params') or {}).get('name')
                    self.calls[m.get('id')] = name
                    self.ev.write(json.dumps({'t': round(t, 3), 'event': f'tool call: {name}', 'seq': r.get('seq')}) + '\n')
                elif r.get('dir') == 'server->client' and m.get('id') in self.calls:
                    name = self.calls.pop(m.get('id'))
                    err = bool((m.get('result') or {}).get('isError')) or 'error' in m
                    self.ev.write(json.dumps({'t': round(t, 3), 'event': f'tool reply: {name}', 'seq': r.get('seq'),
                                              'isError': err}) + '\n')
            self.tpos = f.tell()
        self.ev.flush()

    def say(self, n, msg):
        self.mark(f'turn {n}: typing')
        for ch in msg:
            keys(ch, literal=True)
            time.sleep(0.045)
        time.sleep(0.8)
        done_before = tui.turns_done(pane(full=True))
        self.mark(f'turn {n}: Enter')
        keys('Enter')
        start, seen_busy, quiet_since, approvals, nudges = time.time(), False, None, 0, 0
        while time.time() - start < TURN_LIMIT_S:
            time.sleep(0.4)
            if os.environ.get('L2_NUDGE') == '1':
                a = nudges * 0.7
                subprocess.run(['xdotool', 'mousemove', str(round(NUDGE_AT[0] + NUDGE_R * math.cos(a))),
                                str(round(NUDGE_AT[1] + NUDGE_R * math.sin(a)))])
                nudges += 1
            self.tail()
            text = pane()
            if tui.approval(text):
                k = tui.approval_key(text)
                self.mark(f'turn {n}: approval asked', key=k)
                open(os.path.join(self.out, f'approval-{n}-{approvals + 1}.txt'), 'w').write(text)
                time.sleep(1.5)
                keys(k)
                approvals += 1
                quiet_since = None
                continue
            if tui.turns_done(pane(full=True)) > done_before and not self.calls:
                self.mark(f'turn {n}: end-of-turn line seen')
                time.sleep(2.0)
                break
            if tui.busy(text):
                if not seen_busy:
                    self.mark(f'turn {n}: Claude working')
                seen_busy, quiet_since = True, None
            elif seen_busy and not self.calls:
                quiet_since = quiet_since or time.time()
                if time.time() - quiet_since >= QUIET_S:
                    break
        self.tail()
        self.mark(f'turn {n}: reply done', approvals=approvals, mouse_nudges=nudges,
                  timed_out=time.time() - start >= TURN_LIMIT_S)
        open(os.path.join(self.out, f'pane-turn{n}.txt'), 'w').write(pane())


def main(out, t0, messages):
    r = Run(out, t0)
    for i, m in enumerate(messages, 1):
        r.say(i, m)
        time.sleep(3.0)
    open(os.path.join(out, 'pane-full.txt'), 'w').write(pane(full=True))


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3:])
