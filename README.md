<p align="center">
  <img src="./assets/readme/hero.svg" width="100%" alt="Orca Adaptive Orchestration: a supervised lifecycle connecting Run, Task, Dispatch, Worker, and Quality Gate">
</p>

<p align="center">
  <a href="#中文">中文</a> · <a href="#english">English</a>
</p>

<h1 id="中文">Orca Adaptive Orchestration</h1>

> 面向 Codex 与 Orca 的显式编排 Skill：把复杂目标拆解成可规划、可监督、可验收的多智能体工作流。

它负责协调，而不是简单地“再开几个 Agent”：它记录任务边界、Worker 所有权、模型能力、Worktree/PR 边界，以及每一次执行的证据。

## 它能做什么

- **把目标变成可执行的 Run**：生成 Execution Manifest，明确任务、依赖、并发上限、Runner、Effective Model、Capability Tier、Worktree 和 PR Unit。
- **管理完整生命周期**：使用 Orca Run、Task、Dispatch 和 Worker 关系，等待 `worker_done`、问题、升级与心跳，并在完成后正确释放或复用 Worker。
- **按真实能力路由模型**：区分 Runner（例如 OpenCode）和 Effective Model，再根据任务风险选择 Flash、Pro 或 Strong fallback，而不是从 CLI 名称猜能力。
- **支持安全的强制派发**：通过 `强制派发` / `force-dispatch` 快速进入约束明确的并行工作流，同时保留任务分解、隔离、Quality Gate 和权限边界。
- **用 Quality Gate 验收结果**：Worker 的成功回执只是证据；Skill 会独立检查交付物，并在验证失败时创建有边界的 Repair Task。
- **在失败时保留上下文**：支持 Transfer、Decision Gate、有限重试和 `outcome_unknown` 处理，避免把超时、TUI idle 或 Orca 误报直接当成真实失败。

## 工作方式

<p align="center">
  <img src="./assets/readme/workflow.svg" width="100%" alt="Orca workflow from objective to task, dispatch, worker execution, and evidence-based acceptance">
</p>

1. **Plan** — 读取 Orca、Runner、模型路由、仓库与现有编排状态。
2. **Decompose** — 创建有明确输入、输出、依赖、所有权和验收标准的 Task。
3. **Dispatch** — 通过受监督的 `worker-start` 启动 Worker，并固定生命周期归属。
4. **Supervise** — 以滚动等待处理 Worker 回执、问题、升级和状态消息。
5. **Verify** — 独立执行 Quality Gate；必要时 Repair、Transfer 或暂停到 Decision Gate。

## 快速开始

在 Codex 中加载此 Skill：

```text
$orca-adaptive-orchestrator
```

普通模式会先展示计划并等待确认。需要快速进入受约束的强制编排时，使用精确触发词：

```text
强制派发；max-workers=2；Runner=opencode；model=default：
把这个目标拆成两个可监督的并行任务，并在完成后独立验收。
```

强制派发仍受以下边界约束：最多四个并发 Worker；所有 Task 先创建再启动第一波；远程发布、部署、强制 push、历史重写和破坏性操作不会被隐式授权。

## 四种执行模式

| 模式 | 用途 |
| --- | --- |
| **Default** | 只读调查并展示 Execution Manifest，等待确认 |
| **Plan only** | 只产出计划，不创建 Orca 状态或修改文件 |
| **Direct execution** | 用户明确授权后直接执行 Manifest 中列出的本地效果 |
| **Force dispatch** | 使用显式 Runner/模型约束快速派发，仍保留监督与 Quality Gate |

## 关键设计

### Runner ≠ Effective Model

Runner 是 Worker 使用的 Agent CLI；Effective Model 是经过当前配置与别名解析后真正调用的模型。路由逻辑以 Effective Model 和任务所需的 Capability Tier 为依据，避免把 `opencode`、`claude` 或其他 CLI 名称当成模型能力。

### 监督优先于“看起来完成”

每个 Worker 都必须有受监督的 `worker-start` 回执。`agent_prompt_stalled`、过早 capability 撤销、被拒绝的旧 `worker_done`，或仍有输出的终端，都需要先进入证据检查与 `outcome_unknown` 流程，不能直接重派或释放。

### 结果必须通过 Quality Gate

Worker 的报告不能代替验收。Quality Gate 关注可观察的文件、测试、UI 状态、持久化结果或其他交付证据；验证失败时使用独立 Repair Task，而不是把失败伪装成普通重试。

## 仓库内容

- [`orca-adaptive-orchestrator/SKILL.md`](./orca-adaptive-orchestrator/SKILL.md) — Skill 入口与总体生命周期
- [`references/`](./orca-adaptive-orchestrator/references/) — 分解、Manifest、路由、监督与强制派发规则
- [`scripts/inspect_runtime.py`](./orca-adaptive-orchestrator/scripts/inspect_runtime.py) — 只输出白名单运行时与模型路由信息
- [`docs/orca-adaptive-orchestrator-architecture-zh.html`](./docs/orca-adaptive-orchestrator-architecture-zh.html) — 架构图
- [`docs/orca-adaptive-orchestrator-dataflow-zh.html`](./docs/orca-adaptive-orchestrator-dataflow-zh.html) — 数据流图
- [`docs/adr/0001-route-by-effective-model-and-supervised-lifecycle.md`](./docs/adr/0001-route-by-effective-model-and-supervised-lifecycle.md) — Effective Model 与监督生命周期 ADR

## 验证

```bash
python3 -m unittest discover -s orca-adaptive-orchestrator/tests -v
python3 orca-adaptive-orchestrator/scripts/inspect_runtime.py --pretty
```

---

<h1 id="english">English</h1>

> An explicit orchestration skill for Codex and Orca: turn complex goals into planned, supervised, and verifiable multi-agent workflows.

This project coordinates more than “opening a few agents.” It preserves task boundaries, Worker ownership, model capability, Worktree/PR boundaries, and evidence for every execution attempt.

## What it does

- **Turns goals into executable Runs** — produces an Execution Manifest covering tasks, dependencies, concurrency, Runner, Effective Model, Capability Tier, Worktree, and PR Unit boundaries.
- **Manages the full lifecycle** — connects Orca Run, Task, Dispatch, and Worker state; waits for `worker_done`, questions, escalations, and heartbeats; then reuses or releases Workers correctly.
- **Routes by real capability** — separates the Runner CLI from the Effective Model and selects Flash, Pro, or a strong fallback based on task risk instead of guessing from a CLI name.
- **Supports constrained force dispatch** — uses the exact `强制派发` / `force-dispatch` trigger for fast, explicit parallel coordination while retaining decomposition, isolation, Quality Gates, and authority boundaries.
- **Accepts evidence, not claims** — treats Worker reports as evidence and validates deliverables independently; failed validation becomes a bounded Repair Task.
- **Recovers without losing context** — preserves evidence across Transfers, Decision Gates, bounded retries, and `outcome_unknown` states so timeouts or Orca false positives are not mistaken for real failures.

## How it works

1. **Plan** — inspect Orca, Runner, model routing, repository state, and existing orchestration state.
2. **Decompose** — create Tasks with explicit inputs, outputs, dependencies, ownership, and acceptance criteria.
3. **Dispatch** — start each Worker through supervised `worker-start` and preserve lifecycle authority.
4. **Supervise** — process Worker completion, questions, escalations, and status through rolling waits.
5. **Verify** — apply an independent Quality Gate; repair, transfer, or pause at a Decision Gate when needed.

## Quick start

Load the Skill in Codex:

```text
$orca-adaptive-orchestrator
```

The default mode presents a plan and waits for confirmation. For a constrained fast path, use the exact trigger:

```text
force-dispatch; max-workers=2; Runner=opencode; model=default:
Split this goal into two supervised parallel tasks and independently verify the result.
```

Force dispatch still caps concurrency at four Workers, creates all Tasks before the first wave, and never implicitly authorizes remote publication, deployment, force pushes, history rewrites, or destructive actions.

## Execution modes

| Mode | Use |
| --- | --- |
| **Default** | Read-only investigation plus an Execution Manifest, then confirmation |
| **Plan only** | Produce the plan without creating Orca state or changing files |
| **Direct execution** | Execute the locally authorized effects listed in the Manifest |
| **Force dispatch** | Dispatch with explicit Runner/model constraints while retaining supervision and Quality Gates |

## Design principles

### Runner is not the Effective Model

The Runner is the Agent CLI used by a Worker. The Effective Model is the model resolved through the current configuration and aliases. Routing uses the Effective Model and the required Capability Tier, so `opencode`, `claude`, and other CLI names are never treated as capability identities.

### Supervision beats an early status label

Every Worker needs a supervised `worker-start` receipt. An early `agent_prompt_stalled`, capability revocation, rejected stale `worker_done`, or a terminal that is still producing output enters evidence inspection and `outcome_unknown` handling instead of immediate retry or release.

### Quality Gates define completion

A Worker report does not replace acceptance. Quality Gates inspect observable files, tests, UI state, persistence, or other deliverable evidence. Failed validation creates an independent Repair Task instead of being relabeled as a runtime retry.

## Repository map

- [`orca-adaptive-orchestrator/SKILL.md`](./orca-adaptive-orchestrator/SKILL.md) — entrypoint and lifecycle rules
- [`references/`](./orca-adaptive-orchestrator/references/) — decomposition, Manifest, routing, supervision, and force-dispatch guidance
- [`scripts/inspect_runtime.py`](./orca-adaptive-orchestrator/scripts/inspect_runtime.py) — allow-listed runtime and model-routing inspection
- [`docs/orca-adaptive-orchestrator-architecture-zh.html`](./docs/orca-adaptive-orchestrator-architecture-zh.html) — architecture diagram
- [`docs/orca-adaptive-orchestrator-dataflow-zh.html`](./docs/orca-adaptive-orchestrator-dataflow-zh.html) — data-flow diagram
- [`docs/adr/0001-route-by-effective-model-and-supervised-lifecycle.md`](./docs/adr/0001-route-by-effective-model-and-supervised-lifecycle.md) — Effective Model and supervised lifecycle ADR

## Validation

```bash
python3 -m unittest discover -s orca-adaptive-orchestrator/tests -v
python3 orca-adaptive-orchestrator/scripts/inspect_runtime.py --pretty
```

<p align="center"><sub>Built for explicit, evidence-based coordination through Orca.</sub></p>
