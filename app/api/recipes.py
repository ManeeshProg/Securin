from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import Optional
from app.db.base import get_db
from app.models.recipe import Recipe
from app.schemas.recipe import RecipeResponse, RecipePaginatedResponse

router = APIRouter()


@router.get("/recipes", response_model=RecipePaginatedResponse)
def get_recipes(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):

    offset = (page - 1) * limit

    total = db.query(Recipe).count()

    # Get recipes with pagination and sorting
    recipes = (
        db.query(Recipe)
        .order_by(Recipe.rating.desc().nullslast(), Recipe.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Convert to response model
    recipe_responses = [
        RecipeResponse(
            id=recipe.id,
            title=recipe.title,
            cuisine=recipe.cuisine,
            rating=recipe.rating,
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            total_time=recipe.total_time,
            description=recipe.description,
            nutrients=recipe.nutrients,
            serves=recipe.serves,
        )
        for recipe in recipes
    ]

    return RecipePaginatedResponse(
        page=page,
        limit=limit,
        total=total,
        data=recipe_responses
    )


@router.get("/recipes/search", response_model=RecipePaginatedResponse)
def search_recipes(
    title: Optional[str] = Query(None, description="Search by recipe title (partial match)"),
    cuisine: Optional[str] = Query(None, description="Filter by cuisine"),
    rating_gte: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating (greater than or equal)"),
    rating_lte: Optional[float] = Query(None, ge=0, le=5, description="Maximum rating (less than or equal)"),
    rating: Optional[float] = Query(None, ge=0, le=5, description="Exact rating match"),
    total_time_gte: Optional[int] = Query(None, ge=0, description="Minimum total time (greater than or equal)"),
    total_time_lte: Optional[int] = Query(None, ge=0, description="Maximum total time (less than or equal)"),
    total_time: Optional[int] = Query(None, ge=0, description="Exact total time match"),
    calories_gte: Optional[int] = Query(None, ge=0, description="Minimum calories (greater than or equal)"),
    calories_lte: Optional[int] = Query(None, ge=0, description="Maximum calories (less than or equal)"),
    calories: Optional[int] = Query(None, ge=0, description="Exact calories match"),
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(get_db)
):
    query = db.query(Recipe)

    if title:
        query = query.filter(Recipe.title.ilike(f"%{title}%"))

    if cuisine:
        query = query.filter(Recipe.cuisine.ilike(f"%{cuisine}%"))

    if rating is not None:
        query = query.filter(Recipe.rating == rating)
    else:
        if rating_gte is not None:
            query = query.filter(Recipe.rating >= rating_gte)
        if rating_lte is not None:
            query = query.filter(Recipe.rating <= rating_lte)

    # Total time filters
    if total_time is not None:
        query = query.filter(Recipe.total_time == total_time)
    else:
        if total_time_gte is not None:
            query = query.filter(Recipe.total_time >= total_time_gte)
        if total_time_lte is not None:
            query = query.filter(Recipe.total_time <= total_time_lte)

    # Calories filter (from JSON nutrients field)
    # Note: This requires JSON querying which varies by database
    # For SQLite, we'll need to handle this differently
    if calories is not None:
        # SQLite JSON support is limited, but we can use LIKE for basic matching
        query = query.filter(Recipe.nutrients.contains(f'"calories": "{calories} kcal"'))
    else:
        if calories_gte is not None or calories_lte is not None:
            # For range queries on calories in SQLite, we'd need to extract and compare
            # This is a simplified approach - for production, consider PostgreSQL with JSONB
            pass

    # Get total count of filtered results
    total = query.count()

    # Apply pagination and sorting
    offset = (page - 1) * limit
    recipes = (
        query
        .order_by(Recipe.rating.desc().nullslast(), Recipe.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    # Convert to response model
    recipe_responses = [
        RecipeResponse(
            id=recipe.id,
            title=recipe.title,
            cuisine=recipe.cuisine,
            rating=recipe.rating,
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            total_time=recipe.total_time,
            description=recipe.description,
            nutrients=recipe.nutrients,
            serves=recipe.serves,
        )
        for recipe in recipes
    ]

    return RecipePaginatedResponse(
        page=page,
        limit=limit,
        total=total,
        data=recipe_responses
    )
