"""Support in a PrusaSlicer G-code (plain text): extrusion moves under ;TYPE:Support material and ;TYPE:Support
material interface, their filament length -> grams, and the slicer's own totals from the footer. Arcs (G2/G3) count as
moves too (the SPEED preset fits arcs). Copied for lesson 5 from the overhang lab (same author, Apache-2.0), plus
minutes() for the footer's time."""
import math
import re

SUPPORT = 'Support material'
INTERFACE = 'Support material interface'
E_RE = re.compile(r'\bE(-?[0-9.]+)')


def stats(text):
    foot = dict(re.findall(r'^; ([^=\n]+?) = (.+)$', text, re.M))
    dia = float(foot.get('filament_diameter', '1.75').split(',')[0])
    dens = float(foot.get('filament_density', '1.24').split(',')[0])
    area = math.pi * (dia / 2) ** 2
    cur = None
    lines = {SUPPORT: 0, INTERFACE: 0}
    e_mm = {SUPPORT: 0.0, INTERFACE: 0.0}
    xy = {SUPPORT: [], INTERFACE: []}
    z = 0.0
    zs = {SUPPORT: set(), INTERFACE: set()}
    for raw in text.splitlines():
        if raw.startswith(';TYPE:'):
            cur = raw[6:].strip()
            continue
        if raw.startswith(';Z:'):
            z = float(raw[3:])
            continue
        if cur not in lines or not raw.startswith(('G1 ', 'G2 ', 'G3 ')):
            continue
        m = E_RE.search(raw)
        if m and float(m.group(1)) > 0:
            lines[cur] += 1
            e_mm[cur] += float(m.group(1))
            zs[cur].add(round(z, 3))
            mx, my = re.search(r'\bX(-?[0-9.]+)', raw), re.search(r'\bY(-?[0-9.]+)', raw)
            if mx and my:
                xy[cur].append((float(mx.group(1)), float(my.group(1))))
    g = lambda k: e_mm[k] * area * dens / 1000.0  # noqa: E731
    return {
        'support_lines': lines[SUPPORT], 'support_interface_lines': lines[INTERFACE],
        'support_g': g(SUPPORT) + g(INTERFACE), 'support_only_g': g(SUPPORT), 'support_interface_g': g(INTERFACE),
        'support_z_range': [min(zs[SUPPORT] | zs[INTERFACE]), max(zs[SUPPORT] | zs[INTERFACE])]
        if (zs[SUPPORT] | zs[INTERFACE]) else None,
        'support_xy_box': _box(xy[SUPPORT] + xy[INTERFACE]),
        'total_g': float(foot['total filament used [g]']) if 'total filament used [g]' in foot else None,
        'time': foot.get('estimated printing time (normal mode)'),
        'support_settings': {k: foot.get(k) for k in ('support_material', 'support_material_auto',
                                                       'support_material_buildplate_only', 'support_material_threshold',
                                                       'print_settings_id', 'layer_height',
                                                       'external_perimeter_extrusion_width', 'perimeter_extrusion_width',
                                                       'extrusion_width')},
    }


def _box(pts):
    if not pts:
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return [round(min(xs), 2), round(min(ys), 2), round(max(xs), 2), round(max(ys), 2)]


def minutes(t):
    """PrusaSlicer's time text ("1h 2m 30s", "32m 45s") -> minutes, rounded to 4 places."""
    n = {'d': 1440, 'h': 60, 'm': 1, 's': 1 / 60}
    return round(sum(float(v) * n[u] for v, u in re.findall(r'(\d+)([dhms])', t or '')), 4)
