from graph.graph import MealPlanGraph
from chains.intake_agent import IntakeAgent
from chains.pantry_parser import PantryParserChain
from chains.planner import PlanningChain
from chains.consolidator import ConsolidationChain
from chains.validator import ValidationChain
from chains.output_formatter import OutputFormatter
from tools.recipe_retriever import RecipeRetriever
from tools.aisle_mapper import AisleMappingTool


def main() -> None:
    """CLI entry point driving the conversation and printing final output."""
    # Instantiate all chains, retriever, aisle mapper, and formatter.
    retriever = RecipeRetriever()
    aisle_mapper = AisleMappingTool()

    intake = IntakeAgent()
    pantry_parser = PantryParserChain()
    planner = PlanningChain(retriever=retriever)
    consolidator = ConsolidationChain()
    validator = ValidationChain()
    formatter = OutputFormatter(aisle_mapper=aisle_mapper)

    # Build the MealPlanGraph with MemorySaver checkpointer.
    graph = MealPlanGraph(
        intake=intake,
        pantry_parser=pantry_parser,
        planner=planner,
        consolidator=consolidator,
        validator=validator,
        formatter=formatter,
    )

    # Run an interactive loop prompting the user for preferences and pantry text.
    print("Welcome to the Meal Planning Assistant!")
    print("Tell me about your dietary restrictions, cuisine preferences, calorie target, meals per day, and budget.")
    print("Type your preferences (or 'done' when finished):")

    user_input = ""
    while True:
        line = input("> ")
        if line.strip().lower() in ("done", "exit", "quit"):
            break
        user_input += line + "\n"

    if not user_input.strip():
        user_input = input("Please describe your preferences: ")

    print("\nWhat do you currently have in your pantry? (list ingredients with quantities, e.g., '2 cups rice, 1 lb chicken')")
    pantry_text = input("> ")

    # Drive the graph.
    graph.run(user_input)

    # Print the final calendar and aisle-grouped grocery list.
    config = {"configurable": {"thread_id": "meal-plan-thread"}}
    state = graph.graph.get_state(config)
    if state and state.values and state.values.get("final_output"):
        print("\n" + "=" * 60)
        print(state.values["final_output"])
    else:
        print("\nNo final output was generated. Please check the conversation and try again.")


if __name__ == "__main__":
    main()
