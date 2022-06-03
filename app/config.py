from pydantic import BaseSettings


class Settings(BaseSettings):
    Database_Hostname: str
    Database_Name: str
    Database_Username: str
    Database_Port: str
    Database_Password: str
    Secret_Key: str
    Algorithm: str
    Access_Token_Expire_Minutes: str

    class Config:
        env_file = ".env"


settings = Settings()
