# Application Inference from Packet Flows

Participant-facing repository for the ITU AI/ML Challenge "Application Inference from Packet Flows".

The challenge asks participants to classify mobile application flows using header-derived traffic statistics extracted from encrypted packet traces. The dataset excludes IP addresses, DNS query names, TLS SNI, HTTP Host values, URLs, domain strings, and payload contents.

## Contents

- `dataset/`: participant-facing train, validation, and final-test feature files for both tasks.
- `dataset/task1_static/`: full-flow static application inference task.
- `dataset/task2_realtime_prefix5/`: real-time inference task using first-5-packet features.
- `evaluation_script/main.py`: scoring logic used by the platform.
- `submission.json`: example JSON submission.
- `templates/`: challenge page text.

Final test labels are held only by the organizers and are not included in this repository.

## Submission Format

The recommended submission is a JSON file with two top-level objects:

```json
{
  "task1_static": {
    "flow_000007": "google"
  },
  "task2_realtime_prefix5": {
    "flow_000007": "google"
  }
}
```

The evaluation script also accepts a ZIP file containing:

```text
task1_static.csv
task2_realtime_prefix5.csv
```

Each CSV must have exactly:

```csv
flow_id,app
flow_000007,google
```

Allowed labels are `facebook`, `google`, `instagram`, `mozilla`, `x`, and `youtube`.

## Evaluation

Each task is evaluated with macro F1 and accuracy. The official score is:

```text
Task 1 Score = 50 * macro_f1(task1_static)
Task 2 Score = 50 * macro_f1(task2_realtime_prefix5)
Total Score  = Task 1 Score + Task 2 Score
```

The leaderboard is ordered by `Total`.
