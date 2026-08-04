from pathlib import Path
from yoyo import get_backend, read_migrations

from .core.config import get_config

# See https://ollycope.com/software/yoyo/latest/#calling-yoyo-from-python-code

config = get_config()

def get_migration_dir() -> Path:
    """
    Resolve the migrations directory relative to this source file,
    independent of the process's current working directory.
    """
    service_root = Path(__file__).resolve().parent.parent
    migration_dir = service_root / "migrations"

    if not migration_dir.exists():
        raise FileNotFoundError(
            f"Migration directory does not exist: {migration_dir}"
        )

    if not migration_dir.is_dir():
        raise NotADirectoryError(
            f"Migration path is not a directory: {migration_dir}"
        )

    return migration_dir

def build_dsn() -> str:
    user = config.db_user
    password = config.db_password
    # host and port depends on where yoyo is being run on
    host = config.db_host # TODO: make it useful for production too
    port = config.db_port
    name = config.db_name
    connection_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    return connection_url

def migrate() -> None:
    backend = get_backend(build_dsn())
    migration_dir = get_migration_dir()
    migrations = read_migrations(str(migration_dir))
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

if __name__ == '__main__':
    migrate()