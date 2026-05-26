from cookbook.models import Cookbook, Recipe


def test_recipe_matches_name_ingredient_and_tag() -> None:
    recipe = Recipe(
        name="Tomato Soup",
        ingredients=("tomato", "basil", "cream"),
        instructions="Simmer and blend.",
        tags=("vegetarian",),
    )

    assert recipe.matches("tomato")
    assert recipe.matches("basil")
    assert recipe.matches("Vegetarian")
    assert not recipe.matches("chicken")


def test_cookbook_enforces_unique_names_case_insensitive() -> None:
    book = Cookbook()
    book.add_recipe(Recipe("Toast", ("bread",), "Toast bread."))

    try:
        book.add_recipe(Recipe("toast", ("bread", "butter"), "Toast and butter bread."))
    except ValueError as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("Expected duplicate recipe name to fail")


def test_cookbook_search_and_tag_filter() -> None:
    book = Cookbook(
        [
            Recipe("Avocado Toast", ("bread", "avocado"), "Toast bread.", ("breakfast",)),
            Recipe("Salad", ("lettuce", "olive oil"), "Mix ingredients.", ("vegan", "quick")),
        ]
    )

    search_results = book.find("avocado")
    tag_results = book.by_tag("quick")

    assert [recipe.name for recipe in search_results] == ["Avocado Toast"]
    assert [recipe.name for recipe in tag_results] == ["Salad"]
