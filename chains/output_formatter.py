from typing import Dict, List
from schemas.models import MealPlan, GroceryList
from tools.aisle_mapper import AisleMappingTool


class OutputFormatter:
    """Formats the approved meal plan as a calendar and aisle-grouped grocery list."""

    def __init__(self, aisle_mapper: AisleMappingTool = None):
        self.aisle_mapper = aisle_mapper or AisleMappingTool()

    def group_by_aisle(self, grocery_list: GroceryList) -> Dict[str, List]:
        """Group grocery items by aisle using the aisle mapper."""
        grouped: Dict[str, List] = {}
        for item in grocery_list.items:
            aisle = self.aisle_mapper.map_item(item.name)
            if aisle not in grouped:
                grouped[aisle] = []
            grouped[aisle].append(item)
        return grouped

    def format_calendar(self, meal_plan: MealPlan) -> str:
        """Render each day with its recipe name."""
        lines = ["Meal Plan Calendar", "==================="]
        for meal in meal_plan.meals:
            tags = ", ".join(meal.recipe.dietary_tags) if meal.recipe.dietary_tags else "none"
            lines.append(f"{meal.day}: {meal.recipe.name} ({tags})")
        return "\n".join(lines)

    def format_grocery_list(self, grocery_list: GroceryList) -> str:
        """Render items grouped by aisle with needed/owned flags."""
        grouped = self.group_by_aisle(grocery_list)
        lines = ["Grocery List (by Aisle)", "========================"]
        for aisle in sorted(grouped.keys()):
            lines.append(f"\n{aisle}:")
            for item in grouped[aisle]:
                status = "Owned" if item.owned else "Buy"
                lines.append(f"  - {item.name} ({item.quantity}) [{status}]")
        return "\n".join(lines)

    def render(self, meal_plan: MealPlan, grocery_list: GroceryList) -> str:
        """Combine both into a single human-readable string."""
        calendar = self.format_calendar(meal_plan)
        grocery = self.format_grocery_list(grocery_list)
        return f"{calendar}\n\n{grocery}"
