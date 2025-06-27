from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_NAME: str
    GOOGLE_API_KEY: str
    GEMINI_MODEL: str 
    THINKING_BUDGET: int = 4000
    batch_size:int
    callback_url:str

    class Config:
        env_file = "/home/fariq.rahman/work/Coaching/Auto_Coaching/.env"

settings = Settings()
