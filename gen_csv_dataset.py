import argparse
import csv
from pathlib import Path
import tensorflow_datasets as tfds


def _ensure_parent(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def _to_str(x):
    if isinstance(x, (bytes, bytearray)):
        return x.decode("utf-8", errors="replace")
    return str(x)


def export_ag_news_tsv(
    split: str, out_path: str, limit: int | None = None, delimiter: str = "\t"
) -> int:
    ds = tfds.load("ag_news_subset", split=split)
    out = Path(out_path)
    _ensure_parent(out)

    written = 0
    with out.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter=delimiter)
        w.writerow(["title", "description", "label"])  # header
        for ex in tfds.as_numpy(ds):
            title = _to_str(ex["title"])
            desc = _to_str(ex["description"])
            label = int(ex["label"])
            w.writerow([title, desc, label])
            written += 1
            if limit is not None and written >= limit:
                break
    return written


def main():
    ap = argparse.ArgumentParser(
        description="Export AG News split to TSV (title, description, label)."
    )
    ap.add_argument(
        "--split",
        default="test",
        choices=["train", "test"],
        help="Dataset split to export",
    )
    ap.add_argument("--out", default="data/ag_news_test.csv", help="Output CSV path")
    ap.add_argument(
        "--limit", type=int, default=None, help="Optional cap on number of rows"
    )
    ap.add_argument("--delimiter", default=",", help="Field delimiter (default: COMMA)")
    args = ap.parse_args()

    n = export_ag_news_tsv(args.split, args.out, args.limit, args.delimiter)
    print(f"Wrote {n} rows to {args.out}")


if __name__ == "__main__":
    main()
