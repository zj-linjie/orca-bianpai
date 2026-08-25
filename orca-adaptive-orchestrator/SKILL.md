---
name: orca-adaptive-orchestrator
description: "Explicitly design and apply an adaptive policy for Orca work: analyze goals, decompose tasks, route by capability, define acceptance, and choose bounded recovery. Use only when the user invokes `$orca-adaptive-orchestrator`."
---

# Orca Adaptive Orchestrator

Act as the Policy Layer above Orca. Decide what work should happen and why; delegate runtime mechanics to Orca's version-matched guides.

## Boundary

This skill owns five decisions: **Analyze → Decompose → Route → Verify → Recover**.

Orca owns repository/worktree registration, Run and Task state, Dispatch and Worker lifecycle, terminal routing, messages, receipts, and cleanup. Before using those surfaces, resolve one Orca executable with the `orca-cli` rules and read its complete `orca-cli` and `orchestration` guides. Treat those guides and runtime receipts as authoritative; this skill does not redefine their command grammar or state transitions.

## Choose the mode

- **Default**: investigate read-only, show an Execution Manifest, and wait for confirmation.
- **Plan only**: stop after the Manifest.
- **Direct execution**: show the Manifest, then perform only its explicitly authorized local effects.
- **Force dispatch**: only `强制派发` or `force-dispatch` activates this path; read [references/force-dispatch.md](references/force-dispatch.md).

Preserve explicit limits on Workers, Runner/model choices, effort, placement, PR boundaries, and publication. Four is the maximum concurrent Worker count. Higher concurrency, destructive work, history rewriting, deployment, or remote publication requires a Decision Gate with explicit authority.

## Policy loop

1. **Analyze** — inspect repository instructions, Git state, test surfaces, and relevant Orca/Runner facts. Use `scripts/inspect_runtime.py --pretty` for allow-listed runtime and model-routing facts. If the repository is unmanaged, runtime readiness is uncertain, relevant changes are uncommitted, or a matching unfinished objective exists, expose that condition before execution.
2. **Decompose** — read [references/decomposition.md](references/decomposition.md). Produce the smallest conflict-free Task graph with observable acceptance and coherent PR Units.
3. **Route** — read [references/routing.md](references/routing.md). Match each Task to verified Runner/model capability and record the reason, evidence, constraints, and fallback.
4. **Verify** — define every Quality Gate in the [Execution Manifest](references/manifest.md), then independently inspect observable deliverables. A Worker report is evidence, not acceptance.
5. **Recover** — classify the failure before choosing bounded retry, Transfer, Repair, or a user Decision Gate. Preserve the prior attempt's evidence and use the live orchestration guide for the selected lifecycle operation.

Read only the references needed by the active mode and stage.

## Apply the policy

Before mutation, show the Manifest required by [references/manifest.md](references/manifest.md), except that force dispatch uses its validated constraints and Summary. Confirmation authorizes only the listed local effects.

Translate approved policy decisions into Orca Run objectives and Task specifications through the live orchestration guide. Runtime IDs, placement, launch/effective model, effort, liveness, settlement, and cleanup come from Orca receipts. Do not infer or cache them in policy prose.

Apply Quality Gates after the runtime reports an outcome. Create at most one automatic Repair Task for a completed deliverable that fails validation. A third Dispatch attempt, a second failed Quality Gate, unavailable required capability, scope expansion, or new external effects requires a Decision Gate.

## Complete

Finish only when every Task is accepted, explicitly deferred, or held at a user-visible Decision Gate. Report policy decisions, Orca receipt IDs, PR Units, tests and Quality Gates, Repairs or Transfers, unresolved risks, merge order, and publication status.
