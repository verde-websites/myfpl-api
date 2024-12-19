from functools import lru_cache
from pydantic_settings import BaseSettings

DEVELOPMENT = "development"

class Settings(BaseSettings):
    """Settings for the FastAPI app"""
    build_target: str =  DEVELOPMENT
    database_url: str = "mysql+aiomysql://fplhub:passwordisgod@localhost:3306/fplhub"
    echo_sql: bool = False
    debug_logs: bool = False
    fpl_bootsrap_url: str = "https://fantasy.premierleague.com/api/bootstrap-static/"
    fpl_live_url: str = "https://fantasy.premierleague.com/api/live/"
    fpl_fixtures_url: str = "https://fantasy.premierleague.com/api/fixtures/"
    fpl_players_url: str = "https://fantasy.premierleague.com/api/element-summary/"


    @property
    def is_production(self) -> bool:
        """Check if the build target is production"""
        return self.build_target != DEVELOPMENT

@lru_cache
def get_settings():
    """Get the settings"""
    return Settings()