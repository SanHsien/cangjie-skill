from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_star_history.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("generate_star_history", SCRIPT)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_star_history_helpers_do_not_need_network() -> None:
    module = _load_module()
    assert module.nice_tick_step(8633) >= 1
    assert module.format_star_tick(1000) == "1K"
    assert module.format_star_tick(12) == "12"
