import json

from google.auth.transport.requests import Request
from google.oauth2 import credentials, service_account

from shared_module.configuration import EnvVar


def sample_fun() -> str:
    """
    This function returns a string.
    """
    return "Hello, World!"


def get_service_account_credentials() -> service_account.Credentials:
    """Obtain service account credentials."""
    print(EnvVar.gcp_service_account)
    return service_account.Credentials.from_service_account_info(
        info=json.loads(EnvVar.gcp_service_account),
    )


def main() -> None:
    account_credentials = get_service_account_credentials()
    print(account_credentials)
    print(EnvVar.openai_api_key)


if __name__ == "__main__":
    main()
