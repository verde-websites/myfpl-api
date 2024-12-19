from pydantic import BaseModel, ConfigDict

class GetSeasonResponse(BaseModel):
    id: int
    season_name: str
    model_config: ConfigDict = ConfigDict(from_attributes=True)

class PostSeasons(BaseModel):
    season_name: str
