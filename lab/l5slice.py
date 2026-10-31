"""L5-Q3: the slicer's numbers for each file, with no window and no AI. PrusaSlicer 2.9.2's CLI with the presets the
filmed window used (0.20mm SPEED @MK4S 0.4, Prusament PLA Blend @MK4S, Original Prusa MK4S 0.4 nozzle), resolved from
its own bundle (slicer/resolve_preset.py: the CLI can't load presets by name), plain-text G-code; once as set (supports
off, the window's default) and once with supports on (build plate only). Per file: time, grams, support, the number of
layers, the slicer's printed warnings, and our checker's lie (height, bed contact).
    python3 lab/l5slice.py OUT.json NAME=FILE [NAME=FILE ...]      (inside sc5-l5:0.28.0)"""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, '/work')
sys.path.insert(0, '/work/lab')
import numpy as np  # noqa: E402
from checker import m3mf, stl  # noqa: E402
from slicer import gcode, resolve_preset  # noqa: E402
import l5score  # noqa: E402

BUNDLE = '/usr/share/PrusaSlicer/profiles/PrusaResearch.ini'
PRESETS = ('0.20mm SPEED @MK4S 0.4', 'Prusament PLA Blend @MK4S', 'Original Prusa MK4S 0.4 nozzle')
WORK = '/tmp/l5slice'


def configs():
    os.makedirs(WORK, exist_ok=True)
    flat = resolve_preset.flat_config(resolve_preset.parse(open(BUNDLE, encoding='utf-8').read()), *PRESETS)
    flat = re.sub(r'^binary_gcode = .*$', 'binary_gcode = 0', flat, flags=re.M)
    on = flat
    for k in ('support_material', 'support_material_auto', 'support_material_buildplate_only'):
        on = re.sub(rf'^{k} = .*$', f'{k} = 1', on, flags=re.M)
    paths = {}
    for name, text in (('as set', flat), ('supports on', on)):
        p = os.path.join(WORK, name.replace(' ', '-') + '.ini')
        open(p, 'w', encoding='utf-8').write(text)
        paths[name] = p
    keys = {k: re.search(rf'^{k} = (.*)$', flat, re.M).group(1) for k in
            ('support_material', 'layer_height', 'fill_density', 'filament_settings_id', 'print_settings_id',
             'printer_settings_id')}
    return paths, keys


def lie_of(path):
    tris = np.concatenate(m3mf.read(path)[1]) if path.endswith('.3mf') else stl.read(path)
    h = float(tris[:, :, 2].max() - tris[:, :, 2].min())
    a = l5score.bed_contact(tris)
    chk = m3mf.check(path) if path.endswith('.3mf') else stl.check(path)
    return {'height_mm': round(h, 3), 'bed_contact_mm2': round(a, 1), 'lie': l5score.lie(h, a),
            'closed': chk['closed'], 'bodies': chk['bodies'], 'size_mm': chk['size_mm'], 'unit': chk.get('unit')}


def slice_one(path, ini, tag):
    g = os.path.join(WORK, tag + '.gcode')
    r = subprocess.run(['prusa-slicer', '--load', ini, '--center', '125,105', '--export-gcode', '-o', g, path],
                       capture_output=True, text=True)
    log = r.stdout + r.stderr
    warn = re.findall(r'print warning: (.*?)(?=^\s*\d+ =>|\Z)', log, re.S | re.M)
    if not os.path.exists(g):
        return {'error': log[-800:]}
    text = open(g, encoding='utf-8', errors='replace').read()
    s = gcode.stats(text)
    zs = [float(z) for z in re.findall(r'^;Z:([0-9.]+)', text, re.M)]
    return {'time': s['time'], 'minutes': gcode.minutes(s['time']), 'total_g': s['total_g'],
            'support_g': round(s['support_g'], 3), 'support_lines': s['support_lines'] + s['support_interface_lines'],
            'layers': len(set(zs)), 'top_z': max(zs) if zs else None,
            'warnings': [' '.join(w.replace(os.path.basename(path), '').split()) for w in warn]}


def main(out, items):
    paths, keys = configs()
    res = {'slicer': subprocess.run(['prusa-slicer', '--help'], capture_output=True, text=True).stdout.split('\n')[0],
           'presets': PRESETS, 'bundle_config_version': re.search(r'config_version = (\S+)', open(BUNDLE).read()).group(1),
           'as_set': keys, 'files': {}}
    for it in items:
        name, path = it.split('=', 1)
        row = {'file': os.path.relpath(path, '/work') if path.startswith('/work') else path}
        row.update(lie_of(path))
        for k, ini in paths.items():
            row[k] = slice_one(path, ini, name + '-' + k.replace(' ', '-'))
        res['files'][name] = row
        print(name, row['lie'], row['as set'].get('time'), row['as set'].get('warnings'), 'supports on:',
              row['supports on'].get('support_g'), row['supports on'].get('warnings'), flush=True)
    json.dump(res, open(out, 'w', encoding='utf-8'), indent=1)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
