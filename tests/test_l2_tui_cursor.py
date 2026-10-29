"""Lesson 2 lab helpers: reading Claude Code's terminal screen (tmux capture-pane text) to know when a reply is done or
an approval is asked, and the cursor log the footage crop follows."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from client import tui  # noqa: E402
from lab import cursorlog  # noqa: E402

IDLE = """ > Make the J
  ⎿  Done.
────────────────────────
❯
────────────────────────
  ⏵⏵ auto mode on (shift+tab to cycle)"""
BUSY = """✻ Thinking… (esc to interrupt)
────────────────────────
❯
────────────────────────"""
ASK = """ Tool use
   solidcraft - execute (MCP)
 Do you want to proceed?
 ❯ 1. Yes
   2. Yes, and don't ask again for solidcraft - execute commands in /root
   3. No, and tell Claude what to do differently (esc)"""


def test_busy_while_the_spinner_line_shows():
    assert tui.busy(BUSY) is True
    assert tui.busy(IDLE) is False


def test_an_approval_prompt_is_seen_and_answered_with_its_yes_option():
    assert tui.approval(ASK) is True
    assert tui.approval(IDLE) is False
    assert tui.approval_key(ASK) == '1'


def test_location_line_from_xdotool():
    assert cursorlog.parse('x:960 y:1000 screen:0 window:2097154') == (960, 1000)
    assert cursorlog.parse('garbage') is None


def test_log_rows_are_seconds_from_the_recording_start(tmp_path):
    p = tmp_path / 'cursor.jsonl'
    with open(p, 'w') as f:
        cursorlog.write_row(f, 100.0, 100.25, (10, 20))
        cursorlog.write_row(f, 100.0, 100.5, (12, 22))
    rows = [json.loads(x) for x in p.read_text().splitlines()]
    assert rows == [{'t': 0.25, 'x': 10, 'y': 20}, {'t': 0.5, 'x': 12, 'y': 22}]


DONE_2_1_311 = """  2. Extrude1 (ExtrudeFeature, id 2): 20 mm
     along +Y, creating Body1.

✻ Worked for 6s · done 1:10 AM

──────────────────────────────────────────────
❯ Flip it so it rises up in +Z
──────────────────────────────────────────────
  ⏵⏵ auto mode on (shift+tab to cycle)"""


def test_claude_code_2_1_311_end_of_turn_line_is_seen():
    # lab run claude-1: 2.1.311 printed "Worked for 6s · done" and no "esc to interrupt" was ever sampled
    assert tui.turns_done(DONE_2_1_311) == 1
    assert tui.turns_done(IDLE) == 0
    assert tui.turns_done(DONE_2_1_311 + '\n✻ Worked for 3s · done 1:12 AM') == 2


def test_end_of_turn_line_with_a_non_ascii_verb():
    # lesson 3 run B1: Claude Code 2.1.311 ended a turn with "Sautéed for 41s"; the ASCII-only pattern missed it
    from client import tui
    assert tui.turns_done('✻ Sautéed for 41s · done 7:40 PM') == 1
