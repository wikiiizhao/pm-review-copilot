# PM Review Copilot

언어: [中文](../README.md) | [English](README.en.md) | [日本語](README.ja.md) | 한국어

PM Review Copilot은 제품 관리자를 위한, Agent 워크플로에서 사용할 수 있는 프로젝트 메모리 및 리뷰 skill 모음입니다.

프로젝트 memory를 로컬에 지속적으로 저장하고, Agent가 생성한 긴 문서, 여러 차례의 수정본, 라벨링 결과를 구조적으로 검토해 여러 프로젝트와 협업 라운드에서 근거 부족, memory 충돌, 환각 위험, 사람이 확인해야 할 지점을 더 빨리 찾을 수 있게 돕습니다.

이 저장소에는 영어 버전과 중국어 버전의 skill이 포함되어 있습니다.

- `skills/pm-review-copilot`: 영어 skill이며 출력도 영어입니다.
- `skills/pm-review-copilot-zh`: 중국어 skill이며 출력도 중국어입니다.

## Agent 발전 흐름

핵심 판단: Agent의 “산출 능력”은 빠르게 강해지고 있지만, 고품질 작업의 병목은 점점 사람의 검토, 확인, 기억 관리로 이동하고 있습니다.

| 흐름 | 대표 관점 | PM 워크플로에 미치는 영향 |
| --- | --- | --- |
| Agent는 “질문에 답하는 도구”에서 “작업을 수행하는 주체”로 이동하고 있습니다 | OpenAI는 ChatGPT agent를 소개하면서 Agent가 가상 컴퓨터를 사용하고, 추론과 행동을 오가며, 엔드투엔드 복잡한 워크플로를 수행할 수 있다고 설명했습니다. 동시에 중요한 행동에는 사용자 확인이 필요하고, 사용자가 언제든 개입할 수 있으며, Agent가 여전히 실수할 수 있다는 점도 강조했습니다. 참고: [Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/). | Agent는 더 많은 PRD, 전략안, 분석 결과, 작업 산출물을 만들게 됩니다. 사람의 검토 대상은 “몇 문단의 답변”에서 “완성된 산출물 전체”로 넓어집니다. |
| 기업은 사람과 Agent의 혼합 팀을 전제로 보기 시작했습니다 | Microsoft 2025 Work Trend Index는 조직이 사람과 Agent로 구성된 “하이브리드 팀”으로 이동하고, Agent가 더 많은 업무 프로세스를 맡으며, 사람은 방향 설정, 예외 처리, 높은 판단력이 필요한 결정을 맡게 된다고 설명합니다. 또한 Agent의 양과 사람의 감독 역량 사이의 균형이 무너지면 비즈니스 위험과 직원 과부하가 생길 수 있다고 경고합니다. 참고: [2025: The year the Frontier Firm is born](https://www.microsoft.com/en-us/worklab/work-trend-index/2025-the-year-the-frontier-firm-is-born). | 사람의 역할은 모든 문장을 직접 쓰는 사람보다 리뷰어, 의사결정자, 컨텍스트 관리자에 가까워집니다. |
| Agent 협업에는 새로운 관리 방식이 필요합니다 | Microsoft 보고서에서 Harvard Business School 교수 Karim R. Lakhani는 기업에 HR이나 IT와 비슷한 Intelligence Resources 기능이 생겨 사람과 AI Agent의 협업 관계를 관리할 수 있다고 말합니다. | Agent 워크플로에는 단일 채팅 스레드에만 의존하지 않고, 저장하고, 인수인계하고, 검토할 수 있는 프로젝트 memory가 필요합니다. |
| 효과적인 Agent는 디버깅 가능하고 조합 가능해야 합니다 | Anthropic은 Agent를 “LLM이 프로세스와 도구 사용 방식을 동적으로 결정하는 시스템”으로 설명하며, 복잡한 프레임워크를 계속 쌓기보다 단순하고 조합 가능하며 디버깅하기 쉬운 패턴에서 시작하라고 권장합니다. 참고: [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents). | PM을 위한 Agent 도구도 리뷰 흐름을 memory, 근거, 충돌, 변경점, 사람의 확인 지점으로 나누어 다룰 필요가 있습니다. |

따라서 PM Review Copilot이 집중하는 것은 “Agent가 더 많은 내용을 생성하게 하는 것”이 아니라, Agent 워크플로의 다음 병목을 해결하는 것입니다.

- 프로젝트 컨텍스트를 채팅 기록에 흩어두지 않고 로컬에 지속적으로 저장합니다.
- 긴 문서 검토를 처음부터 끝까지 읽는 방식에서 위험 우선 검토로 바꿉니다.
- 여러 차례 수정 중 발생하는 사실의 흔들림, 제약 삭제, 지표 정의 변경을 더 쉽게 발견합니다.
- 라벨링 일관성 문제를 전적으로 수작업으로 찾는 대신, 샘플링하고 우선순위를 정하고 위치를 찾기 쉽게 만듭니다.

## 이 skill을 만든 이유

제품 관리자로서 저는 일상 업무에서 Agent 제품을 사용해 PRD, 전략안, 라벨링 데이터, 데이터 인사이트 문서를 만듭니다. 사용하면서 느낀 점은, 정말 시간이 드는 일은 Agent에게 무언가를 쓰게 하는 것이 아니라는 것입니다. 어떤 내용을 신뢰할 수 있는지, 어디에 사람의 확인이 필요한지, 어떤 변경이 의사결정에 영향을 주는지, 그리고 여러 프로젝트와 대화 사이에서 안정적인 컨텍스트를 어떻게 유지할지 계속 판단해야 합니다.

자주 겪는 문제는 다음과 같습니다.

- PRD, 전략안, 분석 보고서는 길어지기 쉽습니다. 여러 번 수정하다 보면 모델이 가설을 사실처럼 쓰거나, 근거가 부족한데도 그럴듯한 결론을 만들 수 있습니다.
- Agent 응답이 길어질수록 사람이 문단별로 검토하는 부담이 커집니다. 하루 종일 일한 뒤에는 중요한 위험을 놓치기도 쉽습니다.
- 프로젝트가 많으면 대화가 프로젝트별로 나뉘는 경우가 많습니다. 프로젝트가 서로 겹칠 때 Agent는 과거 memory, 기존 제약, 이미 확인된 의사결정을 대화 간에 재사용하기 어렵습니다.
- 초안을 반복 수정하는 과정에서 기존 제약, 위험, 열린 질문, 출시 기준이 조용히 삭제되거나 다시 쓰일 수 있습니다.
- 지표, 실험 결론, 데이터 인사이트에 분모, 시간 범위, 출처, 정의 설명이 빠질 수 있습니다.
- “TBD”, “확인 필요”, “가능성 있음” 같은 불확실한 정보가 이후 버전에서 확정 사실처럼 바뀔 수 있습니다.
- 모델의 여러 차례 라벨링 결과가 일관되지 않을 수 있습니다. 데이터가 많아지면 사람이 우선 검토해야 할 불일치 샘플과 라벨 경계를 빠르게 찾기 어렵습니다.

PM Review Copilot의 목표는 Agent 워크플로에서 “사람의 검토 효율이 낮다”는 병목을 엔지니어링 방식으로 해결하는 것입니다. 안정적인 컨텍스트를 기록하고, 가설을 분리하고, 충돌과 위험을 드러내고, 사람의 의사결정을 축적해 정말 검토할 가치가 있는 부분에 주의를 먼저 쓸 수 있게 합니다.

## 핵심 기능

| 기능 | 설명 |
| --- | --- |
| 프로젝트 memory 초기화 | `project-memory/`를 만들고 현재 사실, 의사결정, 근거, 가설, 리뷰 로그, 라벨링 리뷰, 사용자 선호, 인수인계 기록을 저장합니다. |
| memory 생애주기 관리 | memory를 `pinned`, `active`, `background`, `archived`, `superseded`, `deprecated`, `needs_review` 상태로 관리해 오래된 내용이 기본적으로 Agent 컨텍스트를 차지하지 않게 합니다. |
| 영어/중국어 버전 | 영어 워크플로에는 영어 버전, 중국어 PM 워크플로에는 중국어 버전을 사용할 수 있으며, 중국어 버전은 기본적으로 중국어 템플릿과 보고서를 출력합니다. |
| 리뷰 결론 시각화 | 리뷰 결과 상단에 🟢🟡🔴 를 사용해 통과 여부와 사람의 검토 부담을 보여줍니다. |
| 제품 전략 리뷰 | 사실, 지표, 인과관계, 의사결정, 가설, 제안에 근거가 있는지 또는 프로젝트 memory와 충돌하는지 확인합니다. |
| 버전 차이 리뷰 | 기존 PRD/전략 초안과 새 초안을 비교해 새 주장, 삭제된 제약, 지표 정의 변경, 출시 기준 변경을 강조합니다. |
| 라벨링 일관성 리뷰 | 여러 차례의 모델 라벨링이나 여러 사람의 라벨링 결과를 검토해 고위험 불일치 샘플과 라벨 경계 문제를 찾습니다. |
| 수동 memory 업데이트 | 사용자가 명시적으로 요청할 때만 새 사실, 근거, 의사결정, 가설, 인수인계 정보를 해당 memory 파일에 기록합니다. |
| 사용자 선호 기록 | 초기화할 때 언어, 출력 길이, 리뷰 스타일, 의사결정 지원 방식에 대한 선호를 기록할 수 있습니다. |

## 설치

Agent 제품마다 skills, 프로젝트 지시문, 지식 베이스, 로컬 스크립트를 불러오는 방식이 다릅니다. 이 저장소의 핵심은 재사용 가능한 skill 디렉터리이며, 사용자 정의 지시문, skills, 프로젝트 지식을 지원하는 Agent 워크플로라면 연결할 수 있습니다.

### 일반 방식

필요한 skill 디렉터리를 선택합니다.

- 중국어 워크플로: `skills/pm-review-copilot-zh`
- 영어 워크플로: `skills/pm-review-copilot`

사용 중인 Agent 제품에 맞게 해당 디렉터리의 `SKILL.md`를 skill 또는 프로젝트 지시문으로 불러오세요. 같은 디렉터리의 `scripts/`와 `references/`도 유지해 Agent가 설명을 읽고, 로컬 스크립트를 호출하고, 템플릿을 참조할 수 있게 합니다.

### Codex 예시

Codex를 사용하는 경우 필요한 skill 디렉터리를 로컬 Codex skills 디렉터리로 복사합니다.

```bash
# 중국어 버전
cp -R skills/pm-review-copilot-zh ~/.codex/skills/

# 영어 버전
cp -R skills/pm-review-copilot ~/.codex/skills/
```

Codex에 설치한 뒤에는 다음처럼 호출할 수 있습니다.

```text
Use $pm-review-copilot to initialize project-memory for this project.
```

```text
使用 $pm-review-copilot-zh 初始化这个项目的 PM memory。
```

## 빠른 시작

### 1. 프로젝트 memory 초기화

영어:

```text
Use $pm-review-copilot to initialize project-memory for this project and ask only the necessary preference questions.
```

중국어:

```text
使用 $pm-review-copilot-zh 为这个项目初始化 project-memory，并询问我必要的偏好设置。
```

스크립트를 직접 실행할 수도 있습니다.

```bash
python3 skills/pm-review-copilot/scripts/init_pm_memory.py --path . --project-name "My Project"
```

### 2. PRD 또는 전략 문서 리뷰

```text
Use $pm-review-copilot to review this PRD. Focus on unsupported assertions, metric-definition issues, conflicts with project-memory, and items that require my confirmation.
```

출력에는 다음이 포함됩니다.

- 상단의 시각적 결론. 예: `🟡 Verdict: needs local confirmation · Human review load: 🟡 medium`
- 반드시 확인해야 할 항목
- 제품 전략 리뷰
- memory 충돌
- 이전 버전과의 변화
- 무시해도 되는 내용

### 3. memory 수동 업데이트

```text
Use $pm-review-copilot to update project-memory with today's new decisions, evidence, and open questions.
```

이 skill은 자동으로 실행되지 않으며 백그라운드에서 동기화되지 않습니다. 사용자가 명시적으로 요청할 때만 memory를 업데이트합니다.

### 4. 라벨링 일관성 리뷰

```bash
python3 skills/pm-review-copilot/scripts/label_consistency_audit.py labels.csv \
  --id-column id \
  --label-columns label_run_1,label_run_2,label_run_3 \
  --output label_audit.md
```

## 디렉터리 구조

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

## 설계 원칙

- 넓게 수집하고, 선별해 축적하며, 예외를 검토합니다.
- 장기적으로 유지해야 할 사실은 채팅 memory에 의존하지 않고 파일에 저장합니다.
- 근거, 출처, 사용자 의사결정이 없으면 가설을 사실로 승격하지 않습니다.
- 리뷰 보고서는 Agent가 얼마나 많은 일을 했는지 보여주기보다 사람의 주의를 돕도록 최적화합니다.
- 이것은 수동으로 호출하는 skill이며, 자동 리뷰나 백그라운드 동기화 시스템이 아님을 명확히 합니다.

## 라이선스

이 저장소는 MIT License를 사용합니다. 설계 출처는 각 skill의 `references/source-attribution.md`를 참고하세요.
