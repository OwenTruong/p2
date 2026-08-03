import os
from dotenv import load_dotenv
import logging

from ..dtos.config import Config

load_dotenv()

# intentionally using invalid defaults to find error in config if any
__config = Config(
  db_host = os.getenv("DB_HOST", "10.0.3.254"),
  db_name = os.getenv("AUTH_DB_NAME", "my_db"),
  db_user = os.getenv("DB_USER", "my_db_user"),
  db_password = os.getenv("DB_PASSWORD", "MyPassword1234"),
  db_port = int(os.getenv("DB_PORT", 1000)),

  mode = "Production" if os.getenv("MODE") == "Production" else "Development",
  password_salt = os.getenv("PASSWORD_SALT", "MySaltyPassword1234")
)

logging.debug(f"""Config Loaded:
  db_host: {__config.db_host}
  db_name: {__config.db_name}
  db_user: {__config.db_user}
  db_password: REDACTED
  db_port: {__config.db_port}

  mode: {__config.mode}
  password_salt: REDACTED
""")


def get_config():
  return __config