from __future__ import annotations

from collections import defaultdict

from school.config import load_school_config


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def generate_weekly_timetable(guild_id: int) -> dict:
    config = load_school_config(guild_id)
    periods = config.get("periods", [])
    table = defaultdict(list)
    for day in DAYS:
        for idx, period in enumerate(periods):
            table[day].append({"slot": idx + 1, "name": period["name"], "time": f"{period['start']}-{period['end']}"})
    return dict(table)
