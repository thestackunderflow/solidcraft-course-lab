"""L6-Q4: lesson 5's Claude Code driver (l5drive: types the message into the real TUI, answers Claude Code's approvals
with the prompt's own "Yes", marks every tool call, copies every file sent to the slicer, moves a slicer window beside
the terminal) with lesson 6's pre-registered extras (out/l6/prereg.json):
  - one message; if after its turn the design is unchanged (a no-AI read: the six sizes' expressions and the volume
    equal to the start; plan gate accuracy M6: read-only calls don't count as changes), the fixed answer "Your
    choice." once (turn "1b"); the check is logged in trigger.json;
  - after the turn, still filmed, our no-AI read (lab/l6read.py --send --keep-slicer): any slicer Claude opened is
    closed, the live design is read, then sent to PrusaSlicer by the script; the slicer window is moved beside the
    terminal and the driver presses Ctrl+R (Slice now) and holds on the estimate.
    python3 l6drive.py RUN_DIR T0_EPOCH "message" TERM_W"""
import json
import os
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import l4drive  # noqa: E402
import l5drive  # noqa: E402

START = {'plate_height': '60', 'width': '20', 'thickness': '5', 'hook_depth': '25', 'lip_height': '10', 'hole_d': '4.5'}
START_VOLUME = 8306.62


def design_unchanged(out):
    """A no-AI read over the entry SolidCraft wrote: the user sizes' expressions and the volume, against the start."""
    sys.path.insert(0, '/work')
    from client.mcp import McpClient
    e = json.load(open(os.path.join(out, 'entry-solidcraft-wrote.json')))['mcpServers']['solidcraft']
    c = McpClient([e['command']] + list(e.get('args') or []), timeout_s=120,
                  log_path=os.path.join(out, 'trigger-transcript.jsonl'))
    c.start()
    m = McpClient.text_json(c.call_tool('measure', {}))
    pl = McpClient.text_json(c.call_tool('execute', {'command': 'parameters.list', 'params': {}}))
    c.close()
    sizes = {p['name']: str(p.get('expression')) for p in (pl.get('parameters') or [])
             if str(p.get('source', '')).startswith('user')}
    vol = (m.get('total') or {}).get('volume_mm3')
    same = sizes == START and vol is not None and abs(vol - START_VOLUME) < 0.01
    json.dump({'sizes': sizes, 'volume_mm3': vol, 'unchanged': same}, open(os.path.join(out, 'trigger.json'), 'w'), indent=1)
    return same


def main(out, t0, m1, term_w):
    r = l4drive.Run(out, t0)
    w = l5drive.Watch(r, int(term_w))
    th = threading.Thread(target=w.run_, daemon=True)
    th.start()
    r.say(1, m1)
    time.sleep(3.0)
    if design_unchanged(out):
        r.mark('turn 1: the design is unchanged (sizes and volume as at the start); fixed answer sent')
        r.say('1b', l4drive.ANSWER)
        time.sleep(3.0)
    time.sleep(3.0)
    open(os.path.join(out, 'pane-full.txt'), 'w').write(l4drive.d.pane(full=True))
    r.mark('after the turn: our read (no AI) starts: measure, a mesh copy, then a send to PrusaSlicer by the script')
    w.moved.clear()
    p = subprocess.run(['python3', '/work/lab/l6read.py', os.path.join(out, 'read.json'), '--entry',
                        os.path.join(out, 'entry-solidcraft-wrote.json'), '--send', '--keep-slicer'],
                       capture_output=True, text=True)
    open(os.path.join(out, 'read.txt'), 'w').write(p.stdout + p.stderr)
    r.mark('our read done', result=p.stdout.strip()[:300])
    for _ in range(60):
        if l5drive.slicer_win() and l5drive.slicer_win() in w.moved:
            break
        time.sleep(0.5)
    s = l5drive.slicer_win()
    if s:
        time.sleep(3.0)
        r.mark('our send: the slicer window up; Ctrl+R (Slice now), by the driver')
        subprocess.run(['xdotool', 'windowactivate', '--sync', s])
        subprocess.run(['xdotool', 'key', '--clearmodifiers', 'ctrl+r'])
        time.sleep(16.0)
        subprocess.run(['import', '-window', 'root', os.path.join(out, 'slicer-after.png')])
        r.mark('slicer estimate held')
        time.sleep(4.0)
    else:
        r.mark('after our send: no slicer window')
    w.stop = True


if __name__ == '__main__':
    main(sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4])
