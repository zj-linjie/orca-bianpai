# Runner and Model Routing

Use live inspection results for every invocation. A Runner is an agent CLI; an Effective Model is the model reached through that Runner's current aliases and provider configuration.

In force dispatch, the user's validated initial assignments override the capability routing below. Use [force-dispatch.md](force-dispatch.md) for requested/launch/effective model resolution, locking, and fast-path failures.

## Capability routing

Classify each Task by the minimum capability that can reliably satisfy its Quality Gate:

- **Flash tier**: bounded read-only research, mechanical edits, local UI changes, documentation, focused tests, and clearly specified single-point fixes.
- **Pro tier**: architecture, cross-module reasoning, difficult debugging, complex state, concurrency, migrations, security-sensitive code, integration, and high-risk review.
- **Strong fallback**: a verified strong Codex model for independent diagnosis or takeover after a Pro-tier failure.

Do not assign Flash to a Task merely because it is short. Risk, ambiguity, and reasoning coupling outweigh apparent size.

## Runner preferences

When the live configuration resolves both Runners to the same Flash model:

- prefer OpenCode for mechanical implementation, focused edits, migrations with a complete specification, and test additions;
- prefer Claude Code for investigation, option analysis, prompt/tool coordination, and light implementation that needs broader context;
- prefer Claude Code with an alias proven to resolve to the Pro model for complex implementation, debugging, integration, and high-risk review.

These are tie-breakers, not identities. The user's current example maps Claude Code's ordinary aliases and OpenCode defaults to a DeepSeek Flash model, while Claude Code's `opus` alias maps to DeepSeek Pro. Inspect instead of caching that mapping.

## Model and effort flags

The live Orca guide is authoritative. At the time this skill was authored, supervised `worker-start --model` supported Claude, Codex, and Cursor opaque model ids, but not OpenCode or Grok. `--effort` required `--model`; neither could combine with a reused `--terminal`.

For the user's current routing policy:

- Flash work normally omits effort.
- Pro work requests the alias proven to resolve to Pro and ordinarily requests `high` effort.
- Reserve `xhigh` for unusually difficult, well-bounded work.
- Avoid `max` and `ultra` by default.

Effort is a requested reasoning budget, not proof that a third-party backend honored it. Read `launch.requested` and `launch.effective` from the Orca receipt and report only what was requested and applied by the launcher.

OpenCode model overrides require custom agent argv because `worker-start --model` cannot express them. Use that path only when the user explicitly requested an OpenCode model and the current repository setup policy permits safe custom startup. Otherwise use OpenCode's configured default.

## Failure classification and Transfer

Preserve the old attempt's Task, Dispatch, completed work, failure symptom, bounded command output, files, tests, excluded hypotheses, and remaining Quality Gate.

- **Runner/tool failure**: switch to any verified available Runner in the same Capability Tier. Claude Code and OpenCode are the ordinary pair for the user's current setup; respect explicit inclusions/exclusions. If no same-tier alternative exists, pause at a Decision Gate instead of downgrading capability.
- **OpenCode provider/network failure**: certificate verification, stream, proxy, or transport errors belong to the Runner/tool/environment category, not model-resolution failure. Preserve bounded log evidence and run a non-secret health check before retrying. Do not change proxy settings automatically; when `lock-runner-model=true`, pause or wait for recovery instead of switching the locked assignment.
- **Reasoning failure**: escalate Flash to Pro.
- **Pro failure**: transfer to a verified strong Codex model for independent diagnosis or takeover; pause if it is unavailable.
- **Completed work failing validation**: create a Repair Task instead of relabeling it as a runtime retry.

One Task gets at most two automatic Dispatch attempts. Restate worktree placement, Runner, model, and effort on every replacement because retry linkage does not inherit them. A third attempt requires a user Decision Gate and must not silently collide with Orca's circuit breaker.
