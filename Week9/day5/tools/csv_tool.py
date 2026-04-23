import os
import csv
import io


def read_csv_summary(filepath):
    """Read a CSV file and return a text summary of its contents."""
    if not filepath or not os.path.exists(filepath):
        return None

    rows = []
    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for i, row in enumerate(reader):
            rows.append(row)
            if i >= 499:
                break

    if not rows:
        return "CSV file is empty."

    total_rows = len(rows)
    summary_lines = [
        f"File: {os.path.basename(filepath)}",
        f"Rows: {total_rows}",
        f"Columns ({len(headers)}): {', '.join(headers)}",
        "",
        "Sample data (first 5 rows):",
    ]

    for row in rows[:5]:
        summary_lines.append("  " + " | ".join(f"{k}: {v}" for k, v in row.items()))

    # numeric column stats
    numeric_stats = {}
    for col in headers:
        vals = []
        for row in rows:
            try:
                vals.append(float(row[col]))
            except (ValueError, TypeError):
                pass
        if vals:
            numeric_stats[col] = {
                "min": round(min(vals), 2),
                "max": round(max(vals), 2),
                "avg": round(sum(vals) / len(vals), 2),
                "sum": round(sum(vals), 2),
            }

    if numeric_stats:
        summary_lines.append("\nNumeric column stats:")
        for col, stats in numeric_stats.items():
            summary_lines.append(
                f"  {col}: min={stats['min']}, max={stats['max']}, avg={stats['avg']}, sum={stats['sum']}"
            )

    # categorical columns
    cat_stats = {}
    for col in headers:
        if col not in numeric_stats:
            counter = {}
            for row in rows:
                val = row.get(col, "")
                counter[val] = counter.get(val, 0) + 1
            if 1 < len(counter) <= 20:
                cat_stats[col] = sorted(counter.items(), key=lambda x: -x[1])[:5]

    if cat_stats:
        summary_lines.append("\nCategorical column breakdown (top 5):")
        for col, items in cat_stats.items():
            breakdown = ", ".join(f"{v}({c})" for v, c in items)
            summary_lines.append(f"  {col}: {breakdown}")

    return "\n".join(summary_lines)
