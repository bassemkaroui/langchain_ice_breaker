from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    proxycurl_api_key: SecretStr
    openai_api_key: SecretStr
    tavily_api_key: SecretStr
    twitter_api_key: SecretStr
    twitter_api_key_secret: SecretStr
    twitter_bearer_token: SecretStr
    twitter_access_token: SecretStr
    twitter_access_token_secret: SecretStr

    # langchain_tracing_v2: bool
    # langchain_endpoint: HttpUrl
    # langchain_api_key: SecretStr
    # langchain_project: str
