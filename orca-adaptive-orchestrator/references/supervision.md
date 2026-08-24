# Supervision and Recovery

Use the current version-matched Orca orchestration guide for exact commands and receipts. This reference defines the Coordinator's state transitions.

Force dispatch uses the same lifecycle. Its validated constraints replace Manifest confirmation, and its first-Wave receipts produce the Dispatch Summary defined in `force-dispatch.md`.

## Start a Wave

Create or bind one Run, then create every Task and its dependencies before starting Workers. Start every dependency-ready Worker in the Wave before waiting. Verify Task and Dispatch provenance before claiming orchestration is active.

Use supervised worker composition for lifecycle ownership. A full handoff is different: it transfers ownership and ends monitoring, so it cannot satisfy this skill's ordinary supervised mode.

Every Worker must be launched through `worker-start`, and its returned receipt must show supervised lifecycle state before the coordinator waits, accepts output, or retries. Native/default OpenCode uses `--agent opencode`; custom OpenCode commands use a custom terminal bound with `worker-start --terminal <handle>`. If `worker-show` reports `unsupervised` or stage `injected`, stop the lifecycle path, preserve the terminal, and correct the launch before retrying.

If a first-Wave start partially fails, let successfully started independent Workers continue and hold only dependent work. A failure that proves a shared launch combination invalid fences the remaining unstarted uses of that combination.

## Monitor

Wait for `worker_done`, `escalation`, and `question` messages in bounded rolling windows. Process the complete delivery before acknowledging it. A timeout, heartbeat, visible activity, or TUI idle state is a checkpoint, not a failure.

On a timeout, inspect the Task, Dispatch, bounded Worker output, and terminal liveness. Continue waiting while evidence shows useful activity. Do not stop, release, duplicate, or replace a Worker without a proven terminal condition or explicit cancellation.

Startup false-positive guard: when `agent_prompt_stalled` happens before the configured startup timeout, capability is revoked while the exact terminal is still live, or output/artifacts continue after the reported failure, keep the attempt as `outcome_unknown` for coordination purposes. Read `worker-show`, bounded `worker-read` or terminal output, inbox evidence, and the Quality Gate before deciding. A rejected or stale `worker_done` is not a valid failure signal by itself; do not retry, stop, release, or mark the work accepted until the exact process is proven stopped/failed or the live guide's recovery action resolves the unknown outcome.

Answer Worker questions from the approved Manifest or validated force-dispatch constraints and repository facts. Use a user Decision Gate for scope expansion, architecture choices, new external effects, risk expansion, or exhausted recovery limits.

## Accept or repair

Validate the Task's Quality Gate independently. On an accepted `worker_done`, either transfer the exact terminal immediately to an approved follow-up Task or release it after processing. Release failed settled Workers too. Retain a terminal only when the user explicitly requests live debugging.

If completed output fails its Quality Gate, create one Repair Task owned by another Worker. Re-review the repair. A second quality failure pauses for the user.

## Recover a failed attempt

Inspect the supervised Worker receipt first:

- Ready or active: continue waiting or read bounded output.
- Proven failed or stopped: create a replacement linked to the previous Dispatch, explicitly selecting placement and Runner/model options again. `agent_prompt_stalled` alone is not proof when capability was revoked early or the exact terminal remained live.
- Outcome unknown: follow the live receipt's stop-and-inspect or abandon path. Abandonment does not prove the process or filesystem stopped.

For an OpenCode provider certificate or stream error, classify the attempt as a Runner/tool or environment failure, preserve the bounded log evidence, and run a non-secret network/proxy health check before spending another retry. Do not modify proxy settings automatically. A locked force-dispatch Run pauses or waits for the environment rather than switching Runner/model; retry only after the attempt is proven stopped/failed and the health check is recovered.

Transfer the evidence package described in `routing.md`. Never downgrade Pro reasoning work to Flash merely to use a different Runner.

## Resume and cancel

When a matching unfinished Run exists, show its objective, Tasks, Dispatches, Workers, Decision Gates, and archived output. Ask the user to resume or inspect it. A new Run is valid only after the user explicitly abandons or completes the old one, or when the new request has a demonstrably distinct objective and scope; never duplicate a live objective.

On cancellation, stop only exact active supervised Dispatches. Preserve worktrees, branches, commits, setup terminals, and archived output. Report a concrete resume path. Never reset orchestration state or remove worktrees as ordinary cleanup.

## Publish and finish

Local branch/commit authorization comes from the approved Manifest or validated force-dispatch objective and constraints. Remote publication needs a separate authorization naming remote, base, head, PR title, and dependency order. Assign one publication owner and prohibit force push.

The final report accounts for every Task and settled Worker. Include branches, commits, Quality Gates, tests, reviews, dependency/merge order, Transfers, Repair Tasks, baseline failures, unresolved risks, Decision Gates, and remote PR state.
