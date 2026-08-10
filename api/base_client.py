import httpx

from config import settings


class BaseApiClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float | None = None,
    ) -> None:
        if base_url is None:
            base_url = settings.base_url
        if api_key is None:
            api_key = settings.api_key
        if timeout is None:
            timeout = settings.timeout

        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["api_key"] = api_key

        self._client = httpx.Client(base_url=base_url, headers=headers, timeout=timeout)

    def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        return self._client.request(method, url, **kwargs)

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
