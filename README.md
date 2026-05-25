# Mill Air Purifier for Home Assistant

Experimental custom integration for testing Mill air purifier support without replacing Home Assistant's built-in `mill` integration.

This integration uses a separate domain, `mill_air_purifier`, so the built-in Mill integration can remain installed during the trial. It vendors a patched copy of `millheater` with support for the Mill cloud device type `Air Purifiers`.

## Install with HACS

1. In HACS, open **Integrations**.
2. Open the three-dot menu and choose **Custom repositories**.
3. Add this repository URL as category **Integration**.
4. Install **Mill Air Purifier**.
5. Restart Home Assistant.
6. Add the integration from **Settings > Devices & services > Add integration > Mill Air Purifier**.

## Test plan

Keep the existing built-in Mill integration in place. Add this custom integration separately with the same Mill cloud credentials, then confirm the air purifier appears and exposes sensible sensor values.

If the custom integration is not useful, remove it from HACS and restart Home Assistant. The built-in `mill` integration is not modified by this repository.

## Known limits

- This is for cloud setup first. Local generation-3 heater support is copied from Home Assistant's built-in integration but is not the reason for this fork.
- The cloud setup intentionally exposes only Mill air purifier devices. Keep the built-in Mill integration for heaters and Mill Sense.
