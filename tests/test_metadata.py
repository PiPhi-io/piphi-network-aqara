from __future__ import annotations

import json
from pathlib import Path

from piphi_network_aqara import runtime as runtime_module


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


def test_automation_registry_matches_declared_behavior_commands() -> None:
    root = Path(__file__).resolve().parent.parent / "src"
    behaviors = json.loads((root / "behaviors.json").read_text())
    declared_commands = {
        action["runtime"]["command"]
        for device in behaviors["devices"]
        for action in device.get("actions", [])
    }
    registered_commands = {
        definition.command
        for definition in runtime_module.automation_registry.action_definitions
    }

    assert registered_commands == declared_commands
