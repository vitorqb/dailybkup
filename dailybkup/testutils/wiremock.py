import requests
import dataclasses
from urllib.parse import parse_qs
from typing import Dict, Any, Sequence, Optional


@dataclasses.dataclass
class WiremockRequest:
    method: str
    url: str
    formdata_raw: Optional[str] = None

    def formdata(self) -> Dict[str, Any]:
        return parse_qs(self.formdata_raw)

    @classmethod
    def from_dict(cls, x: Dict[str, Any]) -> "WiremockRequest":
        formdata_raw = None
        if "form-urlencoded" in x.get("headers", {}).get("Content-Type"):
            formdata_raw = x.get("body")

        return cls(
            method=x["method"],
            url=x["url"],
            formdata_raw=formdata_raw,
        )


@dataclasses.dataclass
class WiremockResponse:
    status: int
    json_body: Dict[str, Any]


class Wiremock:
    def __init__(self, *, url: str):
        self._url = url
        self._session = requests.Session()

    def url(self, path):
        return f"{self._url}{path}"

    def clean(self):
        self._session.delete(f"{self._url}/__admin/mappings").raise_for_status()
        self._session.delete(f"{self._url}/__admin/requests").raise_for_status()

    def request(self, **kwargs) -> WiremockRequest:
        return WiremockRequest(**kwargs)

    def response(self, **kwargs) -> WiremockResponse:
        return WiremockResponse(**kwargs)

    def stub(self, request: WiremockRequest, response: WiremockResponse) -> None:
        self._session.post(
            f"{self._url}/__admin/mappings",
            json={
                "request": {
                    "method": request.method,
                    "url": request.url,
                }
            },
        ).raise_for_status()

    def find(self, *, url: str, method: str) -> Sequence[WiremockRequest]:
        wiremock_response = self._session.post(
            f"{self._url}/__admin/requests/find",
            json={
                "method": method,
                "url": url,
            },
        )
        wiremock_response.raise_for_status()
        return [
            WiremockRequest.from_dict(x) for x in wiremock_response.json()["requests"]
        ]
