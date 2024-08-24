import json
from datetime import datetime
from typing import ClassVar

from pydantic import Field

from llm.openai.model import FunctionCallModel
from llm.openai.openai import OpenAIModel
from shared_module.prompt_template import simple_prompt


class GetCapitalCityFunction(FunctionCallModel):
    name: ClassVar[str] = "get_capital_city"
    description: ClassVar[str] = "Get the capital city of a given country."
    capital_city: float = Field(
        description="The capital city of the given country, in UPPERCASE."
    )


def main() -> None:
    system_prompt = simple_prompt()
    messages = [
        {
            "role": "system",
            "content": f"{system_prompt}\n Today's date is {datetime.now()}",
        },
        {
            "role": "user",
            "content": "What is the capital of Japan?",
        },
    ]
    model = OpenAIModel(
        model="gpt-4o",
        temperature=0,
    )

    response = model.invoke(
        messages,
        tools=[
            GetCapitalCityFunction.openai_function_tool_schema(),
        ],
        tool_choice="auto",
    )
    print(response)


if __name__ == "__main__":
    main()
