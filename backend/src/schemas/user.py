from pydantic_settings import BaseSettings, SettingsConfigDict


class CLIUser(BaseSettings):
    model_config = SettingsConfigDict(cli_parse_args=True)

    full_name: str = "Bassem Karoui"
