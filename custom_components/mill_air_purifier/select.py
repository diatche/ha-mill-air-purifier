"""Room mode override control for Mill cloud rooms."""

from typing import ClassVar

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import CONNECTION_TYPE, DOMAIN, LOCAL, MANUFACTURER
from .coordinator import MillConfigEntry, MillDataUpdateCoordinator

OPTION_TO_MODE = {
    "Weekly program": "weekly_program",
    "Comfort": "comfort",
    "Sleep": "sleep",
    "Away": "away",
    "Off": "off",
}
MODE_TO_OPTION = {mode: option for option, mode in OPTION_TO_MODE.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MillConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up room mode controls for Mill cloud rooms."""
    if entry.data.get(CONNECTION_TYPE) == LOCAL:
        return

    coordinator = entry.runtime_data
    known_rooms: set[str] = set()

    # Room metadata is needed to create room-scoped entities. The coordinator's
    # initial refresh may have completed before this platform registered its listener.
    await coordinator.mill_data_connection.update_devices()

    @callback
    def add_rooms() -> None:
        """Add controls for rooms discovered by the cloud client."""
        new_rooms = {
            room_id: room
            for room_id, room in coordinator.mill_data_connection.rooms.items()
            if room_id not in known_rooms
        }

        if not new_rooms:
            return

        known_rooms.update(new_rooms)
        async_add_entities(
            MillRoomModeSelect(coordinator, room_id, room)
            for room_id, room in new_rooms.items()
        )

    add_rooms()
    entry.async_on_unload(coordinator.async_add_listener(add_rooms))


class MillRoomModeSelect(CoordinatorEntity[MillDataUpdateCoordinator], SelectEntity):
    """Control a Mill room's active mode override."""

    _attr_has_entity_name = True
    _attr_name = "Mode override"
    _attr_options: ClassVar[list[str]] = list(OPTION_TO_MODE)

    def __init__(
        self,
        coordinator: MillDataUpdateCoordinator,
        room_id: str,
        room: dict,
    ) -> None:
        """Initialize the room mode control."""
        super().__init__(coordinator)
        self._room_id = room_id
        self._attr_unique_id = f"{room_id}_mode_override"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, room_id)},
            name=room.get("roomName") or room.get("name") or "Mill room",
            manufacturer=MANUFACTURER,
            model="Mill room",
        )
        self._update_attr()

    def _room(self) -> dict | None:
        """Return the latest cloud data for this room."""
        return self.coordinator.mill_data_connection.rooms.get(self._room_id)

    @callback
    def _update_attr(self) -> None:
        room = self._room()
        self._attr_available = room is not None
        self._attr_current_option = MODE_TO_OPTION.get(room.get("mode", "")) if room else None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated room data."""
        self._update_attr()
        self.async_write_ha_state()

    async def async_select_option(self, option: str) -> None:
        """Set the room's active override mode."""
        if option == self.current_option:
            return

        mode = OPTION_TO_MODE[option]
        success = await self.coordinator.mill_data_connection.set_room_mode_override(
            self._room_id, mode
        )
        if not success:
            raise HomeAssistantError(f"Failed to set Mill room mode to {option}")

        self._update_attr()
        self.async_write_ha_state()
        await self.coordinator.async_request_refresh()
