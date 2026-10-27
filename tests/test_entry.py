"""checker.entry reads a Claude app's config file and returns the solidcraft entry SolidCraft wrote."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from checker import entry  # noqa: E402


def test_finds_the_entry_and_keeps_other_servers(tmp_path):
    p = tmp_path / 'claude_desktop_config.json'
    p.write_text(json.dumps({'mcpServers': {
        'other': {'command': 'x'},
        'solidcraft': {'command': '/opt/solidcraft-0.24.1/bin/solidcraft-cli', 'args': ['mcp']}}}), encoding='utf-8')
    e = entry.read(str(p))
    assert e['found'] is True
    assert e['command'] == '/opt/solidcraft-0.24.1/bin/solidcraft-cli'
    assert e['args'] == ['mcp']
    assert e['other_servers'] == ['other']
    assert e['problems'] == []


def test_no_file_and_no_entry(tmp_path):
    assert entry.read(str(tmp_path / 'missing.json'))['found'] is False
    p = tmp_path / 'c.json'
    p.write_text('{"mcpServers": {}}', encoding='utf-8')
    e = entry.read(str(p))
    assert e['found'] is False
    assert e['exists'] is True


def test_a_file_that_does_not_parse(tmp_path):
    p = tmp_path / 'c.json'
    p.write_text('{nope', encoding='utf-8')
    e = entry.read(str(p))
    assert e['found'] is False
    assert e['problems'] and 'parse' in e['problems'][0]


def test_problems_named(tmp_path):
    p = tmp_path / 'c.json'
    p.write_text(json.dumps({'mcpServers': {'solidcraft': {'command': 'solidcraft-cli', 'args': ['mcp', '--connect', '127.0.0.1:7878']}}}),
                 encoding='utf-8')
    e = entry.read(str(p))
    assert 'command is not a full path' in e['problems']
    assert 'args are not exactly ["mcp"]' in e['problems']


def test_hash_changes_only_with_content(tmp_path):
    p = tmp_path / 'c.json'
    p.write_text('{"a": 1}', encoding='utf-8')
    h1 = entry.sha256(str(p))
    p.write_text('{"a": 1}', encoding='utf-8')
    assert entry.sha256(str(p)) == h1
    p.write_text('{"a": 2}', encoding='utf-8')
    assert entry.sha256(str(p)) != h1
    assert entry.sha256(str(tmp_path / 'none')) is None
