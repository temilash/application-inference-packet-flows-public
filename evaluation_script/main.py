import csv
import io
import json
import zipfile


TASKS = ("task1_static", "task2_realtime_prefix5")
ALLOWED_LABELS = {"facebook", "google", "instagram", "mozilla", "x", "youtube"}


def _load_annotations(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if "tasks" not in data:
        raise ValueError("Annotation file must contain a 'tasks' object.")
    return data["tasks"]


def _read_csv_predictions(text):
    rows = {}
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames != ["flow_id", "app"]:
        raise ValueError("CSV submissions must have exactly two columns: flow_id,app")
    for row in reader:
        flow_id = row["flow_id"].strip()
        app = row["app"].strip()
        if flow_id:
            rows[flow_id] = app
    return rows


def _load_submission(path):
    with open(path, "rb") as f:
        raw = f.read()

    if zipfile.is_zipfile(io.BytesIO(raw)):
        predictions = {}
        with zipfile.ZipFile(io.BytesIO(raw)) as zf:
            names = set(zf.namelist())
            for task in TASKS:
                csv_name = f"{task}.csv"
                if csv_name not in names:
                    raise ValueError(f"ZIP submission must contain {csv_name}.")
                text = zf.read(csv_name).decode("utf-8-sig")
                predictions[task] = _read_csv_predictions(text)
        return predictions

    text = raw.decode("utf-8-sig")
    if text.lstrip().startswith("{"):
        data = json.loads(text)
        return {
            task: {str(flow_id): str(app).strip() for flow_id, app in data.get(task, {}).items()}
            for task in TASKS
        }

    raise ValueError(
        "Submission must be either a JSON file with task1_static and "
        "task2_realtime_prefix5 objects, or a ZIP containing task1_static.csv "
        "and task2_realtime_prefix5.csv."
    )


def _macro_f1(y_true, y_pred):
    classes = sorted(set(y_true) | set(y_pred))
    if not classes:
        return 0.0
    scores = []
    for label in classes:
        tp = sum(1 for truth, pred in zip(y_true, y_pred) if truth == label and pred == label)
        fp = sum(1 for truth, pred in zip(y_true, y_pred) if truth != label and pred == label)
        fn = sum(1 for truth, pred in zip(y_true, y_pred) if truth == label and pred != label)
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        scores.append(2 * precision * recall / (precision + recall) if precision + recall else 0.0)
    return sum(scores) / len(scores)


def _score_task(task_name, truth, predictions):
    missing = sorted(set(truth) - set(predictions))
    extra = sorted(set(predictions) - set(truth))
    if missing:
        raise ValueError(f"{task_name}: missing predictions for {len(missing)} flow_id values.")
    if extra:
        raise ValueError(f"{task_name}: submission contains {len(extra)} unknown flow_id values.")

    invalid_labels = sorted({label for label in predictions.values() if label not in ALLOWED_LABELS})
    if invalid_labels:
        raise ValueError(f"{task_name}: invalid labels: {', '.join(invalid_labels)}")

    ordered_ids = sorted(truth)
    y_true = [truth[flow_id] for flow_id in ordered_ids]
    y_pred = [predictions[flow_id] for flow_id in ordered_ids]
    accuracy = sum(1 for truth_label, pred_label in zip(y_true, y_pred) if truth_label == pred_label) / len(y_true)
    macro_f1 = _macro_f1(y_true, y_pred)
    return {
        "accuracy": round(accuracy, 6),
        "macro_f1": round(macro_f1, 6),
        "score": round(50.0 * macro_f1, 6),
    }


def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    annotations = _load_annotations(test_annotation_file)
    submission = _load_submission(user_submission_file)

    task_results = {}
    total = 0.0
    for task in TASKS:
        if task not in annotations:
            raise ValueError(f"Annotation file is missing task '{task}'.")
        if task not in submission:
            raise ValueError(f"Submission is missing task '{task}'.")
        task_results[task] = _score_task(task, annotations[task], submission[task])
        total += task_results[task]["score"]

    split_name = "validation_split" if phase_codename == "dev" else "test_split"
    metrics = {
        "Task 1 Macro F1": task_results["task1_static"]["macro_f1"],
        "Task 1 Accuracy": task_results["task1_static"]["accuracy"],
        "Task 1 Score": task_results["task1_static"]["score"],
        "Task 2 Macro F1": task_results["task2_realtime_prefix5"]["macro_f1"],
        "Task 2 Accuracy": task_results["task2_realtime_prefix5"]["accuracy"],
        "Task 2 Score": task_results["task2_realtime_prefix5"]["score"],
        "Total": round(total, 6),
    }
    return {
        "result": [{split_name: metrics}],
        "submission_result": metrics,
    }
