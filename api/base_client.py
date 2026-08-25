import json

import allure
import httpx

from config import settings
from utils import logger, mask_secrets


class BaseApiClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float | None = None,
        retry_count: int | None = None,
    ) -> None:
        if base_url is None:
            base_url = settings.base_url
        if api_key is None:
            api_key = settings.api_key
        if timeout is None:
            timeout = settings.timeout
        if retry_count is None:
            retry_count = settings.retry_count

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["api_key"] = api_key

        self._retry_count = retry_count
        self._client = httpx.Client(base_url=base_url, headers=headers, timeout=timeout)

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        params = mask_secrets(kwargs.get("params") or {})
        payload = mask_secrets(kwargs.get("json") or {})
        logger.info("%s %s params=%s payload=%s", method, url, params, payload)
        allure.attach(
            json.dumps({"params": params, "payload": payload}, indent=2, ensure_ascii=False),
            name=f"request {method} {url}",
            attachment_type=allure.attachment_type.JSON,
        )

        for attempt in range(1, self._retry_count + 2):
            try:
                response = self._client.request(method, url, **kwargs)
            except httpx.TransportError as error:
                logger.warning(
                    "%s %s - attempt %s of %s failed: %s",
                    method,
                    url,
                    attempt,
                    self._retry_count + 1,
                    error,
                )
                if attempt > self._retry_count:
                    raise
                continue

            logger.info(
                "%s %s -> %s (%.2fs)",
                method,
                url,
                response.status_code,
                response.elapsed.total_seconds(),
            )
            allure.attach(
                response.text,
                name=f"response {response.status_code} {method} {url}",
                attachment_type=allure.attachment_type.TEXT,
            )
            return response

    def get(self, url: str, **kwargs) -> httpx.Response:
        return self._request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> httpx.Response:
        return self._request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> httpx.Response:
        return self._request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> httpx.Response:
        return self._request("DELETE", url, **kwargs)

    def close(self) -> None:
        self._client.close()
