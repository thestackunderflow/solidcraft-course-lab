"""Lesson 7: the tool-call failures, shown in a terminal with no AI. A scripted MCP client starts SolidCraft's plug
exactly as a Claude app does (the entry `solidcraft-cli mcp setup` writes: the full path and `mcp`), sends the same
tools/call requests a Claude app sends, and prints each request and the plug's reply word for word (the error lines
in full; long JSON shortened to the keys that matter). Every line also goes to the take's transcript (JSON-RPC).

    python3 lab/l7story.py headless OUT_DIR     case 3: SolidCraft not open when the plug starts
    python3 lab/l7story.py errors OUT_DIR       cases 4-6: a batch rolled back, a refused save folder, an older version

The outer take script (lab/l7take.sh) opens or closes SolidCraft's window when this script waits for it
(it waits for the file OUT_DIR/go-N and writes OUT_DIR/wait-N first)."""
import json
import os
import sys
import time
import textwrap

sys.path.insert(0, '/work')
from client.mcp import McpClient  # noqa: E402

NEW = '/opt/solidcraft-0.27.0/bin/solidcraft-cli'
OLD = '/opt/solidcraft-0.26.1/bin/solidcraft-cli'
HOME = os.path.expanduser('~')
DOCS = HOME + '/Documents'
COLS = 76
PACE = float(os.environ.get('PACE', '1.0'))

# Lesson 3's hook (B2's logged batch, which measured 10,000 at 40 and 8,500 at 25): five names, the J, extrude width.
HOOK = [{'command': 'set_parameter', 'params': {'name': 'plate_height', 'value': 60}},
        {'command': 'set_parameter', 'params': {'name': 'width', 'value': 20}},
        {'command': 'set_parameter', 'params': {'name': 'thickness', 'value': 5}},
        {'command': 'set_parameter', 'params': {'name': 'hook_depth', 'value': 25}},
        {'command': 'set_parameter', 'params': {'name': 'lip_height', 'value': 10}},
        {'command': 'sketch.create', 'params': {'plane': 'XZ', 'flip': 'x'}},
        {'command': 'sketch.line', 'params': {'closed': True, 'points': [
            ['0', '0'], ['hook_depth', '0'], ['hook_depth', 'lip_height'], ['hook_depth - thickness', 'lip_height'],
            ['hook_depth - thickness', 'lip_height - thickness'], ['thickness', 'lip_height - thickness'],
            ['thickness', 'plate_height'], ['0', 'plate_height']]}},
        {'command': 'sketch.finish', 'params': {}},
        {'command': 'solid.extrude', 'params': {'distance': 'width', 'operation': 'new', 'name': 'Hook'}}]
TYPO = [{'command': 'set_parameter', 'params': {'name': 'hook_depth', 'value': 40}},
        {'command': 'set_parameter', 'params': {'name': 'lip_height', 'expression': 'hook_dept / 4'}}]
FIXED = [{'command': 'set_parameter', 'params': {'name': 'hook_depth', 'value': 40}},
         {'command': 'set_parameter', 'params': {'name': 'lip_height', 'expression': 'hook_depth / 4'}}]


class Story:
    def __init__(self, out):
        self.out = out
        self.rows = []
        self.ev = open(os.path.join(out, 'story.jsonl'), 'a')

    def nap(self, s):
        time.sleep(s * PACE)

    def say(self, text, indent=0, pause=0.35):
        text = ' '.join(str(text).split())
        for line in textwrap.wrap(text, COLS - indent) or ['']:
            print(' ' * indent + line, flush=True)
            self.nap(0.12)
        self.nap(pause)

    def mark(self, what, **kw):
        row = {'t': time.time(), 'event': what}
        row.update(kw)
        self.ev.write(json.dumps(row) + '\n')
        self.ev.flush()

    def plug(self, cmd, label):
        self.say(f'# {label}')
        self.say('# (our test script starts the plug, as a Claude app does)')
        self.say('plug: ' + ' '.join(cmd), pause=0.6)
        c = McpClient(cmd, timeout_s=120, log_path=os.path.join(self.out, 'transcript.jsonl'))
        init = c.start()
        backend = (init.get('instructions') or '').split('Backend: ', 1)[-1]
        self.mark('plug started', cmd=cmd, backend=backend)
        return c

    def call(self, c, name, args, show_args, key):
        self.say('')
        self.say(f'-> {name} {show_args}'.rstrip(), pause=0.9)
        r = c.call_tool(name, args)
        texts = [x.get('text', '') for x in r.get('content', []) if x.get('type') == 'text']
        main = texts[0] if texts else ''
        try:
            j = json.loads(main)
        except ValueError:
            j = None
        err = bool(r.get('isError'))
        self.mark(f'reply: {key}', tool=name, isError=err)
        self.rows.append({'key': key, 'tool': name, 'arguments': args, 'isError': err, 'texts': texts})
        # the reply's own fields, word for word (only the keys that matter here; nothing reworded)
        self.say('<- reply' + ('   isError: true' if err else ''), pause=0.3)
        q = lambda k, v: f'"{k}": {json.dumps(v, ensure_ascii=False)}'
        if isinstance(j, dict):
            if 'failed' in j:
                f = j['failed']
                self.say(q('failed', {'index': f.get('index'), 'error': f.get('error')}), 3, pause=0.8)
                self.say(q('rolled_back', j.get('rolled_back')) + ',  ' + q('undone', j.get('undone')) + ',  ' + q('applied', j.get('applied')), 3)
            elif 'total' in j:
                bb = (j.get('bodies') or [{}])[0].get('bbox') or {}
                self.say(q('volume_mm3', (j.get('total') or {}).get('volume_mm3')), 3)
                self.say('"bbox": min ' + json.dumps(bb.get('min')) + '  max ' + json.dumps(bb.get('max')), 3)
            elif 'display_value' in j:
                self.say(q('name', j.get('name')) + ',  ' + q('value', j.get('value')), 3)
            elif 'completed' in j:
                self.say(q('ok', j.get('ok')) + ',  ' + q('completed', j.get('completed')), 3)
            elif 'bytes' in j:
                self.say(q('path', j.get('path')) + ',  ' + q('bytes', j.get('bytes')), 3)
            elif 'timeline' in j:
                self.say(q('timeline', j.get('timeline') if not j.get('timeline') else f'[{len(j["timeline"])} features]') + ',  '
                         + q('bodies', j.get('bodies') if not j.get('bodies') else f'[{len(j["bodies"])} bodies]'), 3)
            else:
                self.say(json.dumps(j)[:200], 3)
        else:
            self.say(main, 3)
        for t in texts[1:]:
            self.say(t, 3)
        self.nap(1.5)
        return r, j

    def wait(self, n, what):
        self.say(f'# ({what})', pause=0.2)
        open(os.path.join(self.out, f'wait-{n}'), 'w').write(what)
        self.mark(f'wait {n}: {what}')
        while not os.path.exists(os.path.join(self.out, f'go-{n}')):
            time.sleep(0.2)
        self.mark(f'go {n}')

    def save(self):
        json.dump(self.rows, open(os.path.join(self.out, 'story.json'), 'w'), indent=1, ensure_ascii=False)


def headless(s):
    c = s.plug([NEW, 'mcp'], 'SolidCraft is NOT open.')
    s.call(c, 'batch', {'commands': HOOK}, "(lesson 3's hook: 5 names, the J, extrude)", 'h-build')
    s.wait(1, 'now SolidCraft opens')
    s.call(c, 'set_parameter', {'name': 'hook_depth', 'value': 40}, 'hook_depth = 40', 'h-after-open')
    s.call(c, 'measure', {}, '', 'h-measure')
    c.close()
    s.say('')
    c = s.plug([NEW, 'mcp'], 'A new plug, SolidCraft already open:')
    s.call(c, 'inspect_design', {'measure': False, 'sketches': False}, '', 'b-inspect')
    s.call(c, 'batch', {'commands': HOOK}, "(lesson 3's hook again)", 'b-build')
    s.call(c, 'measure', {}, '', 'b-measure')
    s.wait(2, 'now SolidCraft is closed')
    s.call(c, 'measure', {}, '', 'b-after-close')
    s.call(c, 'measure', {}, '(again)', 'b-after-close-2')
    c.close()


def errors(s):
    c = s.plug([NEW, 'mcp'], 'SolidCraft is open.')
    s.call(c, 'batch', {'commands': HOOK}, "(lesson 3's hook)", 'e-build')
    s.call(c, 'measure', {}, '', 'e-measure-0')
    s.call(c, 'batch', {'commands': TYPO}, '[0] hook_depth = 40   [1] lip_height = hook_dept / 4', 'e-typo')
    s.call(c, 'measure', {}, '', 'e-measure-after-typo')
    s.call(c, 'batch', {'commands': FIXED}, '[0] hook_depth = 40   [1] lip_height = hook_depth / 4', 'e-fixed')
    s.call(c, 'measure', {}, '', 'e-measure-fixed')
    s.call(c, 'save', {'path': DOCS + '/hook.sc'}, '~/Documents/hook.sc', 'e-save-refused')
    c.close()
    s.say('')
    c = s.plug([NEW, 'mcp', '--allow-path', DOCS], 'The plug started with two more arguments:')
    s.call(c, 'save', {'path': DOCS + '/hook.sc'}, '~/Documents/hook.sc', 'e-save-allowed')
    c.close()
    s.say('')
    s.wait(3, 'the same file, opened with the older SolidCraft 0.26.1')
    c = s.plug([OLD, 'mcp', '--allow-path', DOCS], 'SolidCraft 0.26.1 open, with its own plug:')
    s.call(c, 'open', {'path': DOCS + '/hook.sc'}, '~/Documents/hook.sc', 'e-old-open')
    c.close()


if __name__ == '__main__':
    what, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    st = Story(out)
    try:
        {'headless': headless, 'errors': errors}[what](st)
    finally:
        st.save()
    st.say('# end')
