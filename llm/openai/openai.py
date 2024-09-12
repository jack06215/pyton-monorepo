import json
from dataclasses import asdict
from typing import Any, cast

import requests
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel

from llm.base import BaseChatModel
from llm.openai.model import FunctionCallModel
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
        tools: list[dict[str, Any]] | list[BaseModel] | None = None,
        tool_choice: str = "none",
    ) -> Any:
        # print(tools)
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
            elif isinstance(tools[0], BaseModel):
                payload["tools"] = [
                    {
                        "type": "function",
                        "function": tool.model_dump(exclude={"title"}),
                    }
                    for tool in cast(list[BaseModel], tools)
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
                    "error": f"Error in invoking model after {self.max_retries} retries: {str(e)}"
                }
            )
        except json.JSONDecodeError as e:
            return json.dumps(
                {"error": f"Error processing response: {str(e)}"},
            )

    async def ainvoke(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | list[BaseModel] | None = None,
        tool_choice: str = "none",
    ) -> Any:
        system = messages[0]["content"]
        user = messages[1]["content"]

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
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
            elif isinstance(tools[0], BaseModel):
                payload["tools"] = [
                    {
                        "type": "function",
                        "function": tool.model_dump(exclude={"title"}),
                    }
                    for tool in cast(list[BaseModel], tools)
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
                    "error": f"Error in invoking model after {self.max_retries} retries: {str(e)}"
                }
            )
        except json.JSONDecodeError as e:
            yield json.dumps(
                {"error": f"Error processing response: {str(e)}"},
            )
