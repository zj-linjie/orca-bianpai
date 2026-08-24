# Force Dispatch

Use this fast path only when the user explicitly writes `强制派发` or `force-dispatch`. It replaces automatic initial model routing, the full Execution Manifest, and the second confirmation with validated constraints plus an immediate Dispatch Summary. It retains Orca supervision, safe decomposition, isolation, Quality Gates, and authority boundaries.

## Parse the request

Require an agent/Runner and model constraint. Parse assignments from explicit key/value fragments and ordinary natural language, treating the first unquoted `:` or `：` after the control fragments as the objective delimiter. Preserve the original text and normalize these optional controls:

- `max-workers=N`: adaptive peak concurrency from two through `N`.
- `parallel-workers=N`: the first Wave must contain exactly `N` safe independent Tasks.
- `strategy=partition|replicate`: default `partition`.
- `effort=<level>`: pass only when the live Runner/model combination supports it.
- `custom-launch=true`: permits the validated OpenCode custom-model path.
- `lock-runner-model=true`: locks every implementation, review, Repair, and Transfer Worker to the selected Runner/model.
- Global Runner/model, a fixed combination pool with counts, or per-Task assignments.

Only `强制派发` and `force-dispatch` trigger this mode. A request that combines force dispatch with plan-only is contradictory and pauses before mutation. Direct-execution wording is redundant but harmless.

Assignment precedence is per-Task assignment, fixed combination pool, global Runner/model, then ordinary adaptive routing. Explicit fields outrank prose: words such as “同时” request concurrency within the stated ceiling but do not turn `max-workers` into an exact first-Wave count. Force dispatch requires one of the first three. A higher-priority assignment that makes a lower-priority quota impossible is a conflict, not permission to improvise.

Without an exact count, start every dependency-ready, conflict-free, meaningful initial Task up to the effective ceiling: the Worker count is `min(max-workers or 4, safe initial Task count)`, with a minimum of two. When more Tasks are ready than available seats, choose those that unblock the longest dependency paths, breaking ties by higher risk isolation and then repository order. `max-workers` may lower the ceiling but never raise it above four; values below two contradict this mode. `parallel-workers` also accepts only two through four and claims exactly that many first-Wave seats. Fixed-pool counts likewise mean exact first-Wave seats, not total lifetime Dispatches or a reusable concurrency quota. When more safe Tasks exist than exact seats, fill seats using the same deterministic ordering and hold the rest for later Waves; when fewer exist, pause before state.

A fixed pool's count sum must be between two and four. Map it to selected Tasks by pairing the strongest verified assignment with the highest minimum Capability Tier and risk, then by longest dependency path and repository order. Preserve user order to break equal-assignment ties. If assignment capability cannot be verified or materially different valid mappings remain, pause instead of choosing arbitrarily. A fixed pool governs Wave 1 only; later unassigned implementation Tasks route adaptively. With `lock-runner-model=true`, every held or later Task needs an explicit assignment before the Run starts because adaptive routing is unavailable.

If fewer than two safe initial Tasks exist, pause and offer ordinary direct execution or explicit replication.

## Resolve the model

For every assignment record:

- `requestedModel`: the user's exact model text;
- `launchModel`: the Runner/Orca argument actually used;
- `effectiveModel`: the model resolved from live configuration and launch receipts.

Translate an Effective Model to a Runner alias only when the mapping is unique and verified. Ambiguous or unverifiable mappings create a Decision Gate. When the requested Effective Model is already the Runner's verified default, omit the model launch flag and retain the explicit model constraint in Run/Task state. If effort requires a launch model flag and no unambiguous alias exists, pause.

`model=default` satisfies the required model constraint only when live inspection resolves one unambiguous default Effective Model for that Runner. It uses the verified default without a model launch flag. Otherwise pause before mutation.

An omitted effort uses the Runner/model default. Never synthesize one in this mode. Read launch receipts and report requested versus effective values.

Use native supervised `worker-start` model preferences only for combinations supported by the live Orca guide. For OpenCode, `model=default` uses the verified configured default and needs no custom launch; any explicit `provider/model` id requires `custom-launch=true`, even when it currently equals that default. It also requires a repository setup policy compatible with custom argv. Start the custom terminal, attach it as a supervised Worker, and mark the non-native path in the Summary. OpenCode custom launch does not accept Orca effort. Unsafe setup ordering, unsupported combinations, or failed validation pause before dispatch instead of falling back to a default model.

Force dispatch is supervised end to end: native/default OpenCode uses `worker-start --agent opencode`; custom OpenCode uses a custom terminal followed by `worker-start --terminal <handle>`. A bare `dispatch --inject` receipt is `unsupervised/injected` and is not a valid Worker launch for this skill. Verify the returned Worker receipt before waiting, accepting output, or retrying, and block any retry that does not restore supervised lifecycle state.

## Decompose

`partition` creates distinct Tasks under the ordinary ownership and conflict rules. Every concurrently writing PR Unit has an isolated worktree/branch.

`replicate` sends the same Quality Gate to independent Workers for investigation, review, or solution comparison. Competing implementations require isolated worktrees/branches and remain unmerged until an Integration Task selects one against the declared Quality Gate. Preserve losing branches for inspection. Architecture or product trade-offs go to a user Decision Gate rather than majority vote.

The user's forced model controls every initial implementation Dispatch even when capability appears weak. Record the risk and use an adaptive same-or-stronger Reviewer unless `lock-runner-model=true`; escalate the Reviewer above the implementation tier only when the forced assignment carries a capability warning. With a global lock, every later Worker uses the same combination. With a pool or per-Task assignments, lock each Task lineage to its original combination and require an explicit assignment for cross-lineage Integration Tasks. Report any review capability limitation and pause after the second failed Dispatch attempt for that Task instead of switching or escalating; failures in one Task do not spend another Task's budget. A locked Reviewer below a mandatory high-risk review tier may run and report, but it cannot close that Quality Gate automatically: hold Run completion at a Decision Gate where the user may accept the documented limitation or authorize a qualified review.

## Hard blockers

Pause before creating state when the path is not an Orca-managed worktree, relevant changes are uncommitted, concurrent writers lack isolated checkouts, a matching Run is unfinished, a Runner/model/effort combination is unsupported, or requested concurrency exceeds four. Force dispatch never authorizes remote publication, deployment, force push, history rewrite, destructive actions, or work outside the objective.

## Dispatch and report

Persist the trigger, original constraints, normalized assignments, counts, strategy, lock state, and capability warnings in the Run objective and Task specs. Create all Tasks before starting the first Wave, then start every dependency-ready Task selected for that Wave within the effective ceiling or exact seats. The Dispatch record and `worker-start`/`worker-show` receipt are the source of truth for launch/effective model and effort; include those receipt-backed values in the Summary and resumed status. Mirror them into a structured Run status message only when the live guide explicitly supports that without changing Task lifecycle state.

If `worker-show` proves one Worker failed to start, allow successfully started independent Workers to continue and hold its dependents. A bare `agent_prompt_stalled` label, early capability revocation, or a live/output-producing exact terminal is an orchestration false positive / `outcome_unknown`, not a proven start failure; follow the supervision recovery guard before retrying or releasing it. Recover a proven failed Task through ordinary Transfer rules. When a failure proves a shared Runner/model configuration invalid, fence the remaining unstarted Workers using that combination. Report each as `not-started/fenced` with no Dispatch id; retry it only after the configuration is corrected or a Decision Gate changes the constraint.

When a remote PR request lacks remote, base, head, title, or dependency order, keep publication unauthorized. Continue the clearly requested local implementation and commits when those effects are independently authorized by the force-dispatch objective, and report publication as held. If publication is the only requested outcome, pause before creating state.

After processing every first-Wave start receipt, immediately show:

```md
# Dispatch Summary

Run: <id and objective>
Strategy: <partition|replicate>
Concurrency: <requested, started, and fenced>
Lock: <runner/model locked or adaptive follow-up>

| Task | Dispatch | Status | Runner | requestedModel | launchModel | effectiveModel | effort requested/effective | Worktree / branch | Capability warning |
|---|---|---|---|---|---|---|---|---|---|

Use `—` for the Dispatch and effective launch fields of a `not-started/fenced` Task.

Held Tasks: <Task and reason: dependency, capacity, fenced, or none>
Start failures: <receipts and recovery, or none>
Reviews: <adaptive plan or locked limitation>
Authority: <local effects authorized; remote/destructive effects still excluded>
```

Continue supervising after the Summary until the Run reaches the ordinary completion criteria.
