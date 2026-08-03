from pydantic import BaseModel, Field

class DBConfig(BaseModel):
  db_host: str = Field(examples=["localhost"])
  db_name: str = Field(examples=["my_db"])
  db_user: str = Field(examples=["my_db_user"])
  db_password: str = Field(examples=["MyVeryImportantPassword"])
  db_port: int = Field(examples=[5432])