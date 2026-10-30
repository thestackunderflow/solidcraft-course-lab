"""L4-Q6: lesson 2's Claude Code driver (l2drive.Run: types each message into the real TUI, answers approvals with
the prompt's own "Yes", marks every tool call) with lesson 4's one pre-registered extra: if message 1's turn changed
nothing (no execute or batch call logged: Claude asked a question instead of acting), it sends the fixed answer "Your
choice." once (turn "1b") before message 2. Amended after run A1 (out/l4/prereg.json "amendments"): the first trigger,
"no solid.hole call", fired on A1, which had cut its holes with a sketch and an extrude.
    python3 l4drive.py RUN_DIR T0_EPOCH "message 1" "message 2\""""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l2drive as d  # noqa: E402
import re  # noqa: E402
from client import tui  # noqa: E402

LINE = re.compile(r'[A-Z]\w+ for [0-9hms ]+· done [0-9:]+ ?[AP]?M?')


def last_done(text):
    """The newest end-of-turn line on the screen (Claude Code redraws its history, so older ones can vanish and a
    count of them may never go up: run A1's turn 2 waited for the time-out)."""
    m = LINE.findall(text or '')
    return (len(m), m[-1] if m else None)


class Run(d.Run):
    def say(self, n, msg):
        """l2drive.Run.say with one change: the turn is over when the newest end-of-turn line changes."""
        self.mark(f'turn {n}: typing')
        for ch in msg:
            d.keys(ch, literal=True)
            time.sleep(0.045)
        time.sleep(0.8)
        before = last_done(d.pane(full=True))
        self.mark(f'turn {n}: Enter')
        d.keys('Enter')
        start, seen_busy, quiet_since, approvals = time.time(), False, None, 0
        while time.time() - start < d.TURN_LIMIT_S:
            time.sleep(0.4)
            self.tail()
            text = d.pane()
            if tui.approval(text):
                k = tui.approval_key(text)
                self.mark(f'turn {n}: approval asked', key=k)
                open(os.path.join(self.out, f'approval-{n}-{approvals + 1}.txt'), 'w').write(text)
                time.sleep(1.5)
                d.keys(k)
                approvals += 1
                quiet_since = None
                continue
            now = last_done(d.pane(full=True))
            if now[1] and now != before and not self.calls:
                self.mark(f'turn {n}: end-of-turn line seen')
                time.sleep(2.0)
                break
            if tui.busy(text):
                if not seen_busy:
                    self.mark(f'turn {n}: Claude working')
                seen_busy, quiet_since = True, None
            elif seen_busy and not self.calls:
                quiet_since = quiet_since or time.time()
                if time.time() - quiet_since >= d.QUIET_S:
                    break
        self.tail()
        self.mark(f'turn {n}: reply done', approvals=approvals, mouse_nudges=0,
                  timed_out=time.time() - start >= d.TURN_LIMIT_S)
        open(os.path.join(self.out, f'pane-turn{n}.txt'), 'w').write(d.pane())

ANSWER = 'Your choice.'


def build_calls(path):
    """tools/call requests that can change the design (execute or batch) logged so far."""
    n = 0
    if not os.path.exists(path):
        return 0
    for line in open(path, encoding='utf-8'):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        m = r.get('msg')
        if r.get('dir') == 'client->server' and isinstance(m, dict) and m.get('method') == 'tools/call'                 and (m.get('params') or {}).get('name') in ('execute', 'batch'):
            n += 1
    return n


def main(out, t0, m1, m2):
    r = Run(out, t0)
    r.say(1, m1)
    time.sleep(3.0)
    if build_calls(r.tpath) == 0:
        r.mark('turn 1: nothing built (no execute or batch call); fixed answer sent')
        r.say('1b', ANSWER)
        time.sleep(3.0)
    r.say(2, m2)
    time.sleep(3.0)
    open(os.path.join(out, 'pane-full.txt'), 'w').write(d.pane(full=True))


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4])
