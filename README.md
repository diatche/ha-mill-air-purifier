# Mill Custom for Home Assistant

A custom Mill integration for Home Assistant, covering cloud features that are not available in the built-in `mill` integration.

The integration retains the `mill_air_purifier` domain for compatibility. It began with Mill air-purifier support and now also provides selected whole-home Mill controls, including room mode overrides.

## Features

- Mill air purifier sensors
- Existing Mill heater, socket, and local generation-3 support inherited from the upstream integration
- Room profile temperature service (`mill_air_purifier.set_room_temperature`)
- Room mode override control with Weekly program, Comfort, Sleep, Away, and Off options

The custom integration can remain installed alongside Home Assistant's built-in Mill integration while its broader device coverage is developed incrementally.

## Install with HACS

1. In HACS, open **Integrations**.
2. Open the three-dot menu and choose **Custom repositories**.
3. Add this repository URL as category **Integration**.
4. Install **Mill Custom**.
5. Restart Home Assistant.
6. Add the integration from **Settings > Devices & services > Add integration > Mill Custom**.

## Notes

- Cloud setup is the primary supported path.
- Local generation-3 heater support is retained from Home Assistant's built-in integration.
- The existing domain is intentionally unchanged to avoid a disruptive migration.
