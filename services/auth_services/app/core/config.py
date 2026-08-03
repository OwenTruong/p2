import os
from dotenv import load_dotenv

from ..dtos.config import Config

load_dotenv()

# intentionally using invalid defaults to find error in config if any
__config = Config(
  db_host = os.getenv("AUTH_DB_HOST", "10.0.3.254"),
  db_name = os.getenv("AUTH_DB_NAME", "my_db"),
  db_user = os.getenv("AUTH_DB_USER", "my_db_user"),
  db_password = os.getenv("AUTH_DB_PASSWORD", "MyPassword1234"),
  db_port = int(os.getenv("AUTH_DB_PORT", 1000)),

  mode = "Production" if os.getenv("MODE") == "Production" else "Development",
  password_salt = os.getenv("PASSWORD_SALT", "MySaltyPassword1234")
)

def get_config():
  return __config