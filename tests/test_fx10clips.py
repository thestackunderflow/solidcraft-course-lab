"""fx10clips.py: every filmed beat resolves to a real span in its take's events.jsonl (no ffmpeg needed)."""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['FX10_OUT'] = os.path.join(ROOT, 'out', 'fx10')
spec = importlib.util.spec_from_file_location('fx10clips', os.path.join(ROOT, 'lab', 'fx10clips.py'))
fx10clips = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx10clips)


def last_t(take):
    with open(os.path.join(ROOT, 'out', 'fx10', take, 'events.jsonl')) as f:
        return [json.loads(line) for line in f][-1]['t']


def test_spans_inside_takes():
    for name, take, t0, t1, zoom, centre in fx10clips.segs():
        assert 0 <= t0 < t1 <= last_t(take) + 1.5, name
        assert 1.0 < zoom <= 3.0 and 0 <= centre[0] <= 2880 and 0 <= centre[1] <= 1620, name


def test_names_unique_and_cover_every_take():
    S = fx10clips.segs()
    names = [s[0] for s in S]
    assert len(names) == len(set(names))
    assert {s[1] for s in S} == {'A', 'B', 'C', 'D', 'runs/R1'}


def test_refusal_lines_filmed():
    names = {s[0] for s in fx10clips.segs()}
    for n in ('A-refusal-line', 'A-180-refusal-line', 'A-split-refusal-line', 'C-c2-refusal-line', 'D-mcp-reply',
              'R1-prompt', 'R1-working', 'R1-reply'):
        assert n in names
