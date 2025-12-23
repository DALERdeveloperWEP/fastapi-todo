from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_pass: str
    db_name: str
    db_user: str
    
    jwt_secret: str
    jwt_algorithm: str

    model_config = SettingsConfigDict(env_file='.env')

settings = Settings()
 
