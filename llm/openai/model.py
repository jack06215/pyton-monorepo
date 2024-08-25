import json
from abc import abstractmethod
from typing import Any, ClassVar, Literal, cast

from openai.types.chat import (
    ChatCompletionNamedToolChoiceParam,
    ChatCompletionToolChoiceOptionParam,
    ChatCompletionToolParam,
)
from openai.types.shared_params import FunctionDefinition
from pydantic import BaseModel, Field, field_validator


class BaseFunctionModel(BaseModel):
    @classmethod
    def model_json_schema(cls, *args, **kwargs) -> dict[str, Any]:
        schema = super().model_json_schema(*args, **kwargs)
        schema.pop("description", None)
        schema.pop("title", None)
        schema["additionalProperties"] = False
        for prop in schema.get("properties", {}).values():
            prop.pop("title", None)
            prop["additionalProperties"] = False

        return schema


class FunctionCallModel(BaseModel):
    name: str
    description: str
    parameters: dict[str, Any]
    strict: bool = True

    def to_function_definition(self) -> FunctionDefinition:
        return FunctionDefinition(
            name=cast(str, self.name),
            description=cast(str, self.description),
            parameters=self.model_json_schema(),
            strict=True,
        )


# class WeatherTemperature(FunctionCallModel):
#     name: ClassVar[str] = "weather_temperature"
#     description: ClassVar[str] = "Get the current temperature for a given location."
#     temperature: float = Field(description="The temperature in degrees Celsius.")


# get_weather_temperature = WeatherTemperature
# print(json.dumps(get_weather_temperature.to_function_definition(), indent=2))
