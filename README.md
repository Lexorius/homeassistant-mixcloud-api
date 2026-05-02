# Mixcloud Home Assistant Integration

[![hassfest](https://github.com/Lexorius/homeassistant-mixcloud-api/actions/workflows/hassfest.yml/badge.svg)](https://github.com/Lexorius/homeassistant-mixcloud-api/actions/workflows/hassfest.yml)
[![HACS validation](https://github.com/Lexorius/homeassistant-mixcloud-api/actions/workflows/hacs.yml/badge.svg)](https://github.com/Lexorius/homeassistant-mixcloud-api/actions/workflows/hacs.yml)
[![Python checks](https://github.com/Lexorius/homeassistant-mixcloud-api/actions/workflows/python-checks.yml/badge.svg)](https://github.com/Lexorius/homeassistant-mixcloud-api/actions/workflows/python-checks.yml)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/Lexorius/homeassistant-mixcloud-api.svg)](https://github.com/Lexorius/homeassistant-mixcloud-api/releases)
[![GitHub Activity](https://img.shields.io/github/commit-activity/y/Lexorius/homeassistant-mixcloud-api.svg)](https://github.com/Lexorius/homeassistant-mixcloud-api/commits/main)
[![Version](https://img.shields.io/badge/version-1.1.2-blue)](https://github.com/Lexorius/homeassistant-mixcloud-api)

This custom component integrates [Mixcloud](https://www.mixcloud.com/) user data into [Home Assistant](https://www.home-assistant.io/) via HACS. It provides sensors for follower counts, uploads, and profile information for any public Mixcloud user.

Each release is automatically validated by GitHub Actions: **hassfest** (Home Assistant manifest checks), **HACS validation**, and a **Python checks** workflow that runs `compileall`, `ruff`, the local manifest order check (`scripts/check-manifest.sh`), JSON/YAML lint, and a CHANGELOG-version-consistency check. The badges above reflect the current state of the `main` branch.

---

## Features

- **Sensors for all count fields**: Follower count, following count, cloudcast count, favorite count, listen count.
- **Profile sensor**: All other profile information (bio, city, country, etc.) is available as attributes of a single sensor.
- **Last upload sensor**: Shows the latest upload and its details.
- **Flexible config flow**: Enter either your Mixcloud username or the full profile URL during setup.

---

## Upgrading from 1.0.x — Breaking change

Starting with **1.1.0**, the integration's domain has been renamed from `hacs-mixcloud-api` to **`mixcloud`**.

This change was necessary because Home Assistant requires the manifest `domain` to match the integration's directory name (`custom_components/mixcloud/`) and to consist of `[a-z0-9_]` only — the previous value contained a hyphen and did not match the folder name, so hassfest rejected the integration.

**What you need to do after upgrading:**

1. Remove the existing Mixcloud integration entry under **Settings → Devices & Services**.
2. Restart Home Assistant.
3. Re-add the integration; existing config entries from 1.0.x cannot be migrated automatically because they were registered under the old domain string.

Sensor entity IDs stay the same (`sensor.mixcloud_<username>_*`) — only the underlying integration domain changed.

---

## Installation

1. **Via HACS (recommended):**
   - Go to HACS → Integrations → Custom repositories.
   - Add this repository URL and select "Integration".
   - Search for "Mixcloud" and install.

2. **Manual:**
   - Copy the `mixcloud` folder into your `custom_components` directory.

3. **Restart Home Assistant** after installation.

---

## Configuration

### Add via UI

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Mixcloud**.
3. Enter either your Mixcloud username (e.g. `knockwood`) **or** your profile URL (e.g. `https://api.mixcloud.com/knockwood/`).
4. Confirm and finish setup.

### Options

- **Scan interval**: By default, data is updated every 5 minutes (300 seconds). You can adjust this in the integration options.

---

## Sensors

After setup, the following sensors will be created (replace `yourusername` with your Mixcloud username):

- `sensor.mixcloud_yourusername_follower_count`
- `sensor.mixcloud_yourusername_following_count`
- `sensor.mixcloud_yourusername_cloudcast_count`
- `sensor.mixcloud_yourusername_favorite_count`
- `sensor.mixcloud_yourusername_listen_count`
- `sensor.mixcloud_yourusername_profile`  
  - Attributes: `biog`, `created_time`, `updated_time`, `is_pro`, `is_premium`, `city`, `country`, `cover_pictures`, etc.
- `sensor.mixcloud_yourusername_last_upload`  
  - State: Name of the last upload  
  - Attributes: `created_time`, `url`, `plays`, `likes`

---

## Example

**Profile sensor attributes:**
```yaml
biog: "The german dj and radio-host..."
created_time: "2013-12-16T22:55:03Z"
city: "Stuttgart"
country: "Germany"
is_pro: true
cover_pictures:
  835wx120h: "https://thumbnailer.mixcloud.com/..."
  ...
```

---

## Troubleshooting

- If you see `Network error` or `invalid_username`, check your username or URL.
- Only public Mixcloud profiles are supported.
- Make sure your Home Assistant instance can reach `api.mixcloud.com`.

---

## Version

**1.1.2**

---

## Credits

- [Mixcloud API](https://www.mixcloud.com/developers/)
- Home Assistant Community

---

## License

MIT License