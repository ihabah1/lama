"""
יוצר את קובץ Potential_Wins.csv מתוך היסטוריית הגרלות (Lotto.csv).
הרצה: python build_potential_wins.py
אופציונלי: python build_potential_wins.py --input data/Lotto.csv --output data/Potential_Wins.csv
"""
from __future__ import annotations

import argparse
import csv
from itertools import combinations
from pathlib import Path

import pandas as pd


def load_history(file_path: str | Path):
    df = pd.read_csv(file_path)
    history_list = []
    for row in df.iloc[:, 2:8].values:
        try:
            history_list.append(set(map(int, row)))
        except (TypeError, ValueError):
            continue
    return history_list


def is_unlikely(combo):
    s_combo = sorted(combo)
    for i in range(len(s_combo) - 3):
        if (
            s_combo[i] + 1 == s_combo[i + 1]
            and s_combo[i + 1] + 1 == s_combo[i + 2]
            and s_combo[i + 2] + 1 == s_combo[i + 3]
        ):
            return True
    lows = [n for n in combo if n <= 18]
    highs = [n for n in combo if n > 18]
    if len(lows) == 0 or len(highs) == 0:
        return True
    return False


def build_filtered_database(input_csv: str | Path, output_filename: str | Path) -> None:
    history = load_history(input_csv)
    last_100 = history[:100]
    total_nums = 37
    select = 6

    print(f"מתחיל לייצר את קובץ האפשרויות: {output_filename}")

    with open(output_filename, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Num1", "Num2", "Num3", "Num4", "Num5", "Num6"])

        found_count = 0
        total_scanned = 0

        for combo in combinations(range(1, total_nums + 1), select):
            total_scanned += 1
            combo_set = set(combo)

            if is_unlikely(combo):
                continue

            is_valid = True
            for h in history:
                if len(combo_set.intersection(h)) >= 5:
                    is_valid = False
                    break
            if not is_valid:
                continue

            for h in last_100:
                if len(combo_set.intersection(h)) >= 4:
                    is_valid = False
                    break
            if not is_valid:
                continue

            writer.writerow(sorted(list(combo)))
            found_count += 1

            if total_scanned % 100000 == 0:
                print(f"נסרקו {total_scanned:,} צירופים... נמצאו {found_count:,} תקינים.")

    print(f"הסתיים! הקובץ {output_filename} מוכן עם {found_count:,} צירופים.")


def main():
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Build Potential_Wins.csv from Lotto history")
    parser.add_argument(
        "--input",
        type=Path,
        default=base / "data" / "Lotto.csv",
        help="Path to Lotto.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=base / "data" / "Potential_Wins.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    build_filtered_database(args.input, args.output)


if __name__ == "__main__":
    main()
