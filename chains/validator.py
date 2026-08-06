from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from prompts.validator import validator_prompt
from schemas.models import ValidationResult, MealPlan, UserPreferences


class ValidatorChain:
    """Chain validating a MealPlan against user constraints."""

    def __init__(self, llm: ChatOpenAI = None):
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.0)
        self.parser = PydanticOutputParser(pydantic_object=ValidationResult)
        self.chain = validator_prompt | self.llm | self.parser

    def validate(self, meal_plan: MealPlan, preferences: UserPreferences) -> ValidationResult:
        """Validate the meal plan against calorie, dietary, and budget constraints."""
        meal_plan_text = "\n".join(
            f"Day: {meal.day}\nRecipe: {meal.recipe.name}\nCalories: {meal.recipe.calories}\nDietary tags: {', '.join(meal.recipe.dietary_tags)}\nCost: ${meal.recipe.cost:.2f}"
            for meal in meal_plan.meals
        )
        preferences_text = (
            f"Dietary restrictions: {', '.join(preferences.dietary_restrictions) or 'none'}\n"
            f"Cuisine preferences: {', '.join(preferences.cuisine_preferences) or 'none'}\n"
            f"Calorie target: {preferences.calorie_target} per meal\n"
            f"Number of meals per day: {preferences.num_meals}\n"
            f"Budget: ${preferences.budget:.2f}"
        )
        return self.chain.invoke(
            {"meal_plan": meal_plan_text, "user_preferences": preferences_text}
        )
