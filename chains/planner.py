from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from prompts.planner import planner_prompt
from schemas.models import MealPlan, PantryInventory, UserPreferences, Recipe
from tools.recipe_retriever import RecipeRetriever


class PlannerChain:
    """Chain generating a MealPlan from retrieved recipes and pantry inventory."""

    def __init__(self, llm: ChatOpenAI = None, retriever: RecipeRetriever = None):
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.3)
        self.retriever = retriever or RecipeRetriever()
        self.parser = PydanticOutputParser(pydantic_object=MealPlan)
        self.chain = planner_prompt | self.llm | self.parser

    def plan(self, preferences: UserPreferences, pantry: PantryInventory) -> MealPlan:
        """Generate a meal plan based on user preferences and pantry inventory."""
        query = " ".join(preferences.cuisine_preferences) if preferences.cuisine_preferences else "healthy meals"
        candidates = self.retriever.retrieve(
            query=query,
            dietary_tags=preferences.dietary_restrictions or None,
            max_calories=preferences.calorie_target,
            max_cost=preferences.budget,
            k=preferences.num_meals * 7,
        )
        candidate_text = "\n".join(
            f"ID: {r.id}\nName: {r.name}\nIngredients: {', '.join(r.ingredients)}\nCalories: {r.calories}\nDietary tags: {', '.join(r.dietary_tags)}\nCost: ${r.cost:.2f}\nAisle: {r.aisle}\nInstructions: {r.instructions}"
            for r in candidates
        )
        pantry_text = "\n".join(f"- {item.name}: {item.quantity} {item.unit}" for item in pantry.items)
        return self.chain.invoke({"recipes": candidate_text, "pantry": pantry_text})
