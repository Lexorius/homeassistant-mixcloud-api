import re

import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN


def extract_username(value: str) -> str | None:
    # Extrahiere Username aus URL oder gib Username direkt zurück
    value = value.strip()
    # Prüfe auf URL-Format
    match = re.match(r"https?://api\.mixcloud\.com/([^/]+)/?", value, re.IGNORECASE)
    if match:
        return match.group(1)
    # Prüfe auf Username (nur Buchstaben/Zahlen/_/- erlaubt)
    if re.match(r"^[\w-]+$", value):
        return value
    return None

class MixcloudConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Mixcloud."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            username = extract_username(user_input["username"])
            if not username:
                errors["username"] = "invalid_username"
            else:
                return self.async_create_entry(title=username, data={"username": username})

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username", description={"suggested_value": ""}): str,
            }),
            errors=errors,
        )
