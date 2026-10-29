"""Reading Claude Code's terminal screen (the text of `tmux capture-pane -p`), so the lab script knows when a reply is
still running and when Claude Code asks for an approval. Nothing here types for Claude: the script only waits, and
answers an approval prompt with its own "Yes" option (as a viewer would click it)."""
import re

BUSY = re.compile(r'esc to interrupt', re.IGNORECASE)
ASK = re.compile(r'Do you want to (proceed|allow|make this)', re.IGNORECASE)
DONE = re.compile(r'[A-Z]\w+ for [0-9hms ]+· done [0-9]')   # 2.1.311: "Worked for 6s · done 1:10 AM", "Sautéed for 41s ..." (\w: non-ASCII verbs)
YES = re.compile(r'^\s*[❯>]?\s*(\d)\.\s+Yes\b', re.MULTILINE)


def busy(text):
    return bool(BUSY.search(text or ''))


def approval(text):
    return bool(ASK.search(text or '')) and bool(YES.search(text or ''))


def approval_key(text):
    m = YES.search(text or '')
    return m.group(1) if m else None


def turns_done(text):
    """How many end-of-turn lines the screen shows (a turn is over when this count goes up)."""
    return len(DONE.findall(text or ''))
