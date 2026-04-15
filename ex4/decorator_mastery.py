from collections.abc import Callable
from functools import wraps
from time import perf_counter, sleep
from typing import Any


def spell_timer(func: Callable) -> Callable:
    """Measure and print execution time of a spell function."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"Casting {func.__name__}...")
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result

    return wrapper


def power_validator(min_power: int,) -> Callable:
    """Validate power before executing the wrapped callable."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if not args or not isinstance(args[2], int):
                return "Insufficient power for this spell"
            power = args[2]

            if power < min_power:
                return "Insufficient power for this spell"

            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_spell(max_attempts: int,) -> Callable:
    """Retry a spell when it raises an exception."""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_result = None
            succeeded = False
            had_failure = False
            for attempt in range(1, max_attempts + 1):
                try:
                    last_result = func(*args, **kwargs)
                    succeeded = True
                    break
                except Exception:
                    had_failure = True
                    if attempt < max_attempts:
                        print(
                            "Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})"
                        )
            if succeeded:
                if had_failure and attempt == max_attempts:
                    print(
                        "Spell casting failed after "
                        f"{max_attempts} attempts"
                    )
                return last_result
            return (
                "Spell casting failed after "
                f"{max_attempts} attempts"
            )
        return wrapper

    return decorator


class MageGuild:
    """Guild API for validating names and casting spells."""

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """Valid names contain only letters/spaces and are >= 3 chars."""
        cleaned = name.strip()
        return len(cleaned) >= 3 and all(
            char.isalpha() or char.isspace() for char in cleaned
        )

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        """Cast a spell when power is sufficient."""
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    """Example timed spell."""
    sleep(0.1)
    return "Fireball cast!"


def flaky_spell_factory() -> Callable[[], str]:
    """Create a flaky spell that succeeds on the third call."""
    attempts = 0

    @retry_spell(max_attempts=3)
    def flaky_spell() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("Spell unstable")
        return "Waaaaaaagh spelled !"

    return flaky_spell


if __name__ == "__main__":
    print("Testing spell timer...")
    print("Result:", fireball())

    print("\nTesting retrying spell...")
    flaky_spell = flaky_spell_factory()
    print(flaky_spell())

    print("\nTesting MageGuild...")
    guild = MageGuild()
    print(guild.validate_mage_name("Aeris"))
    print(guild.validate_mage_name("R2D2"))
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))
