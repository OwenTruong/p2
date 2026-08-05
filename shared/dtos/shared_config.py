from pydantic import BaseModel, Field

class SharedConfig(BaseModel):
    jwt_secret_key: str = Field()
    jwt_algorithm: str = Field()