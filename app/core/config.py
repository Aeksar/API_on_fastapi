from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    
    SECRET_KEY: str
    ALGORITHM: str
    ACCECESS_TOKEN_EXPRICE_MINUTES: int
    
    @property
    def ASYNC_DATABASE_URL(self):
        return f"postgres+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
     
        
settings = Settings()