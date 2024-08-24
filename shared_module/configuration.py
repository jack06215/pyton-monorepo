import os

from dotenv import load_dotenv
from pydantic import BaseModel


def get_env_or_throw(
    env_var_name: str,
    default_value: str | None = None,
) -> str:
    value = os.getenv(env_var_name, default_value)
    if value is None:
        raise ValueError(f"Environment variable '{env_var_name}' not found.")
    return value


class EnvironmentVariable(BaseModel):
    openai_api_key: str
    gcp_service_account: str

    @classmethod
    def from_dotev(cls) -> "EnvironmentVariable":
        load_dotenv()
        return cls(
            openai_api_key=get_env_or_throw("OPENAI_API_KEY"),
            gcp_service_account=get_env_or_throw("GCP_SERVICE_ACCOUNT_JSON"),
        )


EnvVar = EnvironmentVariable.from_dotev()
