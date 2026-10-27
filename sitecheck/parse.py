"""Read the version a download page offers from its visible text."""
import re

VER = re.compile(r'(?<![\d.])v?(\d+\.\d+\.\d+)(?![\d.]*\d)')


def versions(text):
    out = []
    for m in VER.finditer(text):
        s = m.group(0)
        start, end = m.span()
        if text[end:end + 1] == '.' and text[end + 1:end + 2].isdigit():
            continue
        out.append(m.group(1))
    return out


def offered(text):
    v = versions(text)
    return v[0] if v else None


def verdict(found, pin):
    if found is None:
        return 'no version found'
    return 'serves the pinned version' if found == pin else 'lags the pinned version'
