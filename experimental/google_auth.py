import json
import os

from google.auth.transport.requests import Request
from google.oauth2 import credentials, service_account
from google_auth_oauthlib.flow import InstalledAppFlow

from definition import PROJECT_ROOT
from shared_module.configuration import EnvVar

_SCOPES = [
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


def get_service_account_credentials() -> service_account.Credentials:
    """Obtain service account credentials."""
    print(EnvVar.gcp_service_account)
    return service_account.Credentials.from_service_account_info(
        info=json.loads(EnvVar.gcp_service_account),
        scopes=_SCOPES,
    )


def get_user_credentials() -> credentials.Credentials:
    """Obtain user credentials."""
    credential = None
    credential_file_path = os.path.join(
        PROJECT_ROOT,
        "secret",
        "token.json",
    )
    if os.path.exists(credential_file_path):
        credential = credentials.Credentials.from_authorized_user_file(
            credential_file_path,
            scopes=_SCOPES,
        )
    if not credential or not credential.valid:
        if credential and credential.expired and credential.refresh_token:
            credential.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                json.loads(EnvVar.gcp_client_secret_desktop),
                scopes=_SCOPES,
            )
            credential = flow.run_local_server(port=0)
            with open(credential_file_path, "w") as token:
                token.write(credential.to_json())

    return credential


def main() -> None:
    account_credentials = get_user_credentials()
    print(account_credentials.token)
    print(EnvVar.openai_api_key)


if __name__ == "__main__":
    main()
