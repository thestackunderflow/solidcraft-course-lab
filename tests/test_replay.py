"""The proof replays Claude's logged tool calls in order; it must take exactly the tools/call requests Claude sent."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from client import replay  # noqa: E402


def row(seq, d, msg):
    return json.dumps({'t': '2026-10-27T00:00:00.000+00:00', 'seq': seq, 'dir': d, 'msg': msg})


def test_takes_only_tools_call_requests_in_order(tmp_path):
    p = tmp_path / 't.jsonl'
    rows = [
        row(1, 'client->server', {'jsonrpc': '2.0', 'id': 0, 'method': 'initialize', 'params': {}}),
        row(2, 'server->client', {'jsonrpc': '2.0', 'id': 0, 'result': {}}),
        row(3, 'client->server', {'jsonrpc': '2.0', 'id': 1, 'method': 'tools/list'}),
        row(4, 'client->server', {'jsonrpc': '2.0', 'id': 2, 'method': 'tools/call',
                                  'params': {'name': 'inspect_design', 'arguments': {}}}),
        row(5, 'server-stderr', 'noise'),
        row(6, 'client->server', {'jsonrpc': '2.0', 'id': 3, 'method': 'tools/call',
                                  'params': {'name': 'batch', 'arguments': {'commands': [{'command': 'solid.box'}]}}}),
        row(7, 'client->server', {'jsonrpc': '2.0', 'id': 4, 'method': 'tools/call',
                                  'params': {'name': 'measure', 'arguments': {}}}),
    ]
    p.write_text('\n'.join(rows) + '\n', encoding='utf-8')
    calls = replay.logged_calls(str(p))
    assert [c['name'] for c in calls] == ['inspect_design', 'batch', 'measure']
    assert calls[1]['arguments'] == {'commands': [{'command': 'solid.box'}]}
    assert [c['seq'] for c in calls] == [4, 6, 7]


def test_volume_from_a_measure_reply():
    reply = {'bodies': [{'name': 'Body 1', 'volume_mm3': 8000.000001, 'closed': True}],
             'total': {'volume_mm3': 8000.000001}}
    assert replay.total_volume(reply) == 8000.000001
    assert replay.total_volume({'bodies': []}) is None
