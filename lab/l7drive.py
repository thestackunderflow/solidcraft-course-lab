"""Lesson 7's Claude run (L7-Q11): lesson 2's driver (l2drive.py: types each message into Claude Code's real terminal,
waits, marks tool calls from the logging proxy) with lesson 7's pre-registered answers to approval prompts
(out/l7/prereg.json, written before the run):
  - every prompt that names a SolidCraft tool (mcp__solidcraft__...) gets the prompt's first option, the one-time "Yes";
  - any other prompt (a shell command, a file write) is answered No (Esc): the run is about SolidCraft's plug only.
Between turn 1 and turn 2 it runs the command in L7_BETWEEN (SolidCraft opens; lesson 3's hook built with no AI).
    python3 l7drive.py RUN_DIR T0_EPOCH "message 1" ["message 2" ...]"""
import os
import re
import sys
import time

sys.path.insert(0, '/work/lab')
sys.path.insert(0, '/work')
import l2drive  # noqa: E402
from l2drive import keys, pane, tui, TURN_LIMIT_S, QUIET_S  # noqa: E402


def decide(turn, nth_in_run, text):
    """'no' or 'yes' for one approval prompt (the pre-registered policy): only the prompt's own lines count (the 14
    lines above "Do you want to ..."), not the user's message higher up the screen. Claude Code 2.1.311 writes
    "solidcraft — Inspect the design Tool: (MCP)" (an em dash: run R1 was stopped because the first version only
    took a hyphen and answered No to it)."""
    lines = (text or '').splitlines()
    idx = max([i for i, ln in enumerate(lines) if 'Do you want to' in ln] or [len(lines)])
    window = ' | '.join(lines[max(0, idx - 14):idx])
    return 'yes' if re.search(r'solidcraft\s+[-–—]\s+\S|mcp__solidcraft', window, re.IGNORECASE) else 'no'


class Run(l2drive.Run):
    asked = 0

    def say(self, n, msg):
        self.mark(f'turn {n}: typing')
        for ch in msg:
            keys(ch, literal=True)
            time.sleep(0.045)
        time.sleep(0.8)
        done_before = tui.turns_done(pane(full=True))
        self.mark(f'turn {n}: Enter')
        keys('Enter')
        start, seen_busy, quiet_since, answers = time.time(), False, None, []
        denied_at = None
        while time.time() - start < TURN_LIMIT_S:
            time.sleep(0.4)
            self.tail()
            text = pane()
            if tui.approval(text):
                Run.asked += 1
                d = decide(n, Run.asked, text)
                open(os.path.join(self.out, f'approval-{n}-{len(answers) + 1}.txt'), 'w').write(text)
                self.mark(f'turn {n}: approval asked', answer=d)
                time.sleep(2.5)
                if d == 'yes':
                    keys(tui.approval_key(text))
                else:
                    keys('Escape')
                    denied_at = time.time()
                self.mark(f'turn {n}: approval answered {d}')
                answers.append(d)
                quiet_since = None
                continue
            if tui.turns_done(pane(full=True)) > done_before and not self.calls:
                self.mark(f'turn {n}: end-of-turn line seen')
                time.sleep(2.0)
                break
            if denied_at and not tui.busy(text) and time.time() - denied_at > 6:
                self.mark(f'turn {n}: idle after the denial')
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
        self.mark(f'turn {n}: reply done', answers=answers, timed_out=time.time() - start >= TURN_LIMIT_S)
        open(os.path.join(self.out, f'pane-turn{n}.txt'), 'w').write(pane())


def main(out, t0, messages):
    r = Run(out, t0)
    for i, m in enumerate(messages, 1):
        r.say(i, m)
        time.sleep(3.0)
        if i == 1 and os.environ.get('L7_BETWEEN'):
            r.mark('between: SolidCraft opens')
            os.system(os.environ['L7_BETWEEN'])
            r.mark('between: SolidCraft open, the hook built (no AI)')
            time.sleep(2.0)
    open(os.path.join(out, 'pane-full.txt'), 'w').write(pane(full=True))


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3:])
