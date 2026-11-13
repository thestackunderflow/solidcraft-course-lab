"""fx12clips.py: every filmed beat resolves to a real span in its take's events.jsonl (no ffmpeg needed)."""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['FX12_OUT'] = os.path.join(ROOT, 'out', 'fx12')
spec = importlib.util.spec_from_file_location('fx12clips', os.path.join(ROOT, 'lab', 'fx12clips.py'))
fx12clips = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx12clips)


def last_t(take):
    with open(os.path.join(ROOT, 'out', 'fx12', take, 'events.jsonl')) as f:
        return [json.loads(line) for line in f][-1]['t']


def test_spans_inside_takes():
    for name, take, t0, t1, zoom, centre in fx12clips.segs():
        assert 0 <= t0 < t1 <= last_t(take) + 1.5, name
        assert 1.0 < zoom <= 3.0 and 0 <= centre[0] <= 2880 and 0 <= centre[1] <= 1620, name


def test_names_unique_and_cover_every_take():
    S = fx12clips.segs()
    names = [s[0] for s in S]
    assert len(names) == len(set(names))
    assert {s[1] for s in S} == {'A', 'B', 'B-wall', 'C', 'C2', 'D'}     # R1 runs on the PC later; Q11 Fix 1 from B-wall (DEVIATIONS)


def test_storyboard_beats_filmed():
    names = {s[0] for s in fx12clips.segs()}
    for n in ('A-open-tray', 'A-sketch-copy', 'A-fillet-refused', 'A-refusal-line', 'A-report-draft',  # F0 F4 F7 S0
              'A-chamfer-refused',                                                                    # logged
              'B-break-menu', 'B-fillet-4', 'B-extrude', 'B-props', 'Bw-wall',                         # F2 F6 left
              'C-round-5', 'C-offset', 'C-measure-r3', 'C-wall', 'C-extrude', 'C-props',              # F5 F6 F7 S1
              'C2-round-1-5', 'C2-offset',                                                            # Q12, S2 end
              'D-mcp-reply'):                                                                         # F9
        assert n in names, n
