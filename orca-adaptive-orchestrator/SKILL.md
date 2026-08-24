---
name: orca-adaptive-orchestrator
description: Explicitly plan, force-dispatch, and supervise context-aware Orca multi-agent work with adaptive task, model, effort, worktree, and PR boundaries.
---

# Orca Adaptive Orchestrator

Turn the user's objective into a supervised Orca Run whose Task boundaries, Workers, model capability, reasoning effort, isolation, and PR Units fit the actual repository. This skill runs only when the user explicitly invokes `$orca-adaptive-orchestrator`.

## Choose the mode

- **Default**: investigate read-only, show an Execution Manifest, and wait for confirmation before creating Orca state or changing files.
- **Plan only**: when the user says `仅规划` or equivalent, stop after the Manifest.
- **Direct execution**: when the user says `直接执行` or equivalent, show and record the Manifest, then proceed without a second confirmation. This mode does not authorize remote publication, deployment, destructive actions, force pushes, history rewrites, or scope not shown in the Manifest.
- **Force dispatch**: only the exact `强制派发` or `force-dispatch` trigger enters the fast path. Read [references/force-dispatch.md](references/force-dispatch.md) and follow it instead of building a full Manifest. Ordinary requests that merely name a Runner or model stay in the other modes.

Honor explicit overrides for a lower maximum Worker count, Runner inclusion/exclusion, model or Capability Tier, effort, single-Worker execution, independent versus stacked PRs, worktree placement, and remote PR publication. Four remains the hard concurrency ceiling; treat a higher request as a Decision Gate instead of silently exceeding it. Show every override in the Manifest, or persist and report it through the force-dispatch Summary.

## Establish live facts

1. Resolve one Orca executable using the current `orca-cli` rules and keep it fixed for the Run.
2. Read the complete version-matched guides with `<orca> skills get orca-cli` and `<orca> skills get orchestration`. Their current command grammar overrides examples in this skill.
3. Run `scripts/inspect_runtime.py --pretty`. Treat Runner names and Effective Models as separate facts. Never infer a model provider or capability from `claude`, `opencode`, `codex`, or another Runner name.
4. Confirm Orca readiness, repository context, Git status, relevant repository instructions, test surfaces, and existing orchestration state using read-only commands.
5. If an unfinished Run already covers this objective, present its Run, Tasks, Dispatches, and Workers and ask whether to resume or inspect it. Create another Run only after the user explicitly abandons or completes the old one, or defines a demonstrably distinct objective and scope.

The inspection script exposes only allow-listed status, version, binary, and model-routing fields. Do not print surrounding configuration or credentials. Force dispatch still completes this minimal preflight before creating state.

## Build the Execution Manifest

Read:

- [references/decomposition.md](references/decomposition.md) for Task, Wave, ownership, Quality Gate, and PR Unit decisions.
- [references/routing.md](references/routing.md) for Runner, Effective Model, Capability Tier, effort, and Transfer decisions.
- [references/manifest.md](references/manifest.md) for the required user-visible plan.

Investigate enough of the repository to make every Manifest field evidence-based. Do not start planning Workers to help plan: before confirmation, use only the Coordinator's read-only tools. Keep simple work with one Worker. Cap concurrent Workers at four unless the user set a lower limit. In force dispatch, use the fast-path decomposition and minimum-two-Worker contract in `force-dispatch.md` instead.

If the current checkout has relevant uncommitted changes, stop at a Decision Gate. Offer to keep one implementation Worker in the current worktree or let the user establish a clean baseline. Choosing the single-Worker option exits force dispatch and replans as ordinary direct execution. Never stash, commit, discard, or copy user changes on their behalf.

## Execute the approved work

Read [references/supervision.md](references/supervision.md), then execute either the approved Manifest or the validated force-dispatch constraints:

1. Require an Orca-managed worktree. If the path is unmanaged, stop and ask the user to authorize repository registration or switch to a managed worktree.
2. Create or bind exactly one Run for the objective.
3. Create every Task, including dependencies and parent relationships, before starting the first Wave.
4. Start all dependency-ready Workers in the Wave before waiting. Use supervised `worker-start`; use custom terminal composition only for an explicitly requested option that `worker-start` cannot express.
   Every Worker in this skill must have a supervised `worker-start` receipt. For native or default OpenCode, start with `worker-start --agent opencode`; for a custom OpenCode command, create the custom terminal and bind it with `worker-start --terminal <handle>`. A bare `dispatch --inject` path is unsupervised and does not satisfy this skill's lifecycle contract. After each start, inspect the returned receipt and require a supervised Worker state before waiting, accepting output, or retrying work.
5. Maintain one current implementation owner per PR Unit. Every concurrently active implementation PR Unit uses its own approved checkout/worktree and branch; otherwise serialize the implementation Tasks. Path-level non-overlap alone does not make concurrent Git branch/index operations safe.
6. Supervise until every expected Dispatch settles. Treat timeouts and TUI idle as liveness checkpoints, not failures.
7. Apply Quality Gates independently of a Worker's claimed outcome. Create at most one automatic Repair Task for a completed deliverable that fails validation.
8. Settle every Worker by immediate reuse, explicit retention requested by the user, or `worker-release` after its result is processed.

When the Manifest or force-dispatch request authorizes local branches and commits, Workers may create only the derived PR Units within the stated objective. Remote pushes and PR creation require a separate explicit authorization that names remote, base, head, title, and dependency order. Never force push.

## Recovery and authority

Preserve evidence when a Dispatch fails. Switch Runner within the same Capability Tier for Runner/tool failures; escalate capability for reasoning failures unless validated force-dispatch constraints lock the Runner/model. Link replacement attempts with the live guide's retry mechanism and restate placement, Runner, model, and effort explicitly.

Treat a startup label as evidence to investigate, not as proof of worker failure. If `agent_prompt_stalled` occurs before the configured startup timeout, `capability_revoked_at` precedes terminal exit or latest output, or the exact Worker terminal remains live or produces output after the failure timestamp, classify the attempt as an orchestration false positive / `outcome_unknown`. Inspect `worker-show`, bounded `worker-read` or terminal output, the Run inbox, and the Quality Gate evidence. Do not retry, stop, release, or treat the status as a terminal failure solely because of that label or a rejected/stale `worker_done`; only recover after the exact process is proven stopped/failed or the live guide's outcome-unknown recovery path has been completed.

Allow at most two automatic Dispatch attempts for one Task. A third attempt requires a Decision Gate. A failed Pro-tier attempt may transfer to a verified strong Codex model when routing is adaptive; a locked force-dispatch Run pauses instead of switching, and an unavailable fallback always pauses instead of downgrading to Flash.

Answer Worker questions only from the approved Manifest or validated force-dispatch constraints and repository facts. Scope expansion, architectural choices, external side effects, and exhausted recovery budgets belong to the user.

If the user cancels, stop only proven active supervised Dispatches, preserve branches, worktrees, commits, and archived output, and report how the Run can resume. Do not delete worktrees automatically.

## Complete the Run

Deliver a final report covering every PR Unit's branch, commits, Quality Gates, tests, review outcome, dependency/merge order, Transfers, unresolved risks, and remote PR status. Completion requires every Task to be accepted, explicitly deferred, or placed behind a user-visible Decision Gate; a `worker_done` message alone is not acceptance.
