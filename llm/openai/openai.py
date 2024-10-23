import json
from typing import Any, Literal, cast

import requests

from llm.base import BaseChatModel
from shared_module.configuration import EnvVar


class OpenAIModel(BaseChatModel):
    def __init__(
        self,
        temperature: float,
        model: str,
        json_response: bool = True,
        max_retries: int = 3,
        retry_delay: int = 1,
    ):
        super().__init__(
            temperature=temperature,
            model=model,
            max_retries=max_retries,
            retry_delay=retry_delay,
            json_response=json_response,
        )
        self.model_endpoint = "https://api.openai.com/v1/chat/completions"
        self.api_key = EnvVar.openai_api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    def invoke(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: Literal["auto", "required", "none"] = "none",
    ) -> Any:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "temperature": self.temperature,
        }

        if tools and tool_choice != "none":
            if isinstance(tools[0], dict):
                payload["tool_choice"] = tool_choice
                payload["tools"] = [
                    {
                        "type": "function",
                        "function": {
                            "name": tool["name"],
                            "description": tool["description"],
                            "parameters": tool["parameters"],
                            "strict": tool["strict"],
                        },
                    }
                    for tool in tools
                ]
                payload["tool_choice"] = tool_choice

        try:
            response_json = self._make_request(
                self.model_endpoint,
                self.headers,
                payload,
            )
            response = json.dumps(response_json)

            return response
        except requests.RequestException as e:
            return json.dumps(
                {
                    "error": f"Error in invoking model after {self.max_retries} retries: {str(e)}"  # noqa
                }
            )
        except json.JSONDecodeError as e:
            return json.dumps(
                {"error": f"Error processing response: {str(e)}"},
            )

    async def ainvoke(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        tool_choice: str = "none",
    ) -> Any:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "temperature": self.temperature,
            "tool_choice": "none",
        }

        if tools and tool_choice != "none":
            if isinstance(tools[0], dict):
                payload["tools"] = [
                    {
                        "type": "function",
                        "function": {
                            "name": tool["name"],
                            "description": tool["description"],
                            "parameters": tool["parameters"],
                            "strict": tool["strict"],
                        },
                    }
                    for tool in cast(list[dict[str, Any]], tools)
                ]
                payload["tool_choice"] = tool_choice

        try:
            async for chunk in await self._make_stream_request(
                self.model_endpoint,
                self.headers,
                payload,
            ):
                yield json.dumps(chunk)

            # return {}
        except requests.RequestException as e:
            yield json.dumps(
                {
                    "error": f"Error in invoking model after {self.max_retries} retries: {str(e)}"  # noqa
                }
            )
        except json.JSONDecodeError as e:
            yield json.dumps(
                {"error": f"Error processing response: {str(e)}"},
            )
