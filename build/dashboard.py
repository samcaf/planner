from datetime import date
from pathlib import Path
import argparse

from lib.aggregator import get_days, get_default_range
from lib.date_utils import resolve_date
from lib.render import render


OUTPUT_PATH = Path("build/dashboard.html")


def build_dashboard(days):
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

        # IMPORTANT: wrap each day
        rendered_days.append(f"""
        <div class="day">
            {day_html}
        </div>
        """)

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
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

    args = parser.parse_args()

    if args.day:
        start = resolve_date(args.day)
        end = start

    elif args.start and args.end:
        start = resolve_date(args.start)
        end = resolve_date(args.end)

    else:
        rng = get_default_range(args.days or 90)
        start = rng.start
        end = rng.end

    days = get_days(start, end)

    html = build_dashboard(days)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Generated {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
