# PM Review Copilot

言語： [中文](../README.md) | [English](README.en.md) | 日本語 | [한국어](README.ko.md)

PM Review Copilot は、プロダクトマネージャー向けに設計された、Agent ワークフローで使えるプロジェクトメモリとレビューのための skill セットです。

ローカルにプロジェクト memory を永続化し、Agent が生成した長いドキュメント、複数回の改訂、ラベリング結果を構造的にレビューすることで、複数プロジェクト・複数ラウンドの協業において、根拠不足、memory との矛盾、ハルシネーションのリスク、人間が確認すべき箇所をより早く見つけられるようにします。

このリポジトリには英語版と中国語版の skill が含まれています。

- `skills/pm-review-copilot`：英語版 skill。出力も英語です。
- `skills/pm-review-copilot-zh`：中国語版 skill。出力も中国語です。

## Agent の発展トレンド

中心となる見立て：Agent の「成果物を作る力」は急速に高まっています。一方で、高品質なタスク遂行のボトルネックは、人間によるレビュー、確認、記憶管理へと移りつつあります。

| トレンド | 代表的な見解 | PM ワークフローへの影響 |
| --- | --- | --- |
| Agent は「質問に答える存在」から「タスクを実行する存在」へ移行している | OpenAI は ChatGPT agent の発表で、Agent が仮想コンピューターを使い、推論と行動を切り替えながら、エンドツーエンドの複雑なワークフローを完了できると説明しています。同時に、重要な操作ではユーザー確認が必要であり、ユーザーはいつでも介入でき、Agent は依然として誤る可能性があることも強調しています。参考：[Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/)。 | Agent は PRD、戦略案、分析結果、タスク成果物をさらに多く生成します。人間のレビュー対象は「数段落の回答」から「完成物全体」へ広がります。 |
| 企業は人間と Agent の混合チームを前提にし始めている | Microsoft 2025 Work Trend Index は、組織が人間と Agent からなる「ハイブリッドチーム」へ向かい、Agent がより多くの業務プロセスを担い、人間は方向づけ、例外処理、高度な判断を担うようになると述べています。また、Agent の量と人間の監督能力のバランスが崩れると、事業リスクや従業員の過負荷につながるとも指摘しています。参考：[2025: The year the Frontier Firm is born](https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born)。 | 人間の役割は、すべてを一字一句書く人というより、レビュー担当者、意思決定者、コンテキストの管理者に近づきます。 |
| Agent 協業には新しい管理の仕組みが必要になる | Microsoft のレポートでは、Harvard Business School 教授の Karim R. Lakhani が、企業には HR や IT に似た Intelligence Resources 部門が生まれ、人間と AI Agent の協業関係を管理する可能性があると述べています。 | Agent ワークフローには、単一のチャットスレッドに依存するのではなく、蓄積・引き継ぎ・レビューが可能なプロジェクト memory が必要になります。 |
| 有効な Agent はデバッグ可能で組み合わせやすいべき | Anthropic は、Agent を「LLM がプロセスとツール利用を動的に決めるシステム」と定義し、複雑なフレームワークを積み上げるよりも、シンプルで組み合わせやすく、デバッグしやすいパターンから始めることを推奨しています。参考：[Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)。 | PM 向けの Agent ツールでも、レビューの流れを memory、根拠、矛盾、差分、人間の確認点に分けて扱うことが重要になります。 |

つまり、PM Review Copilot が重視しているのは「Agent にもっと多く書かせること」ではなく、Agent ワークフローの次のボトルネックを解くことです。

- プロジェクトのコンテキストをチャット履歴に散らばらせず、ローカルに永続化する。
- 長文ドキュメントのレビューを逐語的な確認から、リスク優先の確認へ変える。
- 複数回の改訂で起きる事実のズレ、制約の削除、指標定義の変更を見つけやすくする。
- ラベリングの一貫性問題を、完全な手作業ではなく、サンプリング・優先順位付け・特定しやすい形にする。

## この skill を作った理由

プロダクトマネージャーとして、日々の仕事で Agent 製品を使い、PRD、戦略案、ラベリングデータ、データインサイトの文書化を支援してもらっています。その中で本当に時間がかかるのは、Agent に何かを書かせることではありません。どの内容を信頼できるのか、どこに人間の確認が必要なのか、どの変更が意思決定に影響するのか、そして複数プロジェクト・複数チャットをまたいで安定したコンテキストをどう保つのかを判断し続けることです。

よくある課題は次のとおりです。

- PRD、戦略案、分析レポートは長くなりがちです。何度も修正するうちに、モデルが仮説を事実のように書いたり、根拠が薄いのにもっともらしい結論を出したりします。
- Agent の回答量が増えるほど、段落ごとに人間がレビューする負荷は高まります。長時間働いた後ほど、重要なリスクを見落としやすくなります。
- プロジェクトが多いと、会話はプロジェクトごとに分かれがちです。プロジェクトが交差すると、Agent は過去の memory、古い制約、確認済みの意思決定を会話横断で再利用しにくくなります。
- 草稿を改訂する過程で、古い制約、リスク、未解決事項、リリース基準が静かに削除・書き換えられることがあります。
- 指標、実験結果、データインサイトに、分母、期間、出典、定義の説明が欠けることがあります。
- 「TBD」「要確認」「可能性がある」といった不確実な情報が、後の版で確定事実のように書き換えられることがあります。
- モデルによる複数回のラベリング結果が一致しないことがあります。データ量が大きいと、人間が優先して確認すべき不一致サンプルやラベル境界をすばやく見つけるのは困難です。

PM Review Copilot の目的は、Agent ワークフローにおける「人間のレビュー効率の低さ」というボトルネックを、エンジニアリング的な方法で解くことです。安定したコンテキストを記録し、仮説を切り分け、矛盾とリスクを目立たせ、人間の意思決定を蓄積し、本当にレビューすべき部分に注意を向けられるようにします。

## 主な機能

| 機能 | 説明 |
| --- | --- |
| プロジェクト memory 初期化 | `project-memory/` を作成し、現在の事実、意思決定、根拠、仮説、レビュー履歴、ラベリングレビュー、ユーザー設定、引き継ぎ情報を保存します。 |
| memory ライフサイクル管理 | memory を `pinned`、`active`、`background`、`archived`、`superseded`、`deprecated`、`needs_review` として扱い、古くなった内容がデフォルトで Agent のコンテキストを消費しないようにします。 |
| 英語版と中国語版 | 英語ワークフローには英語版、中国語 PM ワークフローには中国語版を使えます。中国語版ではテンプレートとレポートがデフォルトで中国語になります。 |
| レビュー結論の可視化 | レビュー結果の冒頭に 🟢🟡🔴 を表示し、通過可否と人間のレビュー負荷を示します。 |
| プロダクト戦略レビュー | 事実、指標、因果、意思決定、仮説、提案に根拠があるか、またはプロジェクト memory と矛盾していないかを確認します。 |
| 版間差分レビュー | 新旧の PRD や戦略草稿を比較し、新しい主張、削除された制約、指標定義の変更、リリース基準の変更を強調します。 |
| ラベリング一貫性レビュー | 複数回のモデルラベリングや複数人のラベリング結果をレビューし、高リスクの不一致サンプルとラベル境界の問題を見つけます。 |
| 手動 memory 更新 | ユーザーが明示的に依頼した場合のみ、新しい事実、根拠、意思決定、仮説、引き継ぎ情報を対応する memory ファイルへ書き込みます。 |
| ユーザー設定の記録 | 初期化時に、言語、出力の長さ、レビュー方針、意思決定支援の好みを記録できます。 |

## インストール

Agent 製品によって、skills、プロジェクト指示、ナレッジベース、ローカルスクリプトの読み込み方は異なります。このリポジトリの中核は再利用可能な skill ディレクトリです。カスタム指示、skills、プロジェクトナレッジを扱える Agent ワークフローであれば接続できます。

### 汎用的な使い方

必要な skill ディレクトリを選びます。

- 中国語ワークフロー：`skills/pm-review-copilot-zh`
- 英語ワークフロー：`skills/pm-review-copilot`

利用している Agent 製品に合わせて、対応する `SKILL.md` を skill またはプロジェクト指示として読み込ませます。同じディレクトリにある `scripts/` と `references/` も保持し、Agent が説明を読み、ローカルスクリプトを呼び出し、テンプレートを参照できるようにしてください。

### Codex の例

Codex を使う場合は、必要な skill ディレクトリをローカルの Codex skills ディレクトリへコピーします。

```bash
# 中国語版
cp -R skills/pm-review-copilot-zh ~/.codex/skills/

# 英語版
cp -R skills/pm-review-copilot ~/.codex/skills/
```

Codex にインストールした後は、次のように呼び出せます。

```text
Use $pm-review-copilot to initialize project-memory for this project.
```

```text
使用 $pm-review-copilot-zh 初始化这个项目的 PM memory。
```

## クイックスタート

### 1. プロジェクト memory を初期化する

英語：

```text
Use $pm-review-copilot to initialize project-memory for this project and ask only the necessary preference questions.
```

中国語：

```text
使用 $pm-review-copilot-zh 为这个项目初始化 project-memory，并询问我必要的偏好设置。
```

スクリプトを直接実行することもできます。

```bash
python3 skills/pm-review-copilot/scripts/init_pm_memory.py --path . --project-name "My Project"
```

### 2. PRD または戦略ドキュメントをレビューする

```text
Use $pm-review-copilot to review this PRD. Focus on unsupported assertions, metric-definition issues, conflicts with project-memory, and items that require my confirmation.
```

出力には次の内容が含まれます。

- 冒頭の視覚的な結論。例：`🟡 Verdict: needs local confirmation · Human review load: 🟡 medium`
- 必ず確認すべき項目
- プロダクト戦略レビュー
- memory との矛盾
- 前版からのズレ
- 無視してよい内容

### 3. memory を手動で更新する

```text
Use $pm-review-copilot to update project-memory with today's new decisions, evidence, and open questions.
```

この skill は自動起動せず、バックグラウンド同期もしません。ユーザーが明示的に依頼した場合にのみ memory を更新します。

### 4. ラベリング一貫性をレビューする

```bash
python3 skills/pm-review-copilot/scripts/label_consistency_audit.py labels.csv \
  --id-column id \
  --label-columns label_run_1,label_run_2,label_run_3 \
  --output label_audit.md
```

## ディレクトリ構成

```text
.
├── skills/
│   ├── pm-review-copilot/
│   └── pm-review-copilot-zh/
├── docs/
│   ├── README.en.md
│   ├── README.ja.md
│   └── README.ko.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## 設計原則

- 広く収集し、厳選して蓄積し、例外をレビューする。
- 長期的な事実はチャット memory に頼らず、ファイルに保存する。
- 根拠、出典、ユーザーの意思決定がない場合、仮説を事実へ昇格させない。
- レビュー報告は、Agent がどれだけ作業したかを示すためではなく、人間の注意力を助けるために最適化する。
- これは手動で呼び出す skill であり、自動レビューやバックグラウンド同期システムではないことを明確にする。

## ライセンス

このリポジトリは MIT License を使用しています。設計上の出典については、各 skill の `references/source-attribution.md` を参照してください。
