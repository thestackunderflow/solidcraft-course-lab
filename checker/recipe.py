"""Lesson 2: compare two designs by what SolidCraft itself reports (inspect_design and measure replies, as JSON).
A design file is a recipe: the timeline lists its steps in order. Feature names may differ ("Sketch1" vs "Sketch 1");
the step types are what is compared.

"Same part" needs more than a volume (a mirrored J or a J on another plane has the same volume): the same step types,
the same volume, the same profile area, the same sketch plane (its normal) and the same corner points in that plane.
Where the block sits (its bounding box corners) is reported separately: the same J pushed out the other way is the
same part, made by the same recipe, in another place. A sketch on the same plane whose "up" (y_dir) points the other
way draws the same J upside down (lab runs claude-1/2: sketch.create {plane: "XZ"} has up = -Z; the Browser's XZ +Z)."""

TOL = 1e-6


def live(inspect):
    return [f for f in inspect.get('timeline') or [] if not f.get('suppressed') and not f.get('rolled_back')]


def steps(inspect):
    return [f.get('type') for f in live(inspect)]


def _r(v):
    v = round(float(v), 6)
    return 0.0 if v == 0 else v


def _normal(plane):
    if not plane:
        return None
    a, b = plane.get('x_dir'), plane.get('y_dir')
    if not a or not b:
        return None
    return [_r(a[1] * b[2] - a[2] * b[1]), _r(a[2] * b[0] - a[0] * b[2]), _r(a[0] * b[1] - a[1] * b[0])]


def summary(inspect, measure):
    bodies = measure.get('bodies') or []
    box = lo = hi = None
    if len(bodies) == 1 and bodies[0].get('bbox'):
        lo = [_r(v) for v in bodies[0]['bbox']['min']]
        hi = [_r(v) for v in bodies[0]['bbox']['max']]
        box = [_r(h - l) for l, h in zip(lo, hi)]
    sk = inspect.get('sketches') or []
    first = sk[0] if sk else {}
    corners = sorted({tuple(_r(c) for c in p['at']) for p in first.get('points') or [] if p.get('at') is not None})
    corners = [list(c) for c in corners]
    up = (first.get('plane') or {}).get('y_dir')
    return {'steps': steps(inspect), 'step_names': [f.get('name') for f in live(inspect)],
            'sketch_lines': [sum(1 for c in s.get('curves') or [] if c.get('type') == 'line' and not c.get('construction'))
                             for s in sk],
            'profile_areas_mm2': [p.get('area_mm2') for s in sk for p in s.get('profiles') or []],
            'bodies': len(bodies), 'volume_mm3': (measure.get('total') or {}).get('volume_mm3'),
            'closed': all(b.get('closed') for b in bodies) if bodies else False, 'bbox_mm': box,
            'bbox_min': lo, 'bbox_max': hi, 'plane_normal': _normal(first.get('plane')), 'sketch_up': [_r(v) for v in up] if up else None,
            'corners': corners,
            'errors': sum(1 for f in live(inspect) if f.get('error'))}


def _close(a, b, tol):
    return a is not None and b is not None and abs(a - b) <= tol * max(1.0, abs(b))


def _same_list(a, b, tol=1e-4):
    if a is None or b is None or len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if isinstance(x, list):
            if not _same_list(x, y, tol):
                return False
        elif abs(x - y) > tol:
            return False
    return True


def _parallel(a, b, tol=1e-6):
    if not a or not b:
        return False
    return abs(abs(sum(x * y for x, y in zip(a, b))) - 1.0) <= tol


def compare(hand, claude, expected, tol=TOL):
    v = {'same_steps': hand['steps'] == claude['steps'],
         'same_volume': _close(hand['volume_mm3'], claude['volume_mm3'], tol),
         'volume_matches_expected': _close(hand['volume_mm3'], expected['volume_mm3'], tol)
         and _close(claude['volume_mm3'], expected['volume_mm3'], tol),
         'same_profile_area': _same_list(hand['profile_areas_mm2'], claude['profile_areas_mm2']),
         'same_plane': _parallel(hand.get('plane_normal'), claude.get('plane_normal')),
         'same_up': _same_list(hand.get('sketch_up'), claude.get('sketch_up')),
         'opposite_up': _same_list([-x for x in hand.get('sketch_up') or []] or None, claude.get('sketch_up')),
         'same_corners': _same_list(hand.get('corners'), claude.get('corners')),
         'same_size': _same_list(hand['bbox_mm'], claude['bbox_mm']),
         'same_place': _same_list(hand.get('bbox_min'), claude.get('bbox_min'))
         and _same_list(hand.get('bbox_max'), claude.get('bbox_max')),
         'hand_volume_mm3': hand['volume_mm3'], 'claude_volume_mm3': claude['volume_mm3'],
         'expected_volume_mm3': expected['volume_mm3'], 'hand_steps': hand['steps'], 'claude_steps': claude['steps']}
    v['same_shape'] = v['same_profile_area'] and v['same_corners'] and v['same_size'] and v['same_volume']
    ok = (v['same_steps'] and v['same_shape'] and v['same_plane'] and v['volume_matches_expected']
          and not hand['errors'] and not claude['errors'])
    if ok and v['same_up'] and v['same_place']:
        v['verdict'] = 'same part, same recipe'
    elif ok and v['same_up']:
        v['verdict'] = 'same part and recipe, pushed the other way'
    elif ok and v['opposite_up']:
        v['verdict'] = 'same shape, size and steps, but upside down'
    else:
        v['verdict'] = 'different: see the fields'
    return v
