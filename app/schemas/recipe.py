from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class RecipeBase(BaseModel):
    cuisine: Optional[str] = None
    title: Optional[str] = None
    rating: Optional[float] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    description: Optional[str] = None
    nutrients: Optional[Dict[str, Any]] = None
    serves: Optional[str] = None


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int

    class Config:
        from_attributes = True


class RecipeResponse(BaseModel):
    id: int
    title: Optional[str] = None
    cuisine: Optional[str] = None
    rating: Optional[float] = None
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    total_time: Optional[int] = None
    description: Optional[str] = None
    nutrients: Optional[Dict[str, Any]] = None
    serves: Optional[str] = None

    class Config:
        from_attributes = True


class RecipePaginatedResponse(BaseModel):
    page: int
    limit: int
    total: int
    data: List[RecipeResponse]
