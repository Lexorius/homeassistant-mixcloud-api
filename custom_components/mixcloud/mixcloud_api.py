import aiohttp


class MixcloudError(Exception):
    """Custom exception for Mixcloud API errors."""

class MixcloudClient:
    def __init__(self, username, session):
        self._username = username
        self._session = session

    async def async_get_assets(self):
        base_url = f"https://api.mixcloud.com/{self._username}/"
        try:
            # Profil-Daten abrufen
            async with self._session.get(base_url) as resp:
                if resp.status != 200:
                    raise MixcloudError(f"Fehler beim Laden des Profils: {resp.status}")
                profile = await resp.json(content_type=None)

            # Uploads abrufen (cloudcasts)
            uploads_url = f"{base_url}cloudcasts/?limit=1&order_by=published"
            async with self._session.get(uploads_url) as resp:
                if resp.status != 200:
                    raise MixcloudError(f"Fehler beim Laden der Uploads: {resp.status}")
                uploads = await resp.json(content_type=None)
                last_upload = uploads["data"][0] if uploads["data"] else None

            return {
                "profile": profile,
                "last_upload": last_upload,
            }
        except aiohttp.ClientError as err:
            raise MixcloudError(f"Netzwerkfehler: {err}") from err
