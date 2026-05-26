"""Simple CLI for cookbook search experiences."""

from __future__ import annotations

import argparse

from .models import Cookbook, Recipe


def build_sample_cookbook() -> Cookbook:
    """Build a sample dataset for the CLI."""
    book = Cookbook()
    book.add_recipe(
        Recipe(
            name="Pasta Primavera",
            ingredients=("pasta", "zucchini", "garlic", "parmesan"),
            instructions="Boil pasta, saute vegetables, and combine.",
            tags=("vegetarian", "weeknight"),
        )
    )
    book.add_recipe(
        Recipe(
            name="Lemon Herb Salmon",
            ingredients=("salmon", "lemon", "dill", "olive oil"),
            instructions="Bake salmon with lemon, dill, and olive oil.",
            tags=("high-protein", "quick"),
        )
    )
    return book


def main() -> int:
    """Entrypoint for the cookbook CLI."""
    parser = argparse.ArgumentParser(description="Search sample recipes")
    parser.add_argument("query", nargs="?", default="", help="Query string to search for")
    parser.add_argument("--tag", dest="tag", default="", help="Filter by exact tag")
    args = parser.parse_args()

    book = build_sample_cookbook()
    if args.tag:
        matches = book.by_tag(args.tag)
    else:
        matches = book.find(args.query)

    for recipe in matches:
        print(f"- {recipe.name}: {', '.join(recipe.ingredients)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
