from pydantic import BaseModel


class Settings(BaseModel):
    width: int = 800
    height: int = 800


settings = Settings()
