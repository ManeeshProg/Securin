from sqlalchemy import Column, Integer, String, Float, Text, JSON
from app.db.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cuisine = Column(String(255), index=True, nullable=True)
    title = Column(String(500), index=True, nullable=True)
    rating = Column(Float, index=True, nullable=True)
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    total_time = Column(Integer, index=True, nullable=True)
    description = Column(Text, nullable=True)
    nutrients = Column(JSON, nullable=True)  # JSONB in PostgreSQL
    serves = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<Recipe(id={self.id}, title='{self.title}', cuisine='{self.cuisine}')>"
