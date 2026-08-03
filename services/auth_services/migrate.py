from pathlib import Path
from yoyo import get_backend, read_migrations

from .app.core.config import get_config

# See https://ollycope.com/software/yoyo/latest/#calling-yoyo-from-python-code

config = get_config()

def build_dsn() -> str:
    user = config.db_user
    password = config.db_password
    # host and port depends on where yoyo is being run on
    host = "localhost" # TODO: make it useful for production too
    port = config.db_port
    name = config.db_name
    connection_url = f"postgresql://{user}:{password}@{host}:{port}/{name}"
    return connection_url

def migrate() -> None:
    backend = get_backend(build_dsn())
    migration_dir = Path(__file__).parent / "migrations"
    migrations = read_migrations(str(migration_dir))
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

if __name__ == '__main__':
    migrate()