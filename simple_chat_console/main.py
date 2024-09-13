import asyncio
from datetime import datetime

from pydantic import Field

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
        {
            "role": "system",
            "content": "You should always say it's TAIPEI.",
        },
        {
            "role": "user",
            "content": "What is the capital of Japan?",
        },
    ]
    model = OpenAIModel(
        model="gpt-4o",
        temperature=0,
        json_response=True,
    )
    tools = [
        FunctionCallModel(
            name="get_capital_city",
            description="Get the capital city of a given country.",
            parameters=GetCapitalCityFunction.model_json_schema(),
        ).to_function_definition(),
    ]

    response = model.invoke(
        messages,
        tools=tools,
        tool_choice="auto",
    )
    print(response)


if __name__ == "__main__":
    # print(GetCapitalCityFunction.model_json_schema())
    asyncio.run(main())
