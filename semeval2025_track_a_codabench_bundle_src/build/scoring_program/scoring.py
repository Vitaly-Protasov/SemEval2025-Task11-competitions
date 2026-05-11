#!/usr/bin/env python3
import csv
import html
import json
import sys
import traceback
from pathlib import Path


SUPPORTED_LANGUAGES = [
    "afr", "arq", "ary", "chn", "deu", "eng", "esp", "hau", "hin", "ibo",
    "ind", "jav", "kin", "mar", "pcm", "ptbr", "ptmz", "ron", "rus", "sun",
    "swa", "swe", "tat", "ukr", "vmw", "xho", "yor", "zul",
]

LANGUAGE_NAMES = {
    "afr": "Afrikaans",
    "arq": "Algerian Arabic",
    "ary": "Moroccan Arabic",
    "chn": "Mandarin Chinese",
    "deu": "German",
    "eng": "English",
    "esp": "Spanish (Latin American)",
    "hau": "Hausa",
    "hin": "Hindi",
    "ibo": "Igbo",
    "ind": "Indonesian",
    "jav": "Javanese",
    "kin": "Kinyarwanda",
    "mar": "Marathi",
    "pcm": "Nigerian Pidgin",
    "ptbr": "Portuguese (Brazilian)",
    "ptmz": "Portuguese (Mozambican)",
    "ron": "Romanian",
    "rus": "Russian",
    "sun": "Sundanese",
    "swa": "Swahili",
    "swe": "Swedish",
    "tat": "Tatar",
    "ukr": "Ukrainian",
    "vmw": "Emakhuwa",
    "xho": "isiXhosa",
    "yor": "Yoruba",
    "zul": "isiZulu",
}


def normalize_header(fieldnames):
    return [name.strip().lower() for name in fieldnames]


def empty_scores():
    return {
        "avg_macro_f1": 0.0,
        "avg_micro_f1": 0.0,
        "languages_scored": 0,
    }


def write_outputs(output_dir, scores, html_body):
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "scores.json").write_text(json.dumps(scores, indent=2), encoding="utf-8")
    (output_dir / "detailed_results.html").write_text(html_body, encoding="utf-8")


def fail(output_dir, message):
    write_outputs(
        output_dir,
        empty_scores(),
        f"<h2>Submission failed validation</h2><pre>{html.escape(message)}</pre>",
    )
    print(message)
    sys.exit(0)


def read_csv_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_csv_header(path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return next(csv.reader(handle))


def locate_reference_root(input_dir):
    preferred = input_dir / "ref"
    return preferred if preferred.is_dir() else input_dir


def find_reference_files(input_dir):
    reference_root = locate_reference_root(input_dir)
    refs = {}
    for path in sorted(reference_root.rglob("*.csv")):
        if "__MACOSX" in path.parts or path.name.startswith("._"):
            continue
        header = normalize_header(read_csv_header(path))
        if not header or header[0] != "id" or "text" in header:
            continue
        if path.stem in SUPPORTED_LANGUAGES:
            refs[path.stem] = path
    return refs


def find_prediction_files(input_dir):
    prediction_root = input_dir / "res" if (input_dir / "res").is_dir() else input_dir
    preds = {}
    for path in sorted(prediction_root.rglob("pred_*.csv")):
        if "__MACOSX" in path.parts or path.name.startswith("._"):
            continue
        language = path.stem.replace("pred_", "", 1)
        preds[language] = path
    return preds


def parse_binary(value, path, row_id, label):
    value = str(value).strip()
    if value not in {"0", "1"}:
        raise ValueError(
            f"{path.name}: id={row_id} has invalid value for {label}: {value!r}; expected 0 or 1."
        )
    return int(value)


def f1_score_from_counts(tp, fp, fn):
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return 2 * precision * recall / (precision + recall) if precision + recall else 0.0


def display_language(language):
    return LANGUAGE_NAMES.get(language, language.upper())


def display_label(label):
    return label.replace("_", " ").title()


def evaluate_language(language, gold_path, pred_path):
    gold_header = read_csv_header(gold_path)
    pred_header = read_csv_header(pred_path)
    if normalize_header(gold_header) != normalize_header(pred_header):
        raise ValueError(
            f"{pred_path.name}: invalid header {pred_header}. Expected {gold_header}."
        )

    gold_rows = read_csv_rows(gold_path)
    pred_rows = read_csv_rows(pred_path)
    if len(gold_rows) != len(pred_rows):
        gold_example = gold_rows[0]["id"] if gold_rows else ""
        pred_example = pred_rows[0]["id"] if pred_rows else ""
        hint = ""
        if "_test_" in gold_example and "_dev_" in pred_example:
            hint = (
                " This looks like a dev-vs-test mismatch: the submission uses dev IDs "
                f"(for example {pred_example}) but the evaluation expects test IDs "
                f"(for example {gold_example})."
            )
        raise ValueError(
            f"{pred_path.name}: expected {len(gold_rows)} rows, received {len(pred_rows)} rows.{hint}"
        )

    labels = gold_header[1:]
    gold_by_id = {row["id"]: row for row in gold_rows}
    pred_by_id = {}
    for row in pred_rows:
        row_id = row.get("id", "").strip()
        if not row_id:
            raise ValueError(f"{pred_path.name}: empty id detected.")
        if row_id in pred_by_id:
            raise ValueError(f"{pred_path.name}: duplicate id {row_id}.")
        pred_by_id[row_id] = row

    missing_ids = sorted(set(gold_by_id) - set(pred_by_id))
    extra_ids = sorted(set(pred_by_id) - set(gold_by_id))
    if missing_ids:
        raise ValueError(f"{pred_path.name}: missing ids, first examples: {missing_ids[:5]}.")
    if extra_ids:
        raise ValueError(f"{pred_path.name}: unexpected ids, first examples: {extra_ids[:5]}.")

    per_label = {label: {"tp": 0, "fp": 0, "fn": 0} for label in labels}
    micro = {"tp": 0, "fp": 0, "fn": 0}

    for row_id, gold_row in gold_by_id.items():
        pred_row = pred_by_id[row_id]
        for label in labels:
            gold = parse_binary(gold_row[label], gold_path, row_id, label)
            pred = parse_binary(pred_row[label], pred_path, row_id, label)
            if gold == 1 and pred == 1:
                per_label[label]["tp"] += 1
                micro["tp"] += 1
            elif gold == 0 and pred == 1:
                per_label[label]["fp"] += 1
                micro["fp"] += 1
            elif gold == 1 and pred == 0:
                per_label[label]["fn"] += 1
                micro["fn"] += 1

    label_f1 = {
        label: f1_score_from_counts(counts["tp"], counts["fp"], counts["fn"])
        for label, counts in per_label.items()
    }
    macro_f1 = sum(label_f1.values()) / len(label_f1) if label_f1 else 0.0
    micro_f1 = f1_score_from_counts(micro["tp"], micro["fp"], micro["fn"])
    return {
        "language": language,
        "rows": len(gold_rows),
        "labels": labels,
        "macro_f1": macro_f1,
        "micro_f1": micro_f1,
        "label_f1": label_f1,
    }


def render_details(results, missing_languages):
    cards = []
    for item in results:
        metric_rows = []
        label_items = list(item["label_f1"].items())
        total_rows = len(label_items) + 1

        for index, (label, score) in enumerate(label_items):
            language_cell = ""
            if index == 0:
                language_cell = (
                    f"<td class='language-name' rowspan='{total_rows}'>"
                    f"<div class='language-title'>{html.escape(display_language(item['language']))}</div>"
                    f"<div class='language-meta'>Rows: {item['rows']}</div>"
                    f"<div class='language-meta'>Micro-F1: {item['micro_f1']:.6f}</div>"
                    "</td>"
                )

            metric_rows.append(
                "<tr>"
                f"{language_cell}"
                f"<td class='metric-name'>{html.escape(display_label(label))}</td>"
                f"<td class='metric-score'>{score:.6f}</td>"
                "</tr>"
            )

        metric_rows.append(
            "<tr class='summary-row'>"
            "<td class='metric-name'><strong>Average Macro-F1</strong></td>"
            f"<td class='metric-score'><strong>{item['macro_f1']:.6f}</strong></td>"
            "</tr>"
        )

        cards.append(
            "<table class='language-table'>"
            "<tbody>"
            + "".join(metric_rows) +
            "</tbody></table>"
        )

    missing_html = ""
    if missing_languages:
        missing_html = (
            "<p class='missing-languages'>Languages not included in this submission: "
            f"{html.escape(', '.join(display_language(language) for language in missing_languages))}. "
            "Those language-specific leaderboard columns will remain empty for this submission.</p>"
        )

    return (
        "<style>"
        "body { font-family: Georgia, 'Times New Roman', serif; margin: 16px; color: #111; }"
        "h2 { margin: 0 0 12px 0; font-family: Arial, sans-serif; }"
        "p { margin: 0 0 10px 0; font-family: Arial, sans-serif; font-size: 14px; }"
        ".visualization-wrap { max-width: 980px; }"
        ".language-table { width: 100%; border-collapse: collapse; margin: 0 0 10px 0; }"
        ".language-table td { border: 2px solid #7f7f7f; padding: 6px 8px; vertical-align: middle; }"
        ".language-name { width: 38%; min-width: 220px; }"
        ".language-title { font-size: 26px; line-height: 1.1; }"
        ".language-meta { margin-top: 8px; font-family: Arial, sans-serif; font-size: 13px; color: #444; }"
        ".metric-name { width: 38%; font-size: 22px; line-height: 1.1; }"
        ".metric-score { width: 14%; font-size: 22px; text-align: left; }"
        ".summary-row td { font-weight: 700; }"
        ".missing-languages { margin-top: 16px; }"
        "</style>"
        "<div class='visualization-wrap'>"
        "<h2>SemEval 2025 Task 11 Track A Results</h2>"
        "<p>This scorer accepts one or more language prediction files named "
        "<code>pred_&lt;lang&gt;.csv</code> inside a <code>track_a</code> folder or anywhere inside the zip.</p>"
        "<p><strong>Leaderboard averages are computed over all supported test languages.</strong> "
        "Languages omitted from the submission contribute 0.0 to the overall averages.</p>"
        + "".join(cards) +
        f"{missing_html}"
        "</div>"
    )


def main():
    input_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/app/input")
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("/app/output")

    try:
        refs = find_reference_files(input_dir)
        preds = find_prediction_files(input_dir)

        if not refs:
            fail(output_dir, f"No reference CSV files found under {input_dir}.")
        if not preds:
            fail(output_dir, f"No prediction files named pred_<lang>.csv found under {input_dir}.")

        unsupported = sorted(language for language in preds if language not in refs)
        if unsupported:
            fail(output_dir, f"Unsupported prediction files for languages: {', '.join(unsupported)}")

        results = []
        for language in sorted(preds):
            results.append(evaluate_language(language, refs[language], preds[language]))

        scores = empty_scores()
        scores["languages_scored"] = len(results)

        total_languages = len(SUPPORTED_LANGUAGES)
        if total_languages:
            scores["avg_macro_f1"] = round(
                sum(item["macro_f1"] for item in results) / total_languages, 6
            )
            scores["avg_micro_f1"] = round(
                sum(item["micro_f1"] for item in results) / total_languages, 6
            )

        for item in results:
            scores[f"{item['language']}_macro_f1"] = round(item["macro_f1"], 6)

        submitted_languages = {item["language"] for item in results}
        missing_languages = [language for language in SUPPORTED_LANGUAGES if language not in submitted_languages]

        write_outputs(output_dir, scores, render_details(results, missing_languages))
        print(json.dumps(scores, indent=2))
    except ValueError as exc:
        fail(output_dir, str(exc))
    except Exception:
        fail(output_dir, traceback.format_exc())


if __name__ == "__main__":
    main()
