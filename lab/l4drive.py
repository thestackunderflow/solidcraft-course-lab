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
    r = d.Run(out, t0)
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
