"""Redact account fields, the plan name and e-mail addresses in a Claude run's text logs before they are committed.
    python lab/fx9redact.py RUN_DIR
organizationUuid / accountUuid / organizationName / emailAddress values become "[redacted]" (also inside JSON strings
that hold JSON, where the quotes are escaped); "· Claude Ultra" (any plan name) becomes "· [plan]"; any e-mail address
becomes [email]. Host paths are scrub.py's job."""
import os
import re
import sys

BS = chr(92)                     # a backslash, spelled out (shells and heredocs eat them)
Q = BS + BS + '?"'               # regex: an optional backslash, then a quote
KEYS = ('organizationUuid', 'accountUuid', 'organizationName', 'emailAddress', 'userEmail', 'email')
PLAN = re.compile('(·\\s*)Claude (Ultra|Max|Pro|Team|Enterprise)\\b')
MAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
n = 0
for root, _, files in os.walk(sys.argv[1]):
    for f in files:
        if not f.endswith(('.json', '.jsonl', '.txt', '.log')):
            continue
        p = os.path.join(root, f)
        s = open(p, encoding='utf-8', errors='surrogateescape').read()
        t = s
        for k in KEYS:
            t = re.sub('(' + Q + k + Q + r'\s*:\s*' + Q + ')[^"' + BS + BS + ']*', lambda m: m.group(1) + '[redacted]', t)
        t = PLAN.sub(lambda m: m.group(1) + '[plan]', t)
        t = MAIL.sub('[email]', t)
        if t != s:
            open(p, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(t)
            n += 1
print(f'redacted {n} files in {sys.argv[1]}')
