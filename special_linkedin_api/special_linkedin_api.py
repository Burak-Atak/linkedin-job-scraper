import json
import logging
import time

from django.conf import settings
from linkedin_api import Linkedin
from linkedin_api.linkedin import default_evade
from requests.cookies import RequestsCookieJar
from requests.exceptions import ChunkedEncodingError

logger = logging.getLogger(__name__)


class SpecialLinkedinApi(Linkedin):
    def __init__(self, username, password):
        cookies = self._get_cookies()
        super().__init__(username, password, cookies=cookies)

    def _fetch(self, uri, evade=default_evade, base_request=False, **kwargs):
        """GET request to Linkedin API"""
        evade()
        self.client.session.cookies = self._get_cookies()

        url = f"{self.client.API_BASE_URL if not base_request else self.client.LINKEDIN_BASE_URL}{uri}"
        try:
            response = self.client.session.get(url, **kwargs)
            response.raise_for_status()
        except (ConnectionError, ChunkedEncodingError) as e:
            logger.warning(f"Connection error occurred: {e}")
            time.sleep(5)
            return self._fetch(uri, evade=evade, base_request=base_request, **kwargs)
        return response

    @classmethod
    def _get_cookies(cls):
        cookie_dict = json.loads(settings.LINKEDIN_COOKIES)
        cookies = RequestsCookieJar()
        for cookie in cookie_dict:
            cookies.set(cookie, cookie_dict[cookie])

        return cookies
