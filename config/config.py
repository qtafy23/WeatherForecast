"""Config for manager settings"""
from dynaconf import DjangoDynaconf

settings = DjangoDynaconf(
    envvar_prefix=False,
    core_loaders=['TOML'],
    settings_files=['config/settings.toml', 'config/.secrets.toml'],
)
