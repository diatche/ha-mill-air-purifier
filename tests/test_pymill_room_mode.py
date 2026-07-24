"""Tests for Mill room-mode override API behavior."""

import sys
import types
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest

# Load the vendored client without importing the Home Assistant integration package.
_COMPONENT = Path(__file__).parents[1] / "custom_components" / "mill_air_purifier"
for name, path in (
    ("custom_components", _COMPONENT.parent.parent),
    ("custom_components.mill_air_purifier", _COMPONENT),
):
    package = types.ModuleType(name)
    package.__path__ = [str(path)]
    sys.modules.setdefault(name, package)

from custom_components.mill_air_purifier.pymill import Heater, Mill


@pytest.mark.asyncio
async def test_set_room_mode_override_posts_continuous_override() -> None:
    mill = Mill.__new__(Mill)
    mill.request = AsyncMock(return_value={"status": "ok"})
    mill._cache = Mock()
    mill.rooms = {"studio-room": {"mode": "weekly_program"}}
    mill.devices = {
        "heater": Heater(
            device_id="heater",
            room_id="studio-room",
            current_room_mode="weekly_program",
        )
    }

    result = await mill.set_room_mode_override("studio-room", "comfort")

    assert result is True
    mill.request.assert_awaited_once_with(
        "rooms/studio-room/mode/override",
        {
            "overrideModeType": "continuous",
            "overrideEndDate": 9_999_999_999,
            "mode": "comfort",
        },
    )
    assert mill.devices["heater"].current_room_mode == "comfort"
    assert mill.rooms["studio-room"]["mode"] == "comfort"


@pytest.mark.asyncio
async def test_set_room_mode_override_deletes_override_for_weekly_program() -> None:
    mill = Mill.__new__(Mill)
    mill.request = AsyncMock(return_value={})
    mill._cache = Mock()
    mill.rooms = {"studio-room": {"mode": "away"}}
    mill.devices = {
        "heater": Heater(
            device_id="heater",
            room_id="studio-room",
            current_room_mode="away",
        )
    }

    result = await mill.set_room_mode_override("studio-room", "weekly_program")

    assert result is True
    mill.request.assert_awaited_once_with(
        "rooms/studio-room/mode/override",
        {"disableOverride": True},
        delete=True,
    )
    assert mill.devices["heater"].current_room_mode == "weekly_program"
    assert mill.rooms["studio-room"]["mode"] == "weekly_program"


@pytest.mark.asyncio
async def test_set_room_mode_override_rejects_unknown_mode() -> None:
    mill = Mill.__new__(Mill)
    mill.request = AsyncMock()

    with pytest.raises(ValueError, match="Unsupported room mode"):
        await mill.set_room_mode_override("studio-room", "turbo")

    mill.request.assert_not_awaited()
