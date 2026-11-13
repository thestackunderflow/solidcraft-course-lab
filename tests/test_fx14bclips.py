"""fx14bclips.py: every filmed beat resolves to a real span in its take's events.jsonl (no ffmpeg needed)."""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['FX14B_OUT'] = os.path.join(ROOT, 'out', 'fx14b')
spec = importlib.util.spec_from_file_location('fx14bclips', os.path.join(ROOT, 'lab', 'fx14bclips.py'))
fx14bclips = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx14bclips)


def last_t(take):
    with open(os.path.join(ROOT, 'out', 'fx14b', take, 'events.jsonl')) as f:
        return [json.loads(line) for line in f][-1]['t']


def test_spans_inside_takes():
    for name, take, t0, t1, zoom, centre in fx14bclips.segs():
        assert 0 <= t0 < t1 <= last_t(take) + 1.5, name
        assert 1.0 < zoom <= 3.0 and 0 <= centre[0] <= 2880 and 0 <= centre[1] <= 1620, name


def test_names_unique_and_cover_every_take():
    S = fx14bclips.segs()
    names = [s[0] for s in S]
    assert len(names) == len(set(names))
    assert {s[1] for s in S} == {'A', 'B', 'C', 'C2', 'D', 'E'}     # R1 runs on the PC later


def test_storyboard_beats_filmed():
    names = {s[0] for s in fx14bclips.segs()}
    for n in ('A-open', 'A-orbit', 'A-history', 'A-features', 'A-refusal-line', 'A-line-hold', 'A-report-draft',  # F0 F1 F4 S0
              'B-props-before', 'B-use-fixed', 'B-sketch-opens', 'B-circle', 'B-cut', 'B-props', 'B-area',      # F2 F5 S1
              'B-turning',                                                                                     # F7 left, F11
              'C-hole-menu', 'C-hole-pick', 'C-hole-flat', 'C-hole-ok', 'C-hole-props', 'C-timeline',           # F6 F7 right
              'C-yourturn-line', 'C-yourturn-fixed', 'C-yourturn-cut', 'C-yourturn-props',                      # F10
              'D-mcp-reply',                                                                                    # F9 left
              'E-convert-edit', 'E-insert-edit', 'E-search', 'E-control', 'E-extrude-face', 'E-offset'):        # F8, Q23, Q28
        assert n in names, n


def test_centres_are_twice_the_probe_units():
    assert fx14bclips.SRC == (2880, 1620) and fx14bclips.SIZE == (1920, 1080)
    assert fx14bclips.DIALOG[0] > 2400                  # the Create Sketch / Hole / Extrude dialogs sit at the right edge
