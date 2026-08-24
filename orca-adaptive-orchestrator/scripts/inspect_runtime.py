#!/usr/bin/env python3
"""Print allow-listed Orca, Runner, and model-routing facts as JSON."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any


RUNNERS = ("claude", "opencode", "codex", "grok")
CLAUDE_MODEL_KEYS = (
    "ANTHROPIC_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_FABLE_MODEL",
)


def resolve_orca() -> list[str]:
    configured = os.environ.get("ORCA_CLI_COMMAND")
    if configured:
        command = shlex.split(configured)
        if command:
            return command
    if os.environ.get("ORCA_DEV_REPO_ROOT"):
        return ["orca-dev"]
    if platform.system() == "Linux":
        return ["orca-ide"]
    return ["orca"]


def run_bounded(command: list[str], timeout: int = 10) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
            env=os.environ.copy(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "error": type(exc).__name__}

    output = (result.stdout or result.stderr).strip().splitlines()
    return {
        "ok": result.returncode == 0,
        "exitCode": result.returncode,
        "firstLine": output[0][:200] if output else "",
    }


def orca_status(command: list[str]) -> dict[str, Any]:
    try:
        result = subprocess.run(
            [*command, "status", "--json"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
            env=os.environ.copy(),
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"ok": False, "error": type(exc).__name__}

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "exitCode": result.returncode, "error": "invalid_json"}

    app = payload.get("result", {}).get("app", {})
    runtime = payload.get("result", {}).get("runtime", {})
    capabilities = runtime.get("capabilities", [])
    return {
        "ok": payload.get("ok") is True,
        "appRunning": app.get("running"),
        "runtimeState": runtime.get("state"),
        "runtimeReachable": runtime.get("reachable"),
        "appVersion": runtime.get("appVersion"),
        "workerLaunchPreferences": "orchestration.worker-launch-preferences.v1"
        in capabilities,
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def strip_jsonc_comments(text: str) -> str:
    output: list[str] = []
    index = 0
    in_string = False
    escaped = False
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if in_string:
            output.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            output.append(char)
            index += 1
            continue
        if char == "/" and next_char == "/":
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue
        if char == "/" and next_char == "*":
            index += 2
            while index + 1 < len(text) and text[index : index + 2] != "*/":
                index += 1
            index += 2
            continue
        output.append(char)
        index += 1
    return "".join(output)


def load_jsonc(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(strip_jsonc_comments(path.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def inspect_claude(home: Path) -> dict[str, Any]:
    resolved: dict[str, str] = {}
    sources: list[str] = []
    for filename in ("settings.json", "settings.local.json"):
        path = home / ".claude" / filename
        data = load_json(path)
        env = data.get("env", {})
        if not isinstance(env, dict):
            continue
        found = False
        for key in CLAUDE_MODEL_KEYS:
            value = env.get(key)
            if isinstance(value, str):
                resolved[key] = value
                found = True
        if found:
            sources.append(filename)
    return {"sources": sources, "modelAliases": resolved}


def inspect_opencode(home: Path) -> dict[str, Any]:
    candidates: list[dict[str, str]] = []
    config_dir = home / ".config" / "opencode"
    for filename, loader in (("opencode.json", load_json), ("opencode.jsonc", load_jsonc)):
        data = loader(config_dir / filename)
        fields = {
            key: value
            for key in ("model", "small_model")
            if isinstance((value := data.get(key)), str)
        }
        if fields:
            candidates.append({"source": filename, **fields})

    unique_models = sorted(
        {entry[key] for entry in candidates for key in ("model", "small_model") if key in entry}
    )
    return {
        "configurations": candidates,
        "resolvedModel": unique_models[0] if len(unique_models) == 1 else None,
        "ambiguous": len(unique_models) > 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    home = Path.home()
    orca_command = resolve_orca()
    runners: dict[str, Any] = {}
    for runner in RUNNERS:
        binary = shutil.which(runner)
        runners[runner] = {
            "installed": binary is not None,
            "binary": binary,
            "version": run_bounded([runner, "--version"]) if binary else None,
        }

    payload = {
        "orca": {
            "command": orca_command,
            "binary": shutil.which(orca_command[0]),
            "status": orca_status(orca_command),
        },
        "runners": runners,
        "routing": {
            "claude": inspect_claude(home),
            "opencode": inspect_opencode(home),
        },
        "safety": {
            "allowListedFieldsOnly": True,
            "credentialsRead": False,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
