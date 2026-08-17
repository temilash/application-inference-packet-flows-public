# Packet Application Inference Challenge Dataset

日本語は下にあります。

## Tasks

This release contains two scored tasks.

| Task | Directory | Goal | Score |
|---|---|---|---:|
| Task 1 | `task1_static/` | Classify each application flow using full-flow statistical features | 50 |
| Task 2 | `task2_realtime_prefix5/` | Classify each application flow using only features from the first 5 packets | 50 |

The total score is 100 points. Both tasks use the same target application labels.

## Files in Each Task Directory

- `train_features.csv`: public training features
- `train_labels.csv`: public training labels
- `validation_features.csv`: public validation features
- `validation_labels.csv`: public validation labels
- `test_features.csv`: private-evaluation features
- `sample_submission.csv`: submission template
- `metadata.json`: dataset details

Test labels are not included in this release. They are held by the organizers for final scoring.

## Important Constraint

For Task 2, participants must use only `task2_realtime_prefix5/` files. Using full-flow features from Task 1 to generate Task 2 predictions is not allowed.

Participants must submit their prediction CSV files, source code, and a short technical report. The source code is checked to confirm that private labels and disallowed features are not used.

---

# パケットアプリケーション推定課題データセット

## タスク

このリリースには、採点対象のタスクが2つ含まれています。

| タスク | ディレクトリ | 目的 | 点数 |
|---|---|---|---:|
| タスク1 | `task1_static/` | フロー全体の統計特徴量を用いてアプリケーションを分類する | 50 |
| タスク2 | `task2_realtime_prefix5/` | 最初の5パケットから作った特徴量だけを用いてアプリケーションを分類する | 50 |

総合スコアは100点です。どちらのタスクも対象アプリケーションラベルは同じです。

## 各タスクディレクトリのファイル

- `train_features.csv`: 公開学習用特徴量
- `train_labels.csv`: 公開学習用ラベル
- `validation_features.csv`: 公開検証用特徴量
- `validation_labels.csv`: 公開検証用ラベル
- `test_features.csv`: 最終評価用特徴量
- `sample_submission.csv`: 提出テンプレート
- `metadata.json`: データセットの詳細

testラベルはこのリリースには含まれません。最終採点用として主催者が保持します。

## 重要な制約

タスク2では、`task2_realtime_prefix5/` に含まれるファイルだけを使用してください。タスク1のフロー全体特徴量を使ってタスク2の予測を作ることは禁止します。

参加者は、予測CSV、ソースコード、簡単な説明資料を提出します。主催者は、非公開ラベルや禁止された特徴量を使っていないかを提出コードで確認します。
