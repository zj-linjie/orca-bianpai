import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "inspect_runtime.py"
SPEC = importlib.util.spec_from_file_location("inspect_runtime", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class InspectRuntimeTests(unittest.TestCase):
    def test_jsonc_comments_do_not_damage_urls_or_strings(self):
        raw = '{\n  // comment\n  "model": "provider/model",\n  "url": "https://example.test/*safe*/"\n}'
        parsed = json.loads(MODULE.strip_jsonc_comments(raw))
        self.assertEqual(parsed["model"], "provider/model")
        self.assertEqual(parsed["url"], "https://example.test/*safe*/")

    def test_claude_inspection_ignores_credentials(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            config_dir = home / ".claude"
            config_dir.mkdir()
            (config_dir / "settings.json").write_text(
                json.dumps(
                    {
                        "env": {
                            "ANTHROPIC_MODEL": "small-model",
                            "ANTHROPIC_API_KEY": "must-not-appear",
                            "AUTHORIZATION": "must-not-appear",
                        }
                    }
                ),
                encoding="utf-8",
            )
            result = MODULE.inspect_claude(home)
            rendered = json.dumps(result)
            self.assertIn("small-model", rendered)
            self.assertNotIn("must-not-appear", rendered)
            self.assertNotIn("API_KEY", rendered)
            self.assertNotIn("AUTHORIZATION", rendered)

    def test_opencode_conflicting_models_are_ambiguous(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            config_dir = home / ".config" / "opencode"
            config_dir.mkdir(parents=True)
            (config_dir / "opencode.json").write_text(
                json.dumps({"model": "provider/one", "apiKey": "must-not-appear"}),
                encoding="utf-8",
            )
            (config_dir / "opencode.jsonc").write_text(
                '{"model": "provider/two", "token": "must-not-appear"}',
                encoding="utf-8",
            )
            result = MODULE.inspect_opencode(home)
            rendered = json.dumps(result)
            self.assertTrue(result["ambiguous"])
            self.assertIsNone(result["resolvedModel"])
            self.assertNotIn("must-not-appear", rendered)


if __name__ == "__main__":
    unittest.main()
