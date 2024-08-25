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


class FunctionCallModel(BaseModel):
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

    @property
    @abstractmethod
    def name(self) -> str:
        """The name of the function to be called."""
        raise NotImplementedError

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what the function does."""
        raise NotImplementedError

    # @field_validator("name", "description", mode="before")
    # @classmethod
    # def abstract_property_must_be_overridden(cls, value: str) -> str:
    #     if value is None:
    #         raise ValueError("Property must be overridden.")

    #     return value

    @classmethod
    def to_function_definition_dict(cls) -> dict[str, Any]:
        return dict(
            name=cast(str, cls.name),
            description=cast(str, cls.description),
            parameters=cls.model_json_schema(),
            strict=True,
        )

    @classmethod
    def to_function_definition(cls) -> FunctionDefinition:
        return FunctionDefinition(
            name=cast(str, cls.name),
            description=cast(str, cls.description),
            parameters=cls.model_json_schema(),
            strict=True,
        )


# class WeatherTemperature(FunctionCallModel):
#     name: ClassVar[str] = "weather_temperature"
#     description: ClassVar[str] = "Get the current temperature for a given location."
#     temperature: float = Field(description="The temperature in degrees Celsius.")


# get_weather_temperature = WeatherTemperature
# print(json.dumps(get_weather_temperature.to_function_definition(), indent=2))
