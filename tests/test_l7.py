"""Lesson 7 helpers: the approval policy reads only the prompt's own lines (R1 was stopped because the first version
missed Claude Code's em dash), and the filmed test script prints replies word for word on one line per wrap."""
import io
import os
import sys
import types
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
LAB = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(LAB, 'lab'))
sys.path.insert(0, LAB)
sys.modules.setdefault('l2drive', types.SimpleNamespace(Run=object, keys=None, pane=None, tui=None, TURN_LIMIT_S=0, QUIET_S=0))
import l7drive  # noqa: E402


def prompt(path):
    return open(os.path.join(LAB, 'out', 'l7', 'runs', path), encoding='utf-8').read()


def test_a_solidcraft_prompt_with_an_em_dash_gets_yes():
    assert l7drive.decide(1, 1, prompt('R1/approval-1-1.txt')) == 'yes'


def test_a_shell_prompt_gets_no_even_when_the_message_names_solidcraft():
    assert l7drive.decide(2, 2, prompt('R1/approval-2-1.txt')) == 'no'


def test_r2_prompts_were_all_solidcraft_tools():
    folder = os.path.join(LAB, 'out', 'l7', 'runs', 'R2')
    files = [f for f in os.listdir(folder) if f.startswith('approval-')]
    assert files and all(l7drive.decide(1, 2, open(os.path.join(folder, f), encoding='utf-8').read()) == 'yes' for f in files)


def test_story_prints_the_reply_words_unchanged(tmp_path):
    import l7story
    l7story.PACE = 0
    st = l7story.Story(str(tmp_path))
    buf = io.StringIO()
    with redirect_stdout(buf):
        st.say('Note: this is a headless session because the SolidCraft app was not\n   found; the user cannot see this work.', 3)
    out = ' '.join(buf.getvalue().split())
    assert out == 'Note: this is a headless session because the SolidCraft app was not found; the user cannot see this work.'
    assert all(len(line) <= l7story.COLS for line in buf.getvalue().splitlines())
