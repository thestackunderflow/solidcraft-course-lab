"""The site check reads the version a download page offers from its visible text."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
from sitecheck import parse  # noqa: E402


def test_versions_in_order_of_appearance():
    t = 'SolidCraft 0.24.1 Released October 27, 2026. Download for Windows. Older: v0.22.0'
    assert parse.versions(t) == ['0.24.1', '0.22.0']


def test_offered_is_the_first_version_on_the_page():
    assert parse.offered('Download SolidCraft v0.22.0 (Released October 24, 2026)') == '0.22.0'
    assert parse.offered('no versions here') is None


def test_ignores_ip_addresses_and_longer_numbers():
    assert parse.versions('connect to 127.0.0.1 then 1.2.3.4.5 and 0.24.1') == ['0.24.1']


def test_compare_with_the_pin():
    assert parse.verdict('0.24.1', '0.24.1') == 'serves the pinned version'
    assert parse.verdict('0.22.0', '0.24.1') == 'lags the pinned version'
    assert parse.verdict(None, '0.24.1') == 'no version found'
