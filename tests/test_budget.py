"""The spending ledger: only rows below the GO line count; a run may start only if it cannot cross the stop line."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'claude-run'))
import budget  # noqa: E402


def test_only_rows_below_the_go_line_count(tmp_path):
    p = tmp_path / 'b.tsv'
    p.write_text('# run\tcost_usd\tkind\tlab\nold\t5.0\tlogged\tx\n' + budget.MARK + ' cap $1\n'
                 'a\t0.25\tlogged\tsc1\n', encoding='utf-8')
    assert budget.total(str(p)) == 0.25


def test_check_stops_before_the_stop_line():
    assert budget.STOP_AT == 0.90
    assert budget.allowed(0.30, 0.50)
    assert not budget.allowed(0.50, 0.50)


def test_a_killed_run_counts_at_its_cap(tmp_path):
    p = tmp_path / 'b.tsv'
    p.write_text(budget.MARK + '\n', encoding='utf-8')
    assert budget.record(str(p), 'r1', None, 0.3, 'sc1') == 0.3
    assert budget.record(str(p), 'r2', 0.1, 0.3, 'sc1') == 0.4
