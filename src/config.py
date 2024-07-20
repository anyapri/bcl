import os
from functools import lru_cache
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseSettings


class Settings(BaseSettings):
    # database
    s3_config: dict = {}

    request_access_token: str = ""
    rb_access_token: str = ""
    rb_environment: str = ""
    rb_code_version: str = ""
    service_obfuscation: bool = False
    healthcheck_up_path: str = "healthcheck/up.json"

    log_dir: str = "logs"
    log_max_size: int = 1
    debug: bool = True
    log_counts: int = 10


@lru_cache()
def get_settings():
    return Settings()


def read_secrets(
    client: object,
    read_mount_point: str,
    relative_path: str,
) -> Settings:
    """
    Fill Settings from Vault and file secretes

    Parameters
    ----------
    client: object
        Vault Client instance
    read_mount_point: str
        kv name in Vault secret storage
    relative_path: str
        relative path for target machine's secret in kv storage

    Returns
    -------
        Settings instance
    """
    secrets_loaded = {"common": False, "s3": False, "rollbar": False}

    settings = Settings()

    # loading vault secrets
    folders = client.secrets.kv.v2.list_secrets(
        path=relative_path, mount_point=read_mount_point
    )["data"]["keys"]

    for folder in folders:
        secrets = client.read(
            os.path.join(read_mount_point, "data", relative_path, folder)
        )["data"]["data"]
        if folder == "common":
            try:
                settings.request_access_token = secrets["REQUEST_ACCESS_TOKEN"]
                secrets_loaded[folder] = True
            except Exception as err:
                raise KeyError(f"Error loading secrets '{folder}' from vault.")
        elif folder == "s3":
            try:
                settings.s3_config = {
                    "minio_access_key": secrets["MINIO_ACCESS_KEY"],
                    "minio_api_host": secrets["MINIO_API_HOST"],
                    "minio_secret_key": secrets["MINIO_SECRET_KEY"],
                    "model_bucket_name": secrets["MODEL_BUCKET_NAME"],
                    "model_object_name": secrets["MODEL_OBJECT_NAME"]
                                    }
                secrets_loaded[folder] = True
            except Exception as err:
                raise KeyError(f"Error loading secrets '{folder}' from vault.")
            
        elif folder == "rollbar":
            try:
                settings.rb_access_token = secrets["ACCESS_TOKEN"]
                settings.rb_environment = secrets["ACCESS_ENVIRONMENT"]
                settings.rb_code_version = secrets["ACCESS_CODE_VERSION"]
                secrets_loaded[folder] = True
            except Exception as err:
                raise KeyError(f"Error loading secrets '{folder}' from vault.")

    # check vault secrets
    for secret_name, is_correct_loaded in secrets_loaded.items():
        if is_correct_loaded is False:
            raise KeyError(f"No secrets are defined in vault for '{secret_name}'.")

    return settings