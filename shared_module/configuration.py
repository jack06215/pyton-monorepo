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
    gcp_client_secret_desktop: str

    @classmethod
    def from_dotenv(cls) -> "EnvironmentVariable":
        load_dotenv()
        return cls(
            openai_api_key=get_env_or_throw("OPENAI_API_KEY"),
            gcp_service_account=get_env_or_throw("GCP_SERVICE_ACCOUNT_JSON"),
            gcp_client_secret_desktop=get_env_or_throw("GCP_CLIENT_SECRET_DESKTOP_APP"),
        )


EnvVar = EnvironmentVariable.from_dotenv()
