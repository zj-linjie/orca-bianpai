# Force Dispatch Policy

Use this branch only for the exact `强制派发` or `force-dispatch` trigger. It replaces the full pre-dispatch Manifest and second confirmation with validated constraints and an immediate Summary; all Orca lifecycle mechanics still come from the current orchestration guide.

## Normalize constraints

Require a global, pooled, or per-Task Runner/model assignment. Treat the first unquoted `:` or `：` after the controls as the objective delimiter, preserve the original request, and normalize:

- `max-workers=N`: adaptive peak concurrency, two through four;
- `parallel-workers=N`: exactly two through four safe initial Tasks;
- `strategy=partition|replicate`, defaulting to `partition`;
- optional effort, custom-launch permission, and Runner/model lock;
- placement, PR boundaries, and publication authority.

Assignment precedence is per-Task, fixed pool, global assignment, then adaptive routing. Explicit fields outrank prose. Force dispatch combined with plan-only, or any other conflicting or unverifiable constraint, pauses before mutation.

Without an exact count, use every dependency-ready, conflict-free, meaningful initial Task up to the effective ceiling, with a minimum of two. If fewer than two safe Tasks exist, offer ordinary direct execution or explicit replication. Exact seats are filled by longest dependency path, then higher risk, then repository order. For a fixed pool, pair the strongest verified assignment with the highest minimum tier and risk; preserve user order for ties.

## Resolve assignments

For every assignment record `requestedModel`, the launch model or default, the Effective Model evidence, Capability Tier, and lock state. `model=default` is valid only when live inspection resolves one unambiguous default. Unsupported effort, ambiguous aliases, unsafe custom startup, or insufficient mandatory review capability creates a Decision Gate.

`partition` uses distinct Task outcomes and ordinary conflict rules. `replicate` gives independent Workers the same Quality Gate for investigation, review, or comparison; competing implementations require isolated PR Units and a later selection gate.

A lock applies to every Task lineage it covers; later locked or cross-lineage work needs an explicit assignment. Locked work pauses after its recovery budget instead of silently changing Runner/model. Unlocked reviews and recovery may use the same-or-stronger verified capability. A locked reviewer below a mandatory tier may report evidence but cannot close the Quality Gate without a Decision Gate.

## Hard blockers

Pause before creating Orca state when the repository is unmanaged, relevant changes are uncommitted, required isolation is unavailable, a matching objective is unfinished, runtime/model readiness is unresolved, or concurrency exceeds four. Force dispatch does not authorize remote publication, deployment, destructive actions, force push, history rewriting, or work outside the objective.

## Summary

After Orca returns first-Wave receipts, report:

- Run and Task/Dispatch IDs;
- requested, started, held, and fenced counts;
- Runner plus requested/launch/effective model and effort;
- placement, PR Unit, capability warnings, and lock state;
- start failures and receipt-backed recovery status;
- review plan and remaining authority boundaries.

Continue with the ordinary Policy Loop: Verify outcomes independently, then choose bounded Recover decisions. Use Orca's guide for waiting, messaging, settlement, reuse, and cleanup.
