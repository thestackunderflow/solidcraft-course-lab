"""Our own reader for a 3MF file (the format SolidCraft's Send to Slicer writes by default): the model's unit, each
object's triangles, then the same checks as the STL checker (closed, bodies, size, volume), sizes converted to mm.

    python3 -m checker.m3mf FILE.3mf     prints the JSON"""
import json
import re
import sys
import zipfile

import numpy as np

from checker.stl import mesh_check

MM = {'micron': 0.001, 'millimeter': 1.0, 'centimeter': 10.0, 'inch': 25.4, 'foot': 304.8, 'meter': 1000.0}
NUM = r'"([-+0-9.eE]+)"'


def read(path):
    """-> (unit, [triangles array (N, 3, 3) in the file's unit, one per object with a mesh])"""
    z = zipfile.ZipFile(path)
    name = next(n for n in z.namelist() if n.lower().endswith('.model'))
    s = z.read(name).decode('utf-8', 'replace')
    m = re.search(r'<model\b[^>]*\bunit="([a-z]+)"', s)
    unit = m.group(1) if m else 'millimeter'
    objs = []
    for body in re.findall(r'<object\b[^>]*>(.*?)</object>', s, re.S):
        vs = re.findall(r'<vertex\b[^>]*x=' + NUM + r'[^>]*y=' + NUM + r'[^>]*z=' + NUM, body)
        ts = re.findall(r'<triangle\b[^>]*v1="(\d+)"[^>]*v2="(\d+)"[^>]*v3="(\d+)"', body)
        if not vs or not ts:
            continue
        v = np.array(vs, dtype=np.float64)
        objs.append(v[np.array(ts, dtype=np.int64)])
    return unit, objs


def check(path):
    unit, objs = read(path)
    k = MM.get(unit, 1.0)
    allt = np.concatenate(objs) * k
    r = mesh_check(allt)
    r = dict({'file': path.replace('\\', '/').split('/')[-1], 'unit': unit, 'objects': len(objs)}, **r)
    r['closed'] = all(mesh_check(o * k)['closed'] for o in objs)
    return r


if __name__ == '__main__':
    print(json.dumps(check(sys.argv[1]), indent=1))
