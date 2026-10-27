#!/bin/bash
# Q1: which version does solidcraft.io/download offer today? The page in a real browser (headless Chromium, JavaScript
# on, the DOM after scripts ran), the same page with curl (no JavaScript), and GitHub's latest stable release. Host side:
#   docker run --rm --memory 2g --shm-size 1g -v "$PWD:/work" sc1-browser:1 bash /work/sitecheck/check.sh
set -u
O=/work/out/l1/sitecheck
[ -e "$O" ] && { echo "refusing: $O exists"; exit 1; }
mkdir -p "$O"
URL=https://solidcraft.io/download/
date -u +%Y-%m-%dT%H:%M:%SZ > "$O/read-at.txt"
chromium --version > "$O/browser-version.txt" 2>&1
curl -fsSL -A "Mozilla/5.0 (lab site check)" "$URL" -o "$O/curl.html"; echo "curl exit $?" >> "$O/read-at.txt"
chromium --headless=new --no-sandbox --disable-gpu --virtual-time-budget=20000 --dump-dom "$URL" > "$O/browser.html" 2> "$O/browser-stderr.txt"
chromium --headless=new --no-sandbox --disable-gpu --virtual-time-budget=20000 --window-size=1280,1600 --screenshot="$O/browser.png" "$URL" 2>> "$O/browser-stderr.txt"
curl -fsSL https://api.github.com/repos/tangency-labs/solidcraft/releases/latest -o "$O/github-latest.json"
python3 - "$O" <<'EOF'
import html, json, os, re, sys
sys.path.insert(0, '/work')
from sitecheck import parse
o = sys.argv[1]
def text(f):
    s = open(os.path.join(o, f), encoding='utf-8', errors='replace').read()
    s = re.sub(r'(?is)<(script|style)\b.*?</\1>', ' ', s)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
gh = json.load(open(os.path.join(o, 'github-latest.json')))
pin = gh['tag_name'].lstrip('v')
res = {'read_at': open(os.path.join(o, 'read-at.txt')).readline().strip(), 'github_latest': pin,
       'github_published_at': gh['published_at']}
for k, f in (('curl_no_js', 'curl.html'), ('browser_js', 'browser.html')):
    t = text(f)
    open(os.path.join(o, f.replace('.html', '-text.txt')), 'w', encoding='utf-8').write(t + '\n')
    v = parse.offered(t)
    res[k] = {'versions_on_page': parse.versions(t)[:10], 'offered': v, 'verdict': parse.verdict(v, pin)}
json.dump(res, open(os.path.join(o, '..', 'sitecheck.json'), 'w'), indent=1)
print(json.dumps(res, indent=1))
EOF
