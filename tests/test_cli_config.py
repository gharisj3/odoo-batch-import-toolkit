from pathlib import Path

from odoo_batch_import.cli import main
from odoo_batch_import.config import load_config


def test_load_config_from_env_file(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text("POSTGRES_PORT=15432\nIMPORT_BATCH_SIZE=500\nIMPORT_DRY_RUN=false\n", encoding="utf-8")

    config = load_config(env_file=str(env_file))

    assert config.postgres.port == 15432
    assert config.import_defaults.batch_size == 500
    assert config.import_defaults.dry_run is False


def test_cli_validate_success(tmp_path: Path, capsys):
    csv_file = tmp_path / "sample.csv"
    csv_file.write_text("name,email\nAlice,alice@example.com\n", encoding="utf-8")

    exit_code = main(["--env-file", "", "validate", "--file", str(csv_file), "--required", "name", "email"])

    assert exit_code == 0
    assert "CSV validation passed." in capsys.readouterr().out
