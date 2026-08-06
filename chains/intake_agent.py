from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.tools import Tool
from prompts.intake import intake_prompt
from schemas.models import UserPreferences


class IntakeAgent:
    """Conversational ReAct agent that gathers user preferences."""

    def __init__(self, llm: ChatOpenAI = None):
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.7)
        self._preferences = UserPreferences(
            dietary_restrictions=[],
            cuisine_preferences=[],
            calorie_target=2000,
            num_meals=3,
            budget=100.0,
        )

        def set_dietary_restrictions(restrictions: str) -> str:
            """Set the user's dietary restrictions. Pass a comma-separated list of restrictions (e.g., 'vegetarian, gluten-free')."""
            items = [r.strip() for r in restrictions.split(",") if r.strip()]
            self._preferences.dietary_restrictions = items
            return f"Dietary restrictions set to: {', '.join(items) or 'none'}"

        def set_cuisine_preferences(preferences: str) -> str:
            """Set the user's cuisine preferences. Pass a comma-separated list of cuisines (e.g., 'Italian, Mexican')."""
            items = [p.strip() for p in preferences.split(",") if p.strip()]
            self._preferences.cuisine_preferences = items
            return f"Cuisine preferences set to: {', '.join(items) or 'none'}"

        def set_calorie_target(target: str) -> str:
            """Set the user's calorie target per meal. Pass an integer value as a string."""
            try:
                value = int(target.strip())
                self._preferences.calorie_target = value
                return f"Calorie target set to {value} per meal."
            except ValueError:
                return "Invalid calorie target. Please provide an integer."

        def set_num_meals(num: str) -> str:
            """Set the number of meals per day. Pass an integer value as a string."""
            try:
                value = int(num.strip())
                self._preferences.num_meals = value
                return f"Number of meals set to {value} per day."
            except ValueError:
                return "Invalid number of meals. Please provide an integer."

        def set_budget(budget: str) -> str:
            """Set the user's grocery budget. Pass a numeric value as a string (e.g., '75.50')."""
            try:
                value = float(budget.strip())
                self._preferences.budget = value
                return f"Grocery budget set to ${value:.2f}."
            except ValueError:
                return "Invalid budget. Please provide a number."

        def get_preferences(_: str) -> str:
            """Return the current collected preferences as a summary."""
            p = self._preferences
            return (
                f"Current preferences:\n"
                f"- Dietary restrictions: {', '.join(p.dietary_restrictions) or 'none'}\n"
                f"- Cuisine preferences: {', '.join(p.cuisine_preferences) or 'none'}\n"
                f"- Calorie target: {p.calorie_target} per meal\n"
                f"- Meals per day: {p.num_meals}\n"
                f"- Budget: ${p.budget:.2f}"
            )

        self.tools = [
            Tool(
                name="set_dietary_restrictions",
                func=set_dietary_restrictions,
                description="Set the user's dietary restrictions. Input: comma-separated list of restrictions (e.g., 'vegetarian, gluten-free').",
            ),
            Tool(
                name="set_cuisine_preferences",
                func=set_cuisine_preferences,
                description="Set the user's cuisine preferences. Input: comma-separated list of cuisines (e.g., 'Italian, Mexican').",
            ),
            Tool(
                name="set_calorie_target",
                func=set_calorie_target,
                description="Set the user's calorie target per meal. Input: an integer as a string.",
            ),
            Tool(
                name="set_num_meals",
                func=set_num_meals,
                description="Set the number of meals per day. Input: an integer as a string.",
            ),
            Tool(
                name="set_budget",
                func=set_budget,
                description="Set the user's grocery budget. Input: a numeric value as a string (e.g., '75.50').",
            ),
            Tool(
                name="get_preferences",
                func=get_preferences,
                description="Get the current collected preferences as a summary. Input: any string.",
            ),
        ]

        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=intake_prompt,
        )
        self.executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            handle_parsing_errors=True,
            verbose=True,
        )

    def run(self, user_input: str) -> UserPreferences:
        """Run the intake conversation with the given user input and return collected preferences."""
        self.executor.invoke({"user_input": user_input})
        return self._preferences
