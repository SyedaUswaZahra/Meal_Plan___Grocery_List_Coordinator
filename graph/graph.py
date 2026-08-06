from langgraph.graph import StateGraph, END
from langgraph.checkpoint import MemorySaver
from graph.state import MealPlanState
from chains.intake_agent import IntakeAgent
from chains.pantry_parser import PantryParserChain
from chains.planner import PlanningChain
from chains.consolidator import ConsolidationChain
from chains.validator import ValidationChain
from chains.output_formatter import OutputFormatter


class MealPlanGraph:
    """LangGraph wiring of all nodes with conditional edges, checkpointer, and interrupt."""

    def __init__(
        self,
        intake: IntakeAgent,
        pantry_parser: PantryParserChain,
        planner: PlanningChain,
        consolidator: ConsolidationChain,
        validator: ValidationChain,
        formatter: OutputFormatter,
    ):
        self.intake = intake
        self.pantry_parser = pantry_parser
        self.planner = planner
        self.consolidator = consolidator
        self.validator = validator
        self.formatter = formatter
        self.checkpointer = MemorySaver()
        self.graph = self.build()

    def build(self) -> StateGraph:
        """Build and return the compiled StateGraph."""
        workflow = StateGraph(MealPlanState)
        workflow.add_node("intake", self._intake_node)
        workflow.add_node("pantry", self._pantry_node)
        workflow.add_node("planning", self._planning_node)
        workflow.add_node("consolidation", self._consolidation_node)
        workflow.add_node("validation", self._validation_node)
        workflow.add_node("approval", self._approval_node)
        workflow.add_node("output", self._output_node)

        workflow.set_entry_point("intake")
        workflow.add_edge("intake", "pantry")
        workflow.add_edge("pantry", "planning")
        workflow.add_edge("planning", "consolidation")
        workflow.add_edge("consolidation", "validation")
        workflow.add_conditional_edges(
            "validation",
            self._route_after_validation,
            {
                "planning": "planning",
                "approval": "approval",
            },
        )
        workflow.add_edge("approval", "output")
        workflow.add_edge("output", END)

        return workflow.compile(checkpointer=self.checkpointer)

    def _intake_node(self, state: MealPlanState) -> dict:
        """Gather user preferences via the intake agent."""
        preferences = self.intake.run(state.user_input)
        return {"preferences": preferences}

    def _pantry_node(self, state: MealPlanState) -> dict:
        """Parse free-form pantry text into structured inventory."""
        pantry = self.pantry_parser.parse(state.pantry_text)
        return {"pantry": pantry}

    def _planning_node(self, state: MealPlanState) -> dict:
        """Generate a meal plan from preferences and pantry inventory."""
        meal_plan = self.planner.plan(state.preferences, state.pantry)
        return {"meal_plan": meal_plan}

    def _consolidation_node(self, state: MealPlanState) -> dict:
        """Consolidate the meal plan into a grocery list."""
        grocery_list = self.consolidator.consolidate(state.meal_plan, state.pantry)
        return {"grocery_list": grocery_list}

    def _validation_node(self, state: MealPlanState) -> dict:
        """Validate the meal plan against user constraints."""
        validation = self.validator.validate(state.meal_plan, state.preferences)
        return {"validation": validation}

    def _route_after_validation(self, state: MealPlanState) -> str:
        """Route back to planning if validation failed, otherwise to approval."""
        if state.validation is not None and not state.validation.passed:
            return "planning"
        return "approval"

    def _approval_node(self, state: MealPlanState) -> dict:
        """Human-in-the-loop approval node with interrupt for meal swapping."""
        return {"meal_plan": state.meal_plan}

    def _output_node(self, state: MealPlanState) -> dict:
        """Render the final output for the user."""
        final_output = self.formatter.render(state.meal_plan, state.grocery_list)
        return {"final_output": final_output}

    def run(self, user_input: str) -> None:
        """Drive the graph with user input."""
        config = {"configurable": {"thread_id": "meal-plan-thread"}}
        initial_state = {"user_input": user_input}
        self.graph.invoke(initial_state, config)
