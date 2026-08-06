from typing import Dict


class AisleMappingTool:
    """Tool mapping grocery items to store aisles."""

    DEFAULT_MAPPING: Dict[str, str] = {
        "apple": "Produce",
        "banana": "Produce",
        "orange": "Produce",
        "lemon": "Produce",
        "lime": "Produce",
        "avocado": "Produce",
        "tomato": "Produce",
        "onion": "Produce",
        "garlic": "Produce",
        "ginger": "Produce",
        "potato": "Produce",
        "carrot": "Produce",
        "celery": "Produce",
        "broccoli": "Produce",
        "lettuce": "Produce",
        "cucumber": "Produce",
        "zucchini": "Produce",
        "bell pepper": "Produce",
        "pepper": "Produce",
        "mushroom": "Produce",
        "basil": "Produce",
        "parsley": "Produce",
        "cilantro": "Produce",
        "rosemary": "Produce",
        "thyme": "Produce",
        "asparagus": "Produce",
        "cherry tomatoes": "Produce",
        "mixed berries": "Produce",
        "berries": "Produce",
        "jalapeño": "Produce",
        "jalapeno": "Produce",
        "shallot": "Produce",
        "red onion": "Produce",
        "shrimp": "Seafood",
        "salmon": "Seafood",
        "fish": "Seafood",
        "milk": "Dairy",
        "cheese": "Dairy",
        "cheddar cheese": "Dairy",
        "feta cheese": "Dairy",
        "parmesan cheese": "Dairy",
        "fresh mozzarella": "Dairy",
        "mozzarella": "Dairy",
        "butter": "Dairy",
        "sour cream": "Dairy",
        "yogurt": "Dairy",
        "eggs": "Dairy",
        "almond milk": "Dairy Alternative",
        "coconut milk": "Canned Goods",
        "bread": "Bakery",
        "tortilla": "Bakery",
        "flour tortillas": "Bakery",
        "corn tortillas": "Bakery",
        "whole wheat tortilla": "Bakery",
        "pizza dough": "Bakery",
        "chicken": "Meat",
        "chicken breast": "Meat",
        "chicken thighs": "Meat",
        "ground beef": "Meat",
        "beef": "Meat",
        "turkey breast": "Deli",
        "turkey": "Deli",
        "tofu": "Produce",
        "rice": "Pantry",
        "jasmine rice": "Pantry",
        "arborio rice": "Rice",
        "quinoa": "Pantry",
        "pasta": "Pasta",
        "spaghetti": "Pasta",
        "penne": "Pasta",
        "penne pasta": "Pasta",
        "oats": "Breakfast",
        "rolled oats": "Breakfast",
        "chia seeds": "Pantry",
        "maple syrup": "Breakfast",
        "vanilla extract": "Pantry",
        "soy sauce": "International",
        "taco seasoning": "International",
        "green curry paste": "International",
        "red pepper flakes": "Spices",
        "cumin": "Spices",
        "turmeric": "Spices",
        "oregano": "Spices",
        "salt": "Spices",
        "pepper": "Spices",
        "olive oil": "Pantry",
        "vegetable oil": "Pantry",
        "red wine vinegar": "Pantry",
        "balsamic vinegar": "Pantry",
        "white wine": "Pantry",
        "tomato sauce": "Canned Goods",
        "tomato paste": "Canned Goods",
        "vegetable broth": "Canned Goods",
        "black beans": "Canned Goods",
        "chickpeas": "Canned Goods",
        "red lentils": "Canned Goods",
        "lentils": "Canned Goods",
        "kalamata olives": "Canned Goods",
        "bamboo shoots": "Canned Goods",
        "corn": "Canned Goods",
        "mustard": "Pantry",
        "mayonnaise": "Pantry",
        "frozen": "Frozen Foods",
    }

    FALLBACK_AISLE = "General"

    def __init__(self, mapping: Dict[str, str] = None):
        """Initialize with an optional custom aisle mapping.

        Args:
            mapping: Optional dict mapping item name keywords to aisle names.
                If None, the default mapping is used.
        """
        self.mapping = mapping if mapping is not None else dict(self.DEFAULT_MAPPING)

    def map_item(self, item_name: str) -> str:
        """Map a single grocery item to an aisle.

        Args:
            item_name: The name of the grocery item.

        Returns:
            The aisle name for the item, or a generic fallback if no
            keyword matches.
        """
        if not item_name:
            return self.FALLBACK_AISLE

        normalized = item_name.strip().lower()

        # Exact match first
        if normalized in self.mapping:
            return self.mapping[normalized]

        # Substring match for multi-word item names
        for keyword, aisle in self.mapping.items():
            if keyword in normalized:
                return aisle

        return self.FALLBACK_AISLE

    def map_items(self, item_names: list[str]) -> Dict[str, str]:
        """Map a list of grocery items to aisles.

        Args:
            item_names: A list of grocery item names.

        Returns:
            A dict mapping each item name to its corresponding aisle.
        """
        return {item: self.map_item(item) for item in item_names}
