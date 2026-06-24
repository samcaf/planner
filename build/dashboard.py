from datetime import date
from pathlib import Path
import argparse

from lib.aggregator import get_days, get_default_range
from lib.date_utils import resolve_date
from lib.render import render


OUTPUT_PATH = Path("build/dashboard.html")


def build_dashboard(days, auto_refresh):
    """
    days: List[DayEntry]
    """

    rendered_days = []

    # reverse chronological (newest first)
    for day_entry in sorted(days, key=lambda d: d.date, reverse=True):
        day_html = render(
            day_entry.blocks,
            day_entry.date.strftime("%Y-%m-%d"),
        )

        # wrap each day
        rendered_days.append(f"""
        <div class="day">
            {day_html}
        </div>
        """)

    return f"""
<!DOCTYPE html>
<html>
<head>
    {'<meta http-equiv="refresh" content="30">\n' if auto_refresh else ''}<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
</head>

<body>

<div class="dashboard-root">
    {''.join(rendered_days)}
</div>

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--days", type=int)
    parser.add_argument("--day")
    parser.add_argument("--start")
    parser.add_argument("--end")
    parser.add_argument("--auto_refresh", default=True)

    args = parser.parse_args()

    if args.day:
        start = resolve_date(args.day)
        end = start
    elif args.start and args.end:
        start = resolve_date(args.start)
        end = resolve_date(args.end)
    else:
        date_range = get_default_range(args.days or 90)
        start = date_range.start
        end = date_range.end

    days = get_days(start, end)

    html = build_dashboard(days, args.auto_refresh)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
