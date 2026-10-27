"""The scripted MCP client (no AI) used by the start-order cases and the replay, against a fake server."""
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from client.mcp import McpClient, Hang  # noqa: E402

CMD = [sys.executable, os.path.join(HERE, 'fake_server.py')]


def test_initialize_list_and_call(tmp_path):
    log = tmp_path / 'log.jsonl'
    c = McpClient(CMD, timeout_s=5, log_path=str(log))
    init = c.start()
    assert init['instructions'] == 'fake server'
    assert [t['name'] for t in c.list_tools()] == ['measure', 'batch']
    assert c.tool_json('measure', {})['total']['volume_mm3'] == 8000.0
    c.close()
    rows = [json.loads(x) for x in log.read_text(encoding='utf-8').splitlines()]
    assert rows[0]['dir'] == 'client->server' and rows[0]['msg']['method'] == 'initialize'
    assert any(r['dir'] == 'server->client' for r in rows)


def test_an_error_result_is_returned_not_raised():
    c = McpClient(CMD, timeout_s=5)
    c.start()
    r = c.call_tool('fail', {})
    assert r['isError'] is True
    assert McpClient.text(r).startswith('no SolidCraft app is listening')
    c.close()


def test_no_reply_raises_hang():
    c = McpClient(CMD, timeout_s=1)
    c.start()
    with pytest.raises(Hang):
        c.call_tool('sleep', {})
    c.kill()
