import json
import os

import requests

from llm_model.base import BaseChatModel
from shared_module.configuration import EnvVar


class OpenAIModel(BaseChatModel):
    def __init__(
        self,
        temperature: float,
        model: str,
        json_response: bool,
        max_retries: int = 3,
        retry_delay: int = 1,
    ):
        super().__init__(
            temperature,
            model,
            json_response,
            max_retries,
            retry_delay,
        )
        self.model_endpoint = "https://api.openai.com/v1/chat/completions"
        self.api_key = EnvVar.openai_api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def invoke(self, messages: list[dict[str, str]]) -> str:
        system = messages[0]["content"]
        user = messages[1]["content"]

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "temperature": self.temperature,
        }

        if self.json_response:
            payload["response_format"] = {"type": "json_object"}

        try:
            response_json = self._make_request(
                self.model_endpoint,
                self.headers,
                payload,
            )

            if self.json_response:
                response = json.dumps(
                    json.loads(
                        response_json["choices"][0]["message"]["content"],
                    )
                )
            else:
                response = response_json["choices"][0]["message"]["content"]

            return response
        except requests.RequestException as e:
            return json.dumps(
                {
                    "error": f"Error in invoking model after {self.max_retries} retries: {str(e)}"
                }
            )
        except json.JSONDecodeError as e:
            return json.dumps(
                {"error": f"Error processing response: {str(e)}"},
            )
