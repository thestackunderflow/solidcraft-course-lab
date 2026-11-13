"""fx11clips.py: every filmed beat resolves to a real span in its take's events.jsonl (no ffmpeg needed)."""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['FX11_OUT'] = os.path.join(ROOT, 'out', 'fx11')
spec = importlib.util.spec_from_file_location('fx11clips', os.path.join(ROOT, 'lab', 'fx11clips.py'))
fx11clips = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx11clips)


def last_t(take):
    with open(os.path.join(ROOT, 'out', 'fx11', take, 'events.jsonl')) as f:
        return [json.loads(line) for line in f][-1]['t']


def test_spans_inside_takes():
    for name, take, t0, t1, zoom, centre in fx11clips.segs():
        assert 0 <= t0 < t1 <= last_t(take) + 1.5, name
        assert 1.0 < zoom <= 3.0 and 0 <= centre[0] <= 2880 and 0 <= centre[1] <= 1620, name


def test_names_unique_and_cover_every_take():
    S = fx11clips.segs()
    names = [s[0] for s in S]
    assert len(names) == len(set(names))
    assert {s[1] for s in S} == {'A', 'B', 'B-q3', 'C', 'D'}     # R1 runs on the PC later; Q3 from B-q3 (DEVIATIONS)


def test_storyboard_beats_filmed():
    names = {s[0] for s in fx11clips.segs()}
    for n in ('A-open-tower', 'A-split-xy-refused', 'A-refusal-line', 'A-report-draft', 'A-section',   # F0 F1 F4 S0
              'B-offset-100', 'B-split-100', 'B-two-bodies', 'B-props-row1', 'B-props-row2', 'B-pieces',  # F2 F5 F11 S1
              'B-midplane',                                                                             # Q3
              'C-sym-split', 'C-sym-props-row1', 'C-sym-props-row2',                                    # F6
              'C-above-210', 'C-above-refusal-line', 'C-s2-frame', 'C-at-200', 'C-top-face',            # F8 S2 Q6
              'C-block-split', 'C-block-props-row1', 'C-block-props-row2',                              # F10
              'D-mcp-reply'):                                                                           # F9
        assert n in names, n
