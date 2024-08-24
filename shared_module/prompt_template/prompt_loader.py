import os

_current_directory = os.path.dirname(os.path.abspath(__file__))


def read_markdown_file(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return ""
    except IOError:
        print(f"Error: Unable to read file at {file_path}")
        return ""


def simple_prompt():
    return read_markdown_file(
        os.path.join(
            _current_directory,
            "simple_prompt.md",
        )
    )
