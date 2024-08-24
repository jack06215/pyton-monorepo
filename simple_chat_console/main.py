from datetime import datetime

from llm.openai.openai import OpenAIModel
from shared_module.prompt_template import simple_prompt


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
        model="gpt-3.5-turbo",
        temperature=0,
    )
    response = model.invoke(messages)
    print(response)


if __name__ == "__main__":
    main()
