def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """Sort artifacts by power in descending order."""
    return sorted(
        artifacts,
        key=lambda artifact: artifact["power"],
        reverse=True,
    )


def power_filter(
        mages: list[dict],
        min_power: int
        ) -> list[dict]:
    """Keep only mages with power >= min_power."""
    return list(filter(lambda mage: mage["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    """Wrap each spell name with star markers."""
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    """Return max, min, and average power statistics."""
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}

    max_power = max(mages, key=lambda mage: mage["power"])["power"]
    min_power = min(mages, key=lambda mage: mage["power"])["power"]
    avg_power = round(
        sum(map(lambda mage: mage["power"], mages)) / len(mages),
        2,
    )
    return {
        "max_power": max_power,
        "min_power": min_power,
        "avg_power": avg_power,
    }


if __name__ == "__main__":
    artifacts_data: list[dict] = [
        {"name": "Crystal Orb", "power": 85, "type": "focus"},
        {"name": "Fire Staff", "power": 92, "type": "weapon"},
        {"name": "Moon Ring", "power": 74, "type": "accessory"},
    ]
    mages_data: list[dict] = [
        {"name": "Aeris", "power": 60, "element": "wind"},
        {"name": "Brann", "power": 95, "element": "fire"},
        {"name": "Cyra", "power": 40, "element": "ice"},
    ]
    spells = ["fireball", "heal", "shield"]

    print("\nTesting artifact sorter...")
    sorted_artifacts = artifact_sorter(artifacts_data)
    first_artifact = sorted_artifacts[0]
    second_artifact = sorted_artifacts[1]
    print(
        f"{first_artifact['name']} ({first_artifact['power']} power) "
        f"comes before {second_artifact['name']} "
        f"({second_artifact['power']} power)"
    )

    print("\nTesting power filter...")
    print(power_filter(mages_data, 50))

    print("\nTesting spell transformer...")
    print(
        " ".join(spell_transformer(spells))
    )

    print("\nTesting mage stats...")
    print(mage_stats(mages_data))
