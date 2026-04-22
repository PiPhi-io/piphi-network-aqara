from __future__ import annotations

import json
from pathlib import Path


def test_manifest_and_behaviors_align() -> None:
    root = Path(__file__).resolve().parent.parent / "src"
    manifest = json.loads((root / "manifest.json").read_text())
    behaviors = json.loads((root / "behaviors.json").read_text())

    manifest_capabilities = set(manifest["entities"][0]["capabilities"])
    behavior_capabilities = set(behaviors["devices"][0]["capabilities"])
    behavior_actions = {item["id"] for item in behaviors["devices"][0]["actions"]}

    assert manifest["id"] == "aqara-open-api"
    assert manifest["api"]["endpoints"]["config_sync"] == "/configs/sync"
    assert behavior_capabilities == manifest_capabilities
    assert {"refresh", "turn_on", "turn_off", "open", "close", "set_position", "set_brightness"} <= behavior_actions
    assert "stop" not in behavior_actions
