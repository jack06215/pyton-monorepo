import json
from typing import Any, Generator, cast

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed


class BaseChatModel:
    def __init__(
        self,
        temperature: float,
        model: str,
        json_response: bool | None = None,
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
        try:
            response = requests.post(
                url,
                headers=headers,
                data=json.dumps(payload),
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            raise e

    async def _make_stream_request(self, url, headers, payload) -> Any:
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(payload),
            stream=True,  # Ensure the stream parameter is set to True
        )

        # Process the response line by line if newline-delimited
        # or use response.iter_content for arbitrary chunk sizes
        for chunk in response.iter_lines():
            try:
                data = cast(str, chunk.decode()[5:])
                if data.strip() not in ("", "[DONE]"):
                    return json.loads(data)

            except requests.RequestException as e:
                print(f"Request failed: {e}")
                raise e
