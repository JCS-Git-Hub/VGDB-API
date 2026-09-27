from pydantic import BaseModel, ConfigDict, Field

from backend.schema.schema_category import CategoryResponse


class GameBase(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    developer: str = Field(min_length=2, max_length=120)
    release_year: int = Field(ge=1947, le=2030)
    category_id: int = Field(gt=0)


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass


class GameResponse(GameBase):
    id: int
    category: CategoryResponse

    model_config = ConfigDict(from_attributes=True)