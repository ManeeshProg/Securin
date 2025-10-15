import json
import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal, engine, Base
from app.models.recipe import Recipe


def is_nan(value):
    if value is None:
        return True
    if isinstance(value, str) and value.lower() in ['nan', 'null', '','NaN']:
        return True
    return False


def parse_rating(value):
    if is_nan(value):
        return None
    rating = float(value)
    return rating if not math.isnan(rating) else None


def clean_nutrients(nutrients):
    if not nutrients or is_nan(nutrients):
        return None
    if isinstance(nutrients, dict):
        cleaned = {}
        for key, value in nutrients.items():
            if not is_nan(value):
                cleaned[key] = value
        return cleaned if cleaned else None
    return None


def load_recipes_from_json(json_file_path: str, db: Session):
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    total_recipes = len(data)
    loaded_count = 0
    error_count = 0

    for idx, (key, entry) in enumerate(data.items()):
        try:
            recipe = Recipe(
                cuisine=entry.get("cuisine") if not is_nan(entry.get("cuisine")) else None,
                title=entry.get("title") if not is_nan(entry.get("title")) else None,
                rating=parse_rating(entry.get("rating")),
                description=entry.get("description") if not is_nan(entry.get("description")) else None,
                nutrients=clean_nutrients(entry.get("nutrients")),
                serves=entry.get("serves") if not is_nan(entry.get("serves")) else None,
            )

            db.add(recipe)
            loaded_count += 1
            if loaded_count % 100 == 0:
                db.commit()
        except Exception as e:
            error_count += 1
            continue
    db.commit()

    print(f"loaded_count: {loaded_count}")
    print(f"error: {error_count}")
    print(f"{'='*50}")


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    json_file_path="US_recipes_null.json"
    if not Path(json_file_path).exists():
        print(f"Error: JSON file not found at {json_file_path}")
        return
    load_recipes_from_json(json_file_path, db)
    

if __name__ == "__main__":
    main()
