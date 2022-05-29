from pathlib import Path

from dynaconf import Dynaconf

THIS_DIR = Path(__file__).resolve(strict=True).parent

settings = Dynaconf(
    envvar_prefix=False,
    root_path=THIS_DIR,
    settings_files=["settings.toml", "config.py"],
    secrets="secrets.toml",
    environments=True,
    load_dotenv=True,
    env_switcher="DREAMJOB_ENV",
)
