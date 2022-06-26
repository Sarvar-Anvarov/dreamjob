from typing import List
from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    user_input: str


class Recommendation(BaseModel):
    id: int


class Recommendations(BaseModel):
    recommendations: List[Recommendation] = []
