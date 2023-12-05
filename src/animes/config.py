from pydantic_settings import BaseSettings


class AnimeConfig(BaseSettings):
    MAL_API_KEY: str = "3f177ff492d95a505a2cdf5c3b3b3a29"


anime_config = AnimeConfig()
