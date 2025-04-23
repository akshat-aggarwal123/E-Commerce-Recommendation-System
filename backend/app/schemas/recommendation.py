from pydantic import BaseModel
from typing import List, Optional

class Recommendation(BaseModel):
    Product_ID: str
    Category: str
    Subcategory: str
    Price: float
    Brand: str
    Ratings: float
    Recommendation_Score: float