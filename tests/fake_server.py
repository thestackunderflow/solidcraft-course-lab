"""A fake stdio MCP server for the client tests: answers initialize, tools/list and tools/call; 'sleep' never answers."""
import json
import sys

for line in iter(sys.stdin.readline, ""):
    m = json.loads(line)
    if 'id' not in m:
        continue
    if m['method'] == 'initialize':
        r = {'protocolVersion': '2025-06-18', 'serverInfo': {'name': 'fake', 'version': '1'},
             'instructions': 'fake server'}
    elif m['method'] == 'tools/list':
        r = {'tools': [{'name': 'measure'}, {'name': 'batch'}]}
    elif m['method'] == 'tools/call':
        name = m['params']['name']
        if name == 'sleep':
            continue
        if name == 'fail':
            r = {'content': [{'type': 'text', 'text': 'no SolidCraft app is listening at 127.0.0.1:27878'}], 'isError': True}
        else:
            r = {'content': [{'type': 'text', 'text': json.dumps({'total': {'volume_mm3': 8000.0}})}]}
    else:
        print(json.dumps({'jsonrpc': '2.0', 'id': m['id'], 'error': {'code': -32601, 'message': 'no'}}), flush=True)
        continue
    print('{"jsonrpc": "2.0", "method": "notifications/message", "params": {}}', flush=True)
    print(json.dumps({'jsonrpc': '2.0', 'id': m['id'], 'result': r}), flush=True)
