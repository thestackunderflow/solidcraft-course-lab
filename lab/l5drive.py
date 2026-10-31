"""L5-Q6: lesson 4's Claude Code driver (l4drive.Run: types the message into the real TUI, answers Claude Code's
approvals with the prompt's own "Yes", marks every tool call, ends the turn when the newest end-of-turn line changes),
with lesson 5's pre-registered extras (out/l5/prereg.json):
  - one message; if its turn sent nothing to a slicer and changed nothing (no execute or batch call), the fixed answer
    "Your choice." once (turn "1b");
  - while the run goes, every new version of the file in SolidCraft's slicer folder is copied (a second send reuses
    the name), and a PrusaSlicer window that opens is moved into the right-hand part of the screen, beside the terminal;
  - a SolidCraft window asking to allow an agent's send, if one appears, is recorded (screenshot + window name) and
    allowed with Enter (the owner's role);
  - after the turn, the driver (no AI) presses Ctrl+R (Slice now) in the slicer window and keeps a screenshot.
    python3 l5drive.py RUN_DIR T0_EPOCH "message" TERM_W"""
import glob
import os
import shutil
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l4drive  # noqa: E402

SLICED = '/root/.cache/solidcraft/slicer'


def sh(*a):
    return subprocess.run(list(a), capture_output=True, text=True).stdout.strip()


def slicer_win():
    w = sh('xdotool', 'search', '--name', 'PrusaSlicer-2.9')
    return w.split('\n')[0] if w else ''


class Watch:
    def __init__(self, run, term_w, W=2880, H=1800):
        self.run, self.term_w, self.W, self.H = run, term_w, W, H
        self.seen, self.moved, self.stop, self.n = {}, set(), False, 0

    def tick(self):
        for f in glob.glob(os.path.join(SLICED, '*')):
            try:
                st = os.stat(f)
            except OSError:
                continue
            key = (st.st_mtime, st.st_size)
            if self.seen.get(f) != key:
                time.sleep(0.4)
                self.seen[f] = key
                self.n += 1
                dst = os.path.join(self.run.out, 'sent-%d-%s' % (self.n, os.path.basename(f)))
                shutil.copy(f, dst)
                self.run.mark('slicer file written', file=os.path.basename(dst), bytes=st.st_size)
        w = slicer_win()
        if w and w not in self.moved:
            time.sleep(4.0)
            subprocess.run(['xdotool', 'windowsize', w, str(self.W - self.term_w), str(self.H)])
            subprocess.run(['xdotool', 'windowmove', w, str(self.term_w), '0'])
            self.moved.add(w)
            self.run.mark('slicer window up (moved beside the terminal)')
        names = sh('bash', '-c', 'for w in $(xdotool search --onlyvisible --name ".*"); do xdotool getwindowname $w; done')
        for name in names.split('\n'):
            low = name.lower()
            if name and ('allow' in low or 'agent' in low or 'confirm' in low) and name not in self.seen:
                self.seen[name] = 1
                subprocess.run(['import', '-window', 'root', os.path.join(self.run.out, 'confirm.png')])
                self.run.mark('SolidCraft confirmation window', name=name)
                subprocess.run(['xdotool', 'key', 'Return'])

    def run_(self):
        while not self.stop:
            try:
                self.tick()
            except Exception as e:  # keep watching; the error goes to the events
                self.run.mark('watch error', error=str(e)[:200])
            time.sleep(0.5)


def main(out, t0, m1, term_w):
    r = l4drive.Run(out, t0)
    w = Watch(r, int(term_w))
    th = threading.Thread(target=w.run_, daemon=True)
    th.start()
    r.say(1, m1)
    time.sleep(3.0)
    if l4drive.build_calls(r.tpath) == 0:
        r.mark('turn 1: nothing sent or changed (no execute or batch call); fixed answer sent')
        r.say('1b', l4drive.ANSWER)
        time.sleep(3.0)
    time.sleep(2.0)
    s = slicer_win()
    if s:
        r.mark('after the turn: Ctrl+R (Slice now) in the slicer, by the driver')
        subprocess.run(['xdotool', 'windowactivate', '--sync', s])
        subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+r'])
        time.sleep(16.0)
        subprocess.run(['import', '-window', 'root', os.path.join(out, 'slicer-after.png')])
        r.mark('slicer estimate held')
        time.sleep(4.0)
    else:
        r.mark('after the turn: no slicer window')
    w.stop = True
    open(os.path.join(out, 'pane-full.txt'), 'w').write(l4drive.d.pane(full=True))


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4])
