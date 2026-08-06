from pydantic import BaseModel, Field
from typing import List, Optional


class UserPreferences(BaseModel):
    dietary_restrictions: List[str]
    cuisine_preferences: List[str]
    calorie_target: int
    num_meals: int
    budget: float


class PantryItem(BaseModel):
    name: str
    quantity: float
    unit: str


class PantryInventory(BaseModel):
    items: List[PantryItem]


class Recipe(BaseModel):
    id: str
    name: str
    ingredients: List[str]
    calories: int
    dietary_tags: List[str]
    cost: float
    aisle: str
    instructions: str


class Meal(BaseModel):
    day: str
    recipe: Recipe


class MealPlan(BaseModel):
    meals: List[Meal]


class GroceryItem(BaseModel):
    name: str
    quantity: float
    needed: bool
    owned: bool


class GroceryList(BaseModel):
    items: List[GroceryItem]


class ValidationResult(BaseModel):
    passed: bool
    reasons: List[str]
