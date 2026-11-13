"""fx12: summarise a sketch.inspect reply (lab/fx9.py raw ... execute sketch.inspect) into JSON + one line:
curves (id, type, radius), offset constraints (offset_distance), profile areas.
    python3 fx12sk.py RAW.json OUT.json"""
import json
import sys

raw = json.load(open(sys.argv[1]))
txt = raw['content'][0]['text'].split('\nNote:')[0]
if raw.get('isError'):
    print('sketch.inspect refused:', txt)
    sys.exit(0)
d = json.loads(txt)
json.dump(d, open(sys.argv[2], 'w'), indent=1)
curves = [(c['id'], c['type'], c.get('radius')) for c in d.get('curves', [])]
offs = [k['id'] for k in d.get('constraints', []) if 'offset' in k.get('type', '')]
areas = sorted(round(p.get('area_mm2', 0), 2) for p in d.get('profiles', []))
print('curves', ' '.join(f'{i}:{t}' + (f'(R{r:g})' if r else '') for i, t, r in curves),
      '| offset constraints', offs or 'none', '| links', d.get('links'), '| regions', areas, '| dof', d.get('dof'))
