"""fx13clips.py: every filmed beat resolves to a real span in its take's events.jsonl (no ffmpeg needed)."""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['FX13_OUT'] = os.path.join(ROOT, 'out', 'fx13')
spec = importlib.util.spec_from_file_location('fx13clips', os.path.join(ROOT, 'lab', 'fx13clips.py'))
fx13clips = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx13clips)


def last_t(take):
    with open(os.path.join(ROOT, 'out', 'fx13', take, 'events.jsonl')) as f:
        return [json.loads(line) for line in f][-1]['t']


def test_spans_inside_takes():
    for name, take, t0, t1, zoom, centre in fx13clips.segs():
        assert 0 <= t0 < t1 <= last_t(take) + 1.5, name
        assert 1.0 < zoom <= 3.0 and 0 <= centre[0] <= 2880 and 0 <= centre[1] <= 1620, name


def test_names_unique_and_cover_every_take():
    S = fx13clips.segs()
    names = [s[0] for s in S]
    assert len(names) == len(set(names))
    assert {s[1] for s in S} == {'A', 'B', 'C', 'D'}     # R1 runs on the PC later


def test_storyboard_beats_filmed():
    names = {s[0] for s in fx13clips.segs()}
    for n in ('A-open-cup', 'A-orbit', 'A-section-solid', 'A-shell-dialog', 'A-preview-all', 'A-refusal-line',  # F0 F1 F4 S0
              'A-line-hold', 'A-report-draft', 'A-side-pick',                                             # F4, Q3b (F10)
              'B-untick', 'B-preview-top', 'B-ok', 'B-props', 'B-section', 'B-wall', 'B-floor', 'B-turning',  # F2 F5 F7 F11 S1
              'C-second-cup', 'C-second-preview', 'C-second-props',                                        # F6 S2
              'C-yourturn-untick', 'C-yourturn-props',                                                     # F10
              'C-r3',                                                                                       # pinned bonus
              'D-mcp-reply'):                                                                               # F9
        assert n in names, n
