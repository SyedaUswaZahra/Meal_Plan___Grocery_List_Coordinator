from langchain_core.prompts import ChatPromptTemplate

pantry_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at parsing free-form pantry inventory text into a structured "
            "ingredient list. Extract every ingredient the user mentions along with its quantity "
            "and unit.\n\n"
            "Guidelines for parsing:\n"
            "- Identify the ingredient name (e.g., 'chicken breast', 'olive oil', 'flour').\n"
            "- Parse the quantity as a number. Handle fractions (e.g., '1/2', '1.5'), words "
            "(e.g., 'a', 'an' → 1), and common shorthand (e.g., 'dozen' → 12).\n"
            "- Parse the unit when present (e.g., 'cups', 'tbsp', 'g', 'kg', 'oz', 'lbs', "
            "'pieces', 'cloves'). If no explicit unit is given, use 'unit'.\n"
            "- If a quantity is missing, default it to 1 with unit 'unit'.\n"
            "- Ignore filler words and unrelated notes.\n\n"
            "Return the result as a JSON object with the key 'items' containing a list of objects "
            "with 'name', 'quantity', and 'unit' fields.",
        ),
        ("human", "{pantry_text}"),
    ]
)
