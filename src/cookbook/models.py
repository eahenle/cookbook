"""Domain models for managing recipes."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Recipe:
    """Immutable recipe record."""

    name: str
    ingredients: tuple[str, ...]
    instructions: str
    tags: tuple[str, ...] = ()

    def matches(self, query: str) -> bool:
        """Return True when a case-insensitive query matches the recipe name, ingredient, or tag."""
        needle = query.strip().lower()
        if not needle:
            return False
        return (
            needle in self.name.lower()
            or any(needle in ingredient.lower() for ingredient in self.ingredients)
            or any(needle in tag.lower() for tag in self.tags)
        )


@dataclass(slots=True)
class Cookbook:
    """A mutable in-memory collection of recipes."""

    recipes: list[Recipe] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate invariants for pre-seeded recipes."""
        seen: set[str] = set()
        for recipe in self.recipes:
            lowered_name = recipe.name.lower()
            if lowered_name in seen:
                msg = f"Recipe with name '{recipe.name}' already exists."
                raise ValueError(msg)
            seen.add(lowered_name)

    def add_recipe(self, recipe: Recipe) -> None:
        """Add a unique recipe by name."""
        lowered_names = {existing.name.lower() for existing in self.recipes}
        if recipe.name.lower() in lowered_names:
            msg = f"Recipe with name '{recipe.name}' already exists."
            raise ValueError(msg)
        self.recipes.append(recipe)

    def find(self, query: str) -> list[Recipe]:
        """Return recipes matching a query."""
        return [recipe for recipe in self.recipes if recipe.matches(query)]

    def by_tag(self, tag: str) -> list[Recipe]:
        """Return recipes containing a tag (case-insensitive exact tag match)."""
        normalized = tag.strip().lower()
        if not normalized:
            return []
        return [
            recipe
            for recipe in self.recipes
            if any(existing_tag.lower() == normalized for existing_tag in recipe.tags)
        ]
