"""Lesson 5 scoring helpers (rules pre-registered in out/l5/prereg.json): how a part sent to the slicer lies on the bed
(from the sent file's size), and what a Claude run read before it sent (from its logged tools/call lines and their
replies). A "check read" means a reply before the send contained the fact; what Claude then said about it is quoted
separately from its reply text, not scored here.

    calls = [{'seq', 'name', 'args', 'reply'}]  (lab/l5compare.py builds them from transcript.jsonl)"""
import json

HOOK = (25.0, 20.0, 60.0)       # lesson 4's hook as drawn: arm depth x width x plate height, mm
TOL = 0.05


def orientation(size):
    """'standing' (as drawn: 60 tall), 'on its side' (the J outline down: 20 tall), 'on its back' (the plate's back
    down: 25 tall), else 'other'. Size = [x, y, z] of the sent part in mm; x and y may be swapped on the bed."""
    x, y, z = (float(v) for v in size)
    flat = sorted([x, y])
    for name, top, rest in (('standing', 60.0, (20.0, 25.0)), ('on its side', 20.0, (25.0, 60.0)),
                            ('on its back', 25.0, (20.0, 60.0))):
        if abs(z - top) <= TOL and all(abs(a - b) <= TOL for a, b in zip(flat, rest)):
            return name
    return 'other'


def bed_contact(tris):
    """Area (mm²) of the triangles lying flat at the part's lowest height: what touches the bed."""
    import numpy as np
    t = np.asarray(tris, dtype=float)
    z0 = t[:, :, 2].min()
    flat = np.all(np.abs(t[:, :, 2] - z0) < 1e-4, axis=1)
    a, b, c = t[flat, 0], t[flat, 1], t[flat, 2]
    return float(np.linalg.norm(np.cross(b - a, c - a), axis=1).sum() / 2.0)


# lesson 4's hook (probe, the exported mesh): the height and the area on the bed for each flat face we name
LIES = (('standing', 60.0, 500.0), ('on its side', 20.0, 423.0), ('on its back', 25.0, 1128.0))


def lie(height, contact, tol_h=0.05, tol_a=0.06):
    """Name how the part lies from its height and its bed contact (plan gate, accuracy M4: the height alone can't tell
    the lip's face from the back, or upside down from standing). Contact within 6%: the faces' areas differ a lot."""
    for name, h, a in LIES:
        if abs(height - h) <= tol_h and abs(contact - a) <= tol_a * a:
            return name
    return 'other: %.1f mm tall, %.0f mm² on the bed' % (height, contact)


def _commands(c):
    """The SolidCraft commands one tools/call carries: execute -> one, batch -> its list, others -> the tool itself."""
    a = c.get('args') or {}
    if c['name'] == 'execute':
        return [(a.get('command'), a.get('params') or {})]
    if c['name'] == 'batch':
        return [(x.get('command'), x.get('params') or {}) for x in a.get('commands') or []]
    return [(c['name'], a)]


def _facts(reply):
    """Which of the three checks a reply's text carries: body count, closed, size (a bounding box or a size)."""
    t = reply if isinstance(reply, str) else json.dumps(reply or '')
    return {'one body': '"body_count"' in t or '"bodies"' in t,
            'closed': '"closed"' in t or '"is_closed"' in t or '"watertight"' in t,
            'size': '"bbox"' in t or '"size' in t or '"bounding_box"' in t}


def score_calls(calls):
    calls = sorted(calls, key=lambda c: c['seq'])
    send_seq, face, saved, read = None, None, [], {'one body': False, 'closed': False, 'size': False}
    sends = []
    for c in calls:
        cmds = _commands(c)
        names = [n for n, _ in cmds]
        for n, p in cmds:
            if n == 'body.print_face' and p.get('point') is not None and send_seq is None:
                face = {'body': p.get('body'), 'point': p.get('point')}
            if n == 'file.save_mesh':
                saved.append(p.get('path'))
                if p.get('slicer'):
                    sends.append(c['seq'])
            if n == 'file.send_to_slicer':
                sends.append(c['seq'])
        if send_seq is None and sends:
            send_seq = sends[0]
        if send_seq is None and not any(n in ('file.send_to_slicer', 'body.print_face') for n in names):
            for k, v in _facts(c.get('reply')).items():
                read[k] = read[k] or v
    return {'sent': send_seq is not None, 'send_seq': send_seq, 'sends': sends, 'read_before_send': read,
            'print_face': face, 'saved_mesh': saved}
