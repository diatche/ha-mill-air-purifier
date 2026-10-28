"""Validation helpers for Mill service inputs."""

from typing import Any

from .const import MAX_TEMP, MIN_TEMP


def validate_room_temperature(value: Any) -> float:
    """Coerce a room temperature to float while preserving half degrees."""
    temperature = float(value)
    if not MIN_TEMP <= temperature <= MAX_TEMP:
        raise ValueError(
            f"room temperature must be between {MIN_TEMP} and {MAX_TEMP} °C"
        )
    return temperature
