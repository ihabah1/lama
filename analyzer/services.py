from __future__ import annotations

import json
import random
from pathlib import Path

import pandas as pd
from django.conf import settings

approved_combos: set[tuple[int, ...]] = set()
history_sets: list[set[int]] = []
history_df: pd.DataFrame | None = None
init_error: str | None = None
_initialized = False


def _data_path(name: str) -> Path:
    return Path(settings.DATA_DIR) / name


def init_data() -> None:
    global approved_combos, history_sets, history_df, init_error, _initialized
    if _initialized:
        return
    _initialized = True
    potential_path = _data_path("Potential_Wins.csv")
    lotto_path = _data_path("Lotto.csv")
    try:
        potential_df = pd.read_csv(potential_path)
        approved_combos = {
            tuple(sorted(int(x) for x in row))
            for row in potential_df.iloc[:, :6].values
        }
        history_df = pd.read_csv(lotto_path)
        history_sets = []
        for row in history_df.iloc[:, 2:8].values:
            try:
                history_sets.append(set(map(int, row)))
            except (TypeError, ValueError):
                continue
        init_error = None
    except Exception as exc:  # noqa: BLE001 — startup resilience
        init_error = str(exc)
        approved_combos = set()
        history_sets = []
        history_df = None


def get_rejection_reason(nums: list[int]) -> str:
    user_set = set(nums)
    if history_df is None or not history_sets:
        return "נפסל: מאגר ההיסטוריה לא זמין או ריק."
    for i, hist in enumerate(history_sets):
        match = len(user_set.intersection(hist))
        if match == 6:
            draw = history_df.iloc[i, 0]
            return f"נפסל: הצירוף זכה בעבר (הגרלה {draw})"
        if match == 5:
            return "נפסל: דמיון גבוה מדי (5 מספרים) לזכייה היסטורית"
    return (
        "נפסל: מבנה סטטיסטי חלש (רצפים, פיזור לא תקין או דמיון ל-100 האחרונות)"
    )


def decade_spread_score(combo: tuple[int, ...]) -> int:
    buckets: set[int] = set()
    for n in combo:
        if n <= 9:
            buckets.add(0)
        elif n <= 19:
            buckets.add(1)
        elif n <= 29:
            buckets.add(2)
        else:
            buckets.add(3)
    return len(buckets)


def suggest_coverage(count: int) -> list[list[int]]:
    n = min(count, len(approved_combos))
    if n <= 0:
        return []
    sample = random.sample(list(approved_combos), n)
    return [list(c) for c in sample]


def suggest_top_stat(limit: int = 50) -> list[list[int]]:
    if not history_sets or not approved_combos:
        return []
    all_past = [n for s in history_sets for n in s]
    top_10 = pd.Series(all_past).value_counts().head(10).index.tolist()
    top_10_set = set(int(x) for x in top_10)
    results: list[list[int]] = []
    for combo in approved_combos:
        if len(set(combo).intersection(top_10_set)) >= 3:
            results.append(list(combo))
        if len(results) >= limit:
            break
    return results


def suggest_diverse(limit: int = 50) -> list[list[int]]:
    """Favor combinations that spread across decade buckets (1–9, 10–19, 20–29, 30–37)."""
    if not approved_combos:
        return []
    scored = [(decade_spread_score(c), c) for c in approved_combos]
    max_score = max((s for s, _ in scored), default=0)
    best = [c for s, c in scored if s == max_score]
    if len(best) > limit:
        best = random.sample(best, limit)
    return [list(c) for c in best[:limit]]


def parse_json_body(request) -> dict:
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return {}
