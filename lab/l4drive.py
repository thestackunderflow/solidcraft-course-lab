"""L4-Q6: lesson 2's Claude Code driver (l2drive.Run: types each message into the real TUI, answers approvals with
the prompt's own "Yes", marks every tool call) with lesson 4's one pre-registered extra: if message 1's turn ends with
no solid.hole call logged (Claude asked a question instead of acting), it sends the fixed answer "Your choice." once
(turn "1b") before message 2.
    python3 l4drive.py RUN_DIR T0_EPOCH "message 1" "message 2\""""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l2drive as d  # noqa: E402

ANSWER = 'Your choice.'


def hole_calls(path):
    n = 0
    if not os.path.exists(path):
        return 0
    for line in open(path, encoding='utf-8'):
        if '"tools/call"' in line and 'solid.hole' in line:
            n += 1
    return n


def main(out, t0, m1, m2):
    r = d.Run(out, t0)
    r.say(1, m1)
    time.sleep(3.0)
    if hole_calls(r.tpath) == 0:
        r.mark('turn 1: no solid.hole call; fixed answer sent')
        r.say('1b', ANSWER)
        time.sleep(3.0)
    r.say(2, m2)
    time.sleep(3.0)
    open(os.path.join(out, 'pane-full.txt'), 'w').write(d.pane(full=True))


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4])
