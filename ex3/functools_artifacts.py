from functools import lru_cache, partial, reduce, singledispatch
import operator
from typing import Any
from collections.abc import Callable


def spell_reducer(spells: list[int], operation: str) -> int:
    """Reduce spell powers using the selected operation."""
    if not spells:
        return 0

    operations: dict[str, Callable[[int, int], int]] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": lambda left, right: left if left > right else right,
        "min": lambda left, right: left if left < right else right,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    return reduce(operations[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    """Return three specialized enchantment functions."""
    return {
        "fire_enchant": partial(base_enchantment, 50, "Fire"),
        "ice_enchant": partial(base_enchantment, 50, "Ice"),
        "arcane_enchant": partial(base_enchantment, 50, "Arcane"),
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """Return nth Fibonacci number using memoization."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    """Return a single-dispatch spell handler."""

    @singledispatch
    def dispatch(spell: Any) -> str:
        return "Unknown spell type"

    @dispatch.register
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @dispatch.register
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @dispatch.register
    def _(spell: list) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return dispatch


def base_enchantment(power: int, element: str, target: str) -> str:
    """Sample enchantment function for partial examples."""
    return f"{element} enchantment on {target} with {power} power"


if __name__ == "__main__":
    print("\nTesting spell reducer...")
    values = [10, 20, 30, 40]
    print("Sum:", spell_reducer(values, "add"))
    print("Product:", spell_reducer(values, "multiply"))
    print("Max:", spell_reducer(values, "max"))
    print("Min:", spell_reducer(values, "min"))

    print("\nTesting partial enchanter...")
    specialized = partial_enchanter(base_enchantment)
    print(specialized["fire_enchant"]("Sword"))
    print(specialized["ice_enchant"]("Shield"))
    print(specialized["arcane_enchant"]("Orb"))

    print("\nTesting memoized fibonacci...")
    print("Fib(0):", memoized_fibonacci(0))
    print("Fib(1):", memoized_fibonacci(1))
    print("Fib(10):", memoized_fibonacci(10))
    print("Fib(15):", memoized_fibonacci(15))
    print("Cache info:", memoized_fibonacci.cache_info())

    print("\nTesting spell dispatcher...")
    dispatch = spell_dispatcher()
    print(dispatch(42))
    print(dispatch("fireball"))
    print(dispatch(["fireball", "heal", "shield"]))
    print(dispatch({"unknown": True}))
