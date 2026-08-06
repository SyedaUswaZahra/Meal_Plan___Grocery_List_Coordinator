from typing import List, Optional
from dataclasses import dataclass, field
from schemas.models import UserPreferences, PantryInventory, Recipe, MealPlan, ValidationResult, GroceryList


@dataclass
class GraphState:
    """Typed state schema shared across all LangGraph nodes."""

    user_input: Optional[str] = None
    preferences: Optional[UserPreferences] = None
    pantry_text: Optional[str] = None
    pantry: Optional[PantryInventory] = None
    candidate_recipes: List[Recipe] = field(default_factory=list)
    meal_plan: Optional[MealPlan] = None
    validation: Optional[ValidationResult] = None
    grocery_list: Optional[GroceryList] = None
    final_output: Optional[str] = None
    error: Optional[str] = None
