from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from prompts.pantry import pantry_prompt
from schemas.models import PantryInventory


class PantryParser:
    """Chain that converts free-form pantry text into structured inventory."""

    def __init__(self, llm: ChatOpenAI = None):
        self.llm = llm or ChatOpenAI(model="gpt-4o", temperature=0.0)
        self.parser = PydanticOutputParser(pydantic_object=PantryInventory)
        self.chain = pantry_prompt | self.llm | self.parser

    def parse(self, raw_text: str) -> PantryInventory:
        """Parse free-form pantry text into a structured PantryInventory."""
        return self.chain.invoke({"pantry_text": raw_text})
