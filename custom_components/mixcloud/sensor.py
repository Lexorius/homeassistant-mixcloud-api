import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

COUNT_KEYS = [
    "follower_count",
    "following_count",
    "cloudcast_count",
    "favorite_count",
    "listen_count",
]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    username = entry.data["username"]

    sensors = []
    # Ein Sensor pro *_count
    for key in COUNT_KEYS:
        sensors.append(MixcloudCountSensor(coordinator, username, key))
    # Ein Profilsensor für alle anderen Infos
    sensors.append(MixcloudProfileSensor(coordinator, username))
    # Optional: Sensor für letzte Upload-Infos
    sensors.append(MixcloudLastUploadSensor(coordinator, username))

    async_add_entities(sensors)

class MixcloudCountSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, username, key):
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"mixcloud_{username}_{key}"
        self._attr_name = f"Mixcloud {username} {key.replace('_', ' ').title()}"

    @property
    def state(self):
        data = self.coordinator.data
        if not data or "profile" not in data:
            return None
        return data["profile"].get(self._key)

class MixcloudProfileSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, username):
        super().__init__(coordinator)
        self._attr_unique_id = f"mixcloud_{username}_profile"
        self._attr_name = f"Mixcloud {username} Profil"

    @property
    def state(self):
        data = self.coordinator.data
        if not data or "profile" not in data:
            return None
        return data["profile"].get("city")  # oder ein anderes zentrales Feld

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        if not data or "profile" not in data:
            return {}
        profile = data["profile"]
        # Alle Felder außer *_count als Attribute
        return {
            k: v for k, v in profile.items()
            if not k.endswith("_count") and k not in ["city"]  # city ist state
        }

class MixcloudLastUploadSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, username):
        super().__init__(coordinator)
        self._attr_unique_id = f"mixcloud_{username}_last_upload"
        self._attr_name = f"Mixcloud {username} Letzter Upload"

    @property
    def state(self):
        data = self.coordinator.data
        if not data or not data.get("last_upload"):
            return None
        return data["last_upload"].get("name")

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        if not data or not data.get("last_upload"):
            return {}
        upload = data["last_upload"]
        return {
            "created_time": upload.get("created_time"),
            "url": upload.get("url"),
            "plays": upload.get("play_count"),
            "likes": upload.get("favorite_count"),
        }
