"""L2-Q5: the hand-made part against Claude's, from what SolidCraft reported for each (the no-AI reads in
out/l2/hand/read.json and out/l2/runs/RUN/read.json), and both against the number worked out from the outline.
    python3 lab/l2compare.py [RUN]      -> out/l2/compare.json"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from checker import outline, recipe  # noqa: E402

L2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'out', 'l2')


def main(run='claude-1'):
    hand = json.load(open(os.path.join(L2, 'hand', 'read.json')))
    claude = json.load(open(os.path.join(L2, 'runs', run, 'read.json')))
    exp = outline.expected(outline.J_MOVES, width=20)
    # summaries are recomputed from the raw replies, so a checker fix applies to runs made before it
    hand['summary'] = recipe.summary(hand['inspect_design'], hand['measure'])
    claude['summary'] = recipe.summary(claude['inspect_design'], claude['measure'])
    v = recipe.compare(hand['summary'], claude['summary'], exp)
    v['hand_sketch'] = hand['sketch']
    v['claude_sketch'] = claude['sketch']
    v['expected'] = {k: val for k, val in exp.items() if k != 'vertices'}
    v['hand_summary'] = hand['summary']
    v['claude_summary'] = claude['summary']
    json.dump(v, open(os.path.join(L2, 'compare.json'), 'w'), indent=1)
    print(json.dumps({k: v[k] for k in ('verdict', 'same_steps', 'same_volume', 'same_shape', 'same_plane',
                                         'same_up', 'same_place', 'hand_volume_mm3', 'claude_volume_mm3', 'expected_volume_mm3')},
                     indent=1))
    return v


if __name__ == '__main__':
    main(*sys.argv[1:])
