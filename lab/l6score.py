"""Lesson 6's pass rule (pre-registered in out/l6/prereg.json before any Claude run): the change C and the seven
must-stay-true lines M1-M7, each with its tolerance, on a read of the live design written by lab/l6read.py (no AI).
A run passes when every line holds. A value that couldn't be measured fails its line.

    read = {'summary': l4read summary, 'body_count', 'closed', 'mesh': {closed, bodies}, 'geom': checker.l6geom,
            'sent': the file our script sent to the slicer, as l5slice.lie_of reads it (or None)}"""

TARGET_OPENING = 30.0
LINES = [
    ('C', 'the opening is 30 mm', '30.00 ± 0.05 mm, a level ray across the gap (lab/l6geom)'),
    ('M1', 'one closed body', 'measure: body_count 1 and closed; the exported mesh closed, 1 body'),
    ('M2', 'the plate 60 mm tall, 20 mm wide', 'bounding box Z 60.00, Y 20.00 (± 0.05)'),
    ('M3', 'every wall 5 mm thick', 'plate, lip and base each 5.00 ± 0.05 (rays)'),
    ('M4', 'the lip 10 mm tall', 'a ray down through the lip: top 10.00 ± 0.05 above the bottom'),
    ('M5', 'both screw holes 4.5 mm, centred, 15 and 45 mm below the top',
     'exactly 2 bores, Ø 4.50 ± 0.01, centred (± 0.01), 15 and 45 ± 0.05 below the top'),
    ('M6', 'the two rounded top edges', '2 round faces at the top, R 2.00 ± 0.01'),
    ('M7', 'it still goes to the slicer lying on its side', 'a send by our script: the file 20.00 ± 0.05 mm tall'),
]


def _near(v, want, tol):
    return v is not None and abs(float(v) - want) <= tol


def _check(i, r):
    s, g, sent = r.get('summary') or {}, r.get('geom') or {}, r.get('sent')
    bb = s.get('bbox_mm') or [None, None, None]
    if i == 'C':
        v = g.get('opening_mm')
        return _near(v, TARGET_OPENING, 0.05), {'opening_mm': v}
    if i == 'M1':
        mesh = r.get('mesh') or {}
        ok = r.get('body_count') == 1 and r.get('closed') is True and mesh.get('closed') is True and mesh.get('bodies') == 1
        return ok, {'body_count': r.get('body_count'), 'closed': r.get('closed'), 'mesh': mesh}
    if i == 'M2':
        return _near(bb[2], 60.0, 0.05) and _near(bb[1], 20.0, 0.05), {'bbox_mm': bb}
    if i == 'M3':
        w = {k: g.get(k) for k in ('plate_mm', 'lip_mm', 'base_mm')}
        return all(_near(v, 5.0, 0.05) for v in w.values()), w
    if i == 'M4':
        v = g.get('lip_height_mm')
        return _near(v, 10.0, 0.05), {'lip_height_mm': v}
    if i == 'M5':
        holes = s.get('holes') or []
        top = (s.get('bbox_max') or [0, 0, None])[2]
        below = sorted(round(top - h['z'], 4) for h in holes) if top is not None else []
        ok = (len(holes) == 2 and all(_near(h.get('diameter'), 4.5, 0.01) and h.get('centred') for h in holes)
              and len(below) == 2 and _near(below[0], 15.0, 0.05) and _near(below[1], 45.0, 0.05))
        return ok, {'holes': [{k: h.get(k) for k in ('diameter', 'centred', 'from_sides')} for h in holes],
                    'below_top_mm': below}
    if i == 'M6':
        top = (s.get('bbox_max') or [0, 0, 0])[2]
        tops = [f for f in s.get('fillets') or [] if f.get('z', 0) > top - 5.0]
        ok = s.get('top_edges_rounded') == 2 and len(tops) == 2 and all(_near(f.get('radius'), 2.0, 0.01) for f in tops)
        return ok, {'top_edges_rounded': s.get('top_edges_rounded'), 'radii': [f.get('radius') for f in tops]}
    if i == 'M7':
        h = (sent or {}).get('height_mm')
        return _near(h, 20.0, 0.05), {'sent_height_mm': h, 'sent_size_mm': (sent or {}).get('size_mm')}
    raise KeyError(i)


def score(read):
    if read.get('headless'):         # the read landed in an empty headless session, not the user's window: no score
        return {'passed': None, 'refused': 'headless session', 'lines': [], 'also': {}}
    lines = []
    for i, name, how in LINES:
        ok, got = _check(i, read)
        lines.append({'id': i, 'line': name, 'rule': how, 'ok': bool(ok), 'measured': got})
    return {'passed': all(x['ok'] for x in lines), 'lines': lines,
            'also': {'volume_mm3': (read.get('summary') or {}).get('volume_mm3'),
                     'hole_params': (read.get('summary') or {}).get('hole_params')}}
