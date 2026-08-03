import os
from dotenv import load_dotenv
from yoyo import get_backend, read_migrations

from .app.core.config import get_config

# See https://ollycope.com/software/yoyo/latest/#calling-yoyo-from-python-code

load_dotenv()
config = get_config()

def build_dsn() -> str:
    user = config.db_user
    password = config.db_password
    # host and port depends on where yoyo is being run on
    host = "localhost"
    port = config.db_port
    name = config.db_name
    return f"postgresql://{user}:{password}@{host}:{port}/{name}"

def migrate() -> None:
    backend = get_backend(build_dsn())
    migrations = read_migrations("./migrations")
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

if __name__ == '__main__':
    migrate()