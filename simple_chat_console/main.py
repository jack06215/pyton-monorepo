import asyncio
import json
from datetime import datetime
from typing import ClassVar, cast

from pydantic import BaseModel, Field

from llm.openai.model import BaseFunctionModel, FunctionCallModel
from llm.openai.openai import OpenAIModel
from shared_module.prompt_template import simple_prompt


class GetCapitalCityFunction(BaseFunctionModel):
    capital_city: str = Field(
        description="The capital city of the given country, in UPPERCASE."
    )


async def main() -> None:
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
        model="gpt-3.5-turbo",
        temperature=0,
        json_response=True,
    )
    tools = [
        FunctionCallModel(
            name="get_capital_city",
            description="Get the capital city of a given country.",
            parameters=GetCapitalCityFunction.model_json_schema(),
        ),
    ]

    response = model.invoke(
        messages,
        tools=list(map(lambda x: cast(BaseModel, x), tools)),
        tool_choice="auto",
    )
    print(response)


if __name__ == "__main__":
    # print(GetCapitalCityFunction.model_json_schema())
    asyncio.run(main())
