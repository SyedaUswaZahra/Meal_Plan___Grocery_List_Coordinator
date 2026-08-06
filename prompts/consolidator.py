from langchain_core.prompts import ChatPromptTemplate

consolidator_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at consolidating recipe ingredients into a single grocery list. "
            "You will be given a meal plan and the user's current pantry inventory.\n\n"
            "Your task:\n"
            "1. Merge all ingredients from every recipe in the meal plan into one consolidated "
            "grocery list. Combine duplicate ingredients by summing their quantities (convert "
            "units where sensible, e.g., cups, tbsp, g, pieces).\n"
            "2. For each consolidated ingredient, check the pantry inventory. If the user "
            "already owns enough of that ingredient, subtract the owned quantity from the "
            "needed quantity and mark the item as 'owned'.\n"
            "3. Flag items the user already owns (owned=true) and items still needing to be "
            "purchased (owned=false).\n\n"
            "Return the result as a JSON object with the key 'items' containing a list of "
            "objects, each with 'name', 'quantity', 'needed', and 'owned' fields. 'needed' "
            "should be true if the item requires purchase, 'owned' should be true if the item "
            "is already in the pantry.",
        ),
        ("human", "Meal plan:\n{meal_plan}\n\nPantry inventory:\n{pantry_inventory}"),
    ]
)
