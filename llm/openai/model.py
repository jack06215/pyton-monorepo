from typing import Any

from pydantic import BaseModel


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

    def to_function_definition(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "strict": self.strict,
        }
