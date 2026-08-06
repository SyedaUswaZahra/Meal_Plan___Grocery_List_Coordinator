from langchain_core.prompts import ChatPromptTemplate

planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert meal planner. Generate a complete week of meals based on the "
            "user's preferences, budget, and available pantry inventory.\n\n"
            "For every meal you create, you MUST:\n"
            "- Use at least 2-3 pantry items from the provided inventory in each meal.\n"
            "- Respect the user's dietary restrictions (e.g., vegetarian, vegan, gluten-free, "
            "nut allergy).\n"
            "- Stay within the user's calorie target per meal.\n"
            "- Stay within the user's total grocery budget.\n"
            "- Prefer recipes from the provided candidate list where possible.\n\n"
            "Return the result as a JSON object with the key 'meals' containing a list of "
            "objects, each with 'day' and 'recipe' fields. The 'recipe' object must include "
            "'id', 'name', 'ingredients', 'calories', 'dietary_tags', 'cost', 'aisle', and "
            "'instructions'.",
        ),
        ("human", "Candidate recipes:\n{recipes}\n\nPantry inventory:\n{pantry}"),
    ]
)
