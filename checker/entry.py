"""Read a Claude app's MCP config file and return the solidcraft entry (Claude Desktop's claude_desktop_config.json and
Claude Code's ~/.claude.json both keep servers under "mcpServers")."""
import hashlib
import json
import os


def sha256(path):
    if not os.path.exists(path):
        return None
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def read(path, name='solidcraft'):
    out = {'path': path, 'exists': os.path.exists(path), 'found': False, 'command': None, 'args': None,
           'other_servers': [], 'problems': []}
    if not out['exists']:
        return out
    try:
        d = json.load(open(path, encoding='utf-8'))
    except ValueError as e:
        out['problems'].append(f'does not parse: {e}')
        return out
    servers = d.get('mcpServers') or {}
    out['other_servers'] = sorted(k for k in servers if k != name)
    e = servers.get(name)
    if not isinstance(e, dict):
        return out
    out.update(found=True, command=e.get('command'), args=e.get('args'), entry=e)
    if not (isinstance(out['command'], str) and os.path.isabs(out['command'])):
        out['problems'].append('command is not a full path')
    if out['args'] != ['mcp']:
        out['problems'].append('args are not exactly ["mcp"]')
    return out
