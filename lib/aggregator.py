# lib/aggregator.py

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date, timedelta
from typing import List, Optional

from lib.parser import parse_pln


DATA_ROOT = "data"


@dataclass
class DateRange:
    start: date
    end: date

@dataclass
class DayEntry:
    blocks: list
    date: date


def iter_date_range(start: date, end: date):
    """Yield all dates in range [start, end]."""
    current = start
    while current <= end:
        yield current
        current += timedelta(days=1)


def pln_path_for(d: date) -> str:
    """Convert date → file path."""
    return os.path.join(
        DATA_ROOT,
        str(d.year),
        f"{d.month:02d}",
        f"{d.year}-{d.month:02d}-{d.day:02d}.pln",
    )


def load_day(d: date):
    """Load a single .pln file if it exists.
    Returns a DayEntry associated with the file."""
    path = pln_path_for(d)

    if not os.path.exists(path):
        return None

    with open(path, "r", encoding='utf-8') as pln_text:
        return DayEntry(parse_pln(pln_text.read()), d)


def get_days(start: date, end: date):
    """
    Main aggregator:
    returns list of parsed DayEntry objects
    """
    days = []

    for d in iter_date_range(start, end):
        entry = load_day(d)
        if entry is not None:
            days.append(entry)

    return days


def get_default_range(days_back: int = 90, days_forward: int = 14):
    """Default: last N days ending today."""
    end = date.today() + timedelta(days=days_forward)
    start = date.today() - timedelta(days=days_back)
    return DateRange(start=start, end=end)
