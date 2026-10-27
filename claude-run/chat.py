"""One fresh headless Claude Code chat with fixed messages, sent one at a time (stream-json in and out); each reply is
awaited before the next message. Every event goes to session.jsonl; turns.json keeps each message, its start and end
(UTC, to match the footage), Claude's final text and the cost the result event reports.
    python claude-run/chat.py RUN_DIR WORK_DIR MCP_CONFIG BUDGET MODEL "message 1" ["message 2" ...]
Between turns it runs $AFTER_TURN (if set) with the turn number as its argument (the live run takes a screenshot)."""
import datetime
import json
import os
import subprocess
import sys


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='milliseconds')


def main(run, work, mcp_config, budget, model, messages):
    log = os.path.join(run, 'instructions-loaded.jsonl').replace(chr(92), '/')
    settings = {'claudeMdExcludes': ['**/.claude/CLAUDE.md', '**/CLAUDE.md'], 'autoMemoryEnabled': False,
                'hooks': {'InstructionsLoaded': [{'hooks': [{'type': 'command',
                          'command': f"python -c \"import sys; open(r'{log}', 'a').write(sys.stdin.read() + chr(10))\""}]}]}}
    cmd = [os.environ.get('CLAUDE', 'claude'), '-p', '--input-format', 'stream-json', '--output-format', 'stream-json',
           '--verbose', '--model', model, '--mcp-config', mcp_config, '--strict-mcp-config', '--tools', '',
           '--allowedTools', 'mcp__solidcraft__*', '--permission-mode', 'dontAsk', '--max-budget-usd', str(budget),
           '--no-session-persistence', '--setting-sources', 'project,local', '--settings', json.dumps(settings)]
    env = dict(os.environ, CLAUDE_CODE_DISABLE_AUTO_MEMORY='1', ENABLE_TOOL_SEARCH='false', MSYS_NO_PATHCONV='1')
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=open(os.path.join(run, 'claude-stderr.txt'), 'w'),
                         text=True, encoding='utf-8', cwd=work, env=env, shell=False)
    out = open(os.path.join(run, 'session.jsonl'), 'w', encoding='utf-8')
    turns = []
    for i, m in enumerate(messages, 1):
        t = {'turn': i, 'message': m, 'start': now()}
        p.stdin.write(json.dumps({'type': 'user', 'message': {'role': 'user', 'content': [{'type': 'text', 'text': m}]}}) + '\n')
        p.stdin.flush()
        result = None
        for line in p.stdout:
            out.write(line)
            out.flush()
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get('type') == 'result':
                result = d
                break
        t['end'] = now()
        if result is None:
            t['error'] = 'no result event (process ended)'
            turns.append(t)
            break
        t.update(result_text=result.get('result'), cost=result.get('total_cost_usd'), is_error=result.get('is_error'),
                 subtype=result.get('subtype'), num_turns=result.get('num_turns'))
        turns.append(t)
        if os.environ.get('AFTER_TURN'):
            subprocess.run(['bash', os.environ['AFTER_TURN'], str(i)])
        if result.get('is_error'):
            break
    p.stdin.close()
    for line in p.stdout:
        out.write(line)
    p.wait(timeout=120)
    costs = [t.get('cost') or 0 for t in turns]
    json.dump({'turns': turns, 'exit': p.returncode, 'cost_last': costs[-1] if costs else 0,
               'cost_sum': round(sum(costs), 6)}, open(os.path.join(run, 'turns.json'), 'w', encoding='utf-8'), indent=1)
    # Conservative: the ledger takes the larger of "the last result's total" and "the sum of every result's total".
    print(max(costs[-1] if costs else 0, sum(costs)))


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[0], a[1], a[2], float(a[3]), a[4], a[5:])
