import json

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed


class BaseChatModel:
    def __init__(
        self,
        temperature: float,
        model: str,
        json_response: bool,
        max_retries: int = 3,
        retry_delay: int = 1,
    ):
        self.temperature = temperature
        self.model = model
        self.json_response = json_response
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type(requests.RequestException),
    )
    def _make_request(self, url, headers, payload):
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
        )
        response.raise_for_status()
        return response.json()
