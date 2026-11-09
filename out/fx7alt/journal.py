"""fx7alt take D (QA4): the point the Fillet dialog sent, from SolidCraft's own session journal (the recovery copy it
autosaves under ~/.local/share/solidcraft/recovery: a zip whose document.json lists every feature with its params).
Prints the newest recovery file's fillet features as stored.
    python3 -I journal.py"""
import glob
import json
import os
import zipfile

files = sorted(glob.glob(os.path.expanduser('~/.local/share/solidcraft/recovery/*.sc')), key=os.path.getmtime)
if not files:
    print('# no recovery journal yet')
else:
    print('# SolidCraft session journal: ~/.local/share/solidcraft/recovery/' + os.path.basename(files[-1]) + ' (document.json)')
    doc = json.loads(zipfile.ZipFile(files[-1]).read('document.json'))
    for f in doc['features']:
        if f.get('type') == 'fillet':
            print(json.dumps({k: f.get(k) for k in ('name', 'type', 'edges', 'edge_names', 'radius')}))
