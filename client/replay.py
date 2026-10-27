"""The proof: replay the tools/call requests Claude sent (from the logging proxy's transcript.jsonl), in order, over
the same entry, and read the volume SolidCraft measures.

    python3 -m client.replay TRANSCRIPT OUT.json -- COMMAND...   (COMMAND = the entry SolidCraft wrote)
"""
import json
import sys


def logged_calls(path):
    calls = []
    for line in open(path, encoding='utf-8'):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        m = r.get('msg')
        if r.get('dir') == 'client->server' and isinstance(m, dict) and m.get('method') == 'tools/call':
            p = m.get('params') or {}
            calls.append({'seq': r.get('seq'), 'name': p.get('name'), 'arguments': p.get('arguments') or {}})
    return calls


def total_volume(reply):
    if not isinstance(reply, dict):
        return None
    t = (reply.get('total') or {}).get('volume_mm3')
    return t


def main(argv):
    from client.mcp import McpClient
    transcript, out = argv[0], argv[1]
    cmd = argv[argv.index('--') + 1:]
    calls = logged_calls(transcript)
    c = McpClient(cmd, timeout_s=330, log_path=out.replace('.json', '-transcript.jsonl'))
    init = c.start()
    rows = []
    for call in calls:
        r = c.call_tool(call['name'], call['arguments'])
        rows.append({'logged_seq': call['seq'], 'name': call['name'], 'isError': bool(r.get('isError')),
                     'reply': McpClient.text_json(r)})
    c.close()
    vols = [total_volume(x['reply']) for x in rows if x['name'] == 'measure']
    res = {'calls': len(calls), 'names': [x['name'] for x in rows], 'errors': sum(x['isError'] for x in rows),
           'measured_volume_mm3': vols[-1] if vols else None, 'server_instructions': init.get('instructions'),
           'rows': rows}
    json.dump(res, open(out, 'w', encoding='utf-8'), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, indent=1))
    return res


if __name__ == '__main__':
    main(sys.argv[1:])
