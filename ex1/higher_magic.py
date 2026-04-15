from collections.abc import Callable
from typing import Any


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    """Return a spell that executes spell1 and spell2 on same inputs."""

    def combined_spell(*args: Any, **kwargs: Any) -> tuple[Any, Any]:
        return (spell1(*args, **kwargs), spell2(*args, **kwargs))

    return combined_spell


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    """Return a spell that casts with amplified power."""

    def amplified_spell(*args: Any, **kwargs: Any) -> Any:
        new_args = list(args)
        new_kwargs = dict(kwargs)
        amplified_input = False

        if "power" in new_kwargs and isinstance(
            new_kwargs["power"], (int, float)
        ):
            new_kwargs["power"] *= multiplier
            amplified_input = True
        elif len(new_args) >= 2 and isinstance(new_args[1], (int, float)):
            new_args[1] *= multiplier
            amplified_input = True
        else:
            for index, value in enumerate(new_args):
                if isinstance(value, (int, float)):
                    new_args[index] = value * multiplier
                    amplified_input = True
                    break

        result = base_spell(*new_args, **new_kwargs)

        if not amplified_input and isinstance(result, (int, float)):
            return result * multiplier

        return result

    return amplified_spell


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    """Return a spell that casts only when condition is true."""

    def conditional_spell(*args: Any, **kwargs: Any) -> Any:
        if condition(*args, **kwargs):
            return spell(*args, **kwargs)
        return "Spell fizzled"

    return conditional_spell


def spell_sequence(spells: list[Callable]) -> Callable:
    """Return a spell that casts all given spells in order."""

    def sequence_spell(*args: Any, **kwargs: Any) -> list[Any]:
        return [spell(*args, **kwargs) for spell in spells]

    return sequence_spell


def fireball(target: str, power: int) -> str:
    """Sample spell used for demonstration."""
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    """Sample spell used for demonstration."""
    return f"Heal restores {target} for {power} HP"


def is_safe_power(_target: str, power: int) -> bool:
    """Allow cast only for powers up to 50."""
    return power <= 50


if __name__ == "__main__":
    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    print("Combined spell result:", combined("Dragon", 20))

    print("\nTesting power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print("Original:", fireball("Golem", 10))
    print("Amplified:", mega_fireball("Golem", 10))

    print("\nTesting conditional caster...")
    safe_fireball = conditional_caster(is_safe_power, fireball)
    print(safe_fireball("Ogre", 40))
    print(safe_fireball("Ogre", 80))

    print("\nTesting spell sequence...")
    combo = spell_sequence([fireball, heal])
    print(combo("Knight", 15))
