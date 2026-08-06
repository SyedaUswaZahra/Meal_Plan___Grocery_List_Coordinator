import json
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from schemas.models import Recipe


class RecipeRetriever:
    """Retriever over a vector store of recipe embeddings."""

    def __init__(self, seed_file: str = "data/recipes/seed_recipes.json", persist_dir: str = ".chroma"):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.vectorstore = Chroma(
            collection_name="recipes",
            embedding_function=self.embeddings,
            persist_directory=persist_dir,
        )
        self.recipes: dict[str, Recipe] = {}
        self._load_seed_recipes(seed_file)
        self._index_recipes()

    def _load_seed_recipes(self, seed_file: str) -> None:
        path = Path(seed_file)
        if not path.exists():
            return
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            recipe = Recipe(**item)
            self.recipes[recipe.id] = recipe

    def _embed_text(self, recipe: Recipe) -> str:
        return f"{recipe.name}. Ingredients: {', '.join(recipe.ingredients)}. Dietary tags: {', '.join(recipe.dietary_tags)}"

    def _index_recipes(self) -> None:
        if not self.recipes:
            return
        ids = list(self.recipes.keys())
        texts = [self._embed_text(self.recipes[i]) for i in ids]
        metadatas = [
            {
                "calories": self.recipes[i].calories,
                "cost": self.recipes[i].cost,
                "dietary_tags": self.recipes[i].dietary_tags,
            }
            for i in ids
        ]
        self.vectorstore.add_texts(texts=texts, metadatas=metadatas, ids=ids)

    def retrieve(
        self,
        query: str,
        dietary_tags: list[str] | None = None,
        max_calories: int | None = None,
        max_cost: float | None = None,
        k: int = 5,
    ) -> list[Recipe]:
        """Filter by dietary tags, calorie range, and budget, then return top-k by similarity."""
        filter_dict: dict = {}
        if dietary_tags:
            filter_dict["dietary_tags"] = {"$in": dietary_tags}
        if max_calories is not None:
            filter_dict["calories"] = {"$lte": max_calories}
        if max_cost is not None:
            filter_dict["cost"] = {"$lte": max_cost}

        results = self.vectorstore.similarity_search(
            query,
            k=k,
            filter=filter_dict if filter_dict else None,
        )
        return [self.recipes[doc.metadata.get("id", doc.id)] for doc in results]
