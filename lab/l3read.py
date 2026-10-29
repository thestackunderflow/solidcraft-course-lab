"""Lesson 3: the no-AI read of a design (after a recording stops): a scripted MCP client over the entry SolidCraft
wrote (`solidcraft-cli mcp setup`), bridged to the open window: tools/list, inspect_design, measure and
parameters.list (through the execute tool). Writes RUN_DIR/read.json with a summary of what lesson 3 compares:
user parameters (names, values), sketch dimensions written from names, size, volume, Z range, corners, errors.
    python3 lab/l3read.py RUN_DIR [ENTRY_JSON]     (ENTRY_JSON: the entry as SolidCraft wrote it, for wrapped runs)"""
import json
import os
import sys

sys.path.insert(0, '/work')
from checker import entry, recipe  # noqa: E402
from client.mcp import McpClient  # noqa: E402


def dims_from_names(sk, user_names):
    """Sketch dimensions whose parameter expression uses a user parameter name (the 'fx' ones)."""
    out = []
    for k in sk.get('constraints') or []:
        if not k.get('param'):
            continue
        ex = str(k.get('expression') or k.get('param_expression') or '')
        out.append({'param': k.get('param'), 'expression': ex, 'value': k.get('value'),
                    'uses_names': any(n in ex for n in user_names)})
    return out


def summarise(ins, mea, plist):
    s = recipe.summary(ins, mea)
    params = (plist or {}).get('parameters') or []
    user = [p for p in params if (p.get('source') or '').lower().startswith('user')]
    names = [p.get('name') for p in user]
    model = [p for p in params if p not in user]
    sk = (ins.get('sketches') or [{}])[0]
    model_named = [p for p in model if any(n and n in str(p.get('expression') or '') for n in names)]
    s.update({'user_parameters': [{k: p.get(k) for k in ('name', 'expression', 'value', 'unit', 'used_by')} for p in user],
              'user_parameter_names': names,
              'model_parameters': [{k: p.get(k) for k in ('name', 'expression', 'value', 'feature', 'input')} for p in model],
              'model_parameters_from_names': len(model_named),
              'sketch_fully_constrained': sk.get('fully_constrained'), 'sketch_dof': sk.get('dof')})
    return s


def main(o, entry_json=None):
    if entry_json:
        e = json.load(open(entry_json))['mcpServers']['solidcraft']
        cmd = [e['command']] + list(e.get('args') or [])
    else:
        e = entry.read(os.path.expanduser('~/.claude.json'))
        cmd = [e['command']] + e['args']
    c = McpClient(cmd, timeout_s=120, log_path=os.path.join(o, 'read-transcript.jsonl'))
    c.start()
    json.dump(c.list_tools(), open(os.path.join(o, 'tools.json'), 'w'), indent=1)
    ins = McpClient.text_json(c.call_tool('inspect_design', {}))
    mea = McpClient.text_json(c.call_tool('measure', {}))
    pl = McpClient.text_json(c.call_tool('execute', {'command': 'parameters.list', 'params': {}}))
    c.close()
    s = summarise(ins, mea, pl if isinstance(pl, dict) else {})
    res = {'summary': s, 'inspect_design': ins, 'measure': mea, 'parameters_list': pl}
    json.dump(res, open(os.path.join(o, 'read.json'), 'w'), indent=1)
    print(json.dumps({k: s[k] for k in ('volume_mm3', 'bbox_mm', 'bbox_min', 'bbox_max', 'user_parameter_names',
                                         'model_parameters_from_names', 'sketch_dof', 'errors')}, indent=1))
    return res


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 and sys.argv[2].endswith('.json') else None)
