"""Environment-backed configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _load_env_file(path: str) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ[key.strip()] = value.strip().strip('"').strip("'")


@dataclass(frozen=True)
class PostgresConfig:
    host: str
    port: int
    dbname: str
    user: str
    password: str
    sslmode: str = "prefer"

    def dsn(self) -> str:
        return (
            f"host={self.host} port={self.port} dbname={self.dbname} "
            f"user={self.user} password={self.password} sslmode={self.sslmode}"
        )


@dataclass(frozen=True)
class OdooConfig:
    base_url: str
    database: str
    username: str
    password: str


@dataclass(frozen=True)
class ImportConfig:
    batch_size: int
    dry_run: bool


@dataclass(frozen=True)
class AppConfig:
    postgres: PostgresConfig
    odoo: OdooConfig
    import_defaults: ImportConfig


def load_config(*, env_file: str | None = ".env") -> AppConfig:
    if load_dotenv and env_file:
        load_dotenv(env_file, override=True)
    elif env_file:
        _load_env_file(env_file)
    return AppConfig(
        postgres=PostgresConfig(
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=int(os.getenv("POSTGRES_PORT", "5432")),
            dbname=os.getenv("POSTGRES_DB", "odoo"),
            user=os.getenv("POSTGRES_USER", "odoo"),
            password=os.getenv("POSTGRES_PASSWORD", ""),
            sslmode=os.getenv("POSTGRES_SSLMODE", "prefer"),
        ),
        odoo=OdooConfig(
            base_url=os.getenv("ODOO_BASE_URL", "http://localhost:8069"),
            database=os.getenv("ODOO_DATABASE", ""),
            username=os.getenv("ODOO_USERNAME", ""),
            password=os.getenv("ODOO_PASSWORD", ""),
        ),
        import_defaults=ImportConfig(
            batch_size=int(os.getenv("IMPORT_BATCH_SIZE", "1000")),
            dry_run=_as_bool(os.getenv("IMPORT_DRY_RUN"), default=True),
        ),
    )
