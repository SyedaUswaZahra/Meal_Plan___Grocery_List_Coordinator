from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from prompts.consolidator import consolidator_prompt
from schemas.models import GroceryList, MealPlan, PantryInventory


class ConsolidatorChain:
    """Chain consolidating recipe ingredients into a grocery list."""

    def __init__(self, llm: ChatOpenAI = None):
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.0)
        self.parser = PydanticOutputParser(pydantic_object=GroceryList)
        self.chain = consolidator_prompt | self.llm | self.parser

    def consolidate(self, meal_plan: MealPlan, pantry: PantryInventory) -> GroceryList:
        """Merge ingredients, subtract pantry quantities, flag owned items, and return the list."""
        meal_plan_text = "\n".join(
            f"Day: {meal.day}\nRecipe: {meal.recipe.name}\nIngredients: {', '.join(meal.recipe.ingredients)}"
            for meal in meal_plan.meals
        )
        pantry_text = "\n".join(f"- {item.name}: {item.quantity} {item.unit}" for item in pantry.items)
        return self.chain.invoke(
            {"meal_plan": meal_plan_text, "pantry_inventory": pantry_text}
        )
