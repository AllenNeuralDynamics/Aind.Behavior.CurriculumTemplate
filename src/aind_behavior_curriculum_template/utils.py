import os
import pathlib
import typing

from pydantic import BaseModel, Field, RootModel
from pydantic_settings import (
    BaseSettings,
    CliImplicitFlag,
    CliSubCommand,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)

TModel = typing.TypeVar("TModel", bound=BaseModel)


def model_from_json_file(json_path: os.PathLike | str, model: type[TModel]) -> TModel:
    with open(pathlib.Path(json_path), "r", encoding="utf-8") as file:
        return model.model_validate_json(file.read())


class CurriculumCliArgs(BaseSettings):
    model_config = SettingsConfigDict(yaml_file=["./curriculum_default.yml", "./local/curriculum_custom.yml"])

    data_directory: os.PathLike = Field(description="Path to the session data directory.")
    input_trainer_state: os.PathLike = Field(description="Path to a deserializable trainer state.")
    mute_trainer_state: CliImplicitFlag[bool] = Field(
        default=False, description="Disables the output of the TrainerState suggestion"
    )
    mute_metrics: CliImplicitFlag[bool] = Field(
        default=False, description="Disables the output of the calculated metrics"
    )
    output_metrics: typing.Optional[os.PathLike] = Field(
        default=None,
        description="A path to save the used metrics. If not provided, the metrics will not be serialized to a file.",
    )
    output_suggestion: typing.Optional[os.PathLike] = Field(
        default=None,
        description="A path to save the suggestion. If not provided, the suggestion will not be serialized to a file.",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: typing.Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> typing.Tuple[PydanticBaseSettingsSource, ...]:
        """
        Customizes the order of settings sources for the CLI.

        Args:
            settings_cls (Type[BaseSettings]): The settings class.
            init_settings (PydanticBaseSettingsSource): Initial settings source.
            env_settings (PydanticBaseSettingsSource): Environment variable settings source.
            dotenv_settings (PydanticBaseSettingsSource): Dotenv settings source.
            file_secret_settings (PydanticBaseSettingsSource): File secret settings source.

        Returns:
            Tuple[PydanticBaseSettingsSource, ...]: Ordered tuple of settings sources.
        """
        return (init_settings, YamlConfigSettingsSource(settings_cls))


class _AnyRoot(RootModel):
    root: typing.Any


class AppCliArgs(BaseSettings, cli_prog_name="curriculum", cli_kebab_case=True):
    run: CliSubCommand[CurriculumCliArgs]
    version: CliSubCommand[_AnyRoot]
    abc_version: CliSubCommand[_AnyRoot]
