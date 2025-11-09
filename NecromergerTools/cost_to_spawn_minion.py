"""Emprically calculate the cost to spawn a minion based on its attributes."""

import random
from pathlib import Path

import pandas as pd
import yaml


class Lair:
    """Lair class to represent the space in the lair occupied by minions and
    materials.
    Assumes infinite space for simplicity.
    """

    def __init__(
        self, max_minion_level: int, max_material_level: int = 2
    ) -> None:
        # materials indexed by integer levels starting at 1
        self.materials_dict: dict[int, int] = {
            i: 0 for i in range(1, max_material_level + 1)
        }
        # minions indexed by integer levels starting at 1
        self.minions_dict: dict[int, int] = {
            i: 0 for i in range(1, max_minion_level + 1)
        }

    def add_material(self, material_level: int) -> None:
        """Add material to the lair. Keys are integer levels (1-based)."""
        if material_level not in self.materials_dict:
            raise KeyError(
                f"material_level {material_level} not in materials_dict"
            )
        self.materials_dict[material_level] += 1

    def merge(self) -> None:
        """Merge materials and minions in the lair to create higher level
        materials/minions.
        Continues merging until no merges are possible.
        """
        # Merge materials -> possibly produce higher-level materials or a
        # level-1 minion when merging two level-2 materials.
        max_mat_level = max(self.materials_dict.keys())
        while any(v >= 2 for v in self.materials_dict.values()):
            for level in range(1, max_mat_level + 1):
                qty = self.materials_dict[level]
                if qty >= 2:
                    # perform merges (may need to merge multiple pairs)
                    pairs = qty // 2
                    self.materials_dict[level] = qty % 2
                    if level == max_mat_level:
                        # two max level materials -> one minion_level_1
                        self.minions_dict[1] = self.minions_dict[1] + pairs
                    else:
                        # upgrade materials to next level
                        self.materials_dict[level + 1] += pairs

        # Merge minions -> create higher level minions
        max_minion_level = max(self.minions_dict.keys())
        while any(
            v >= 2
            for k, v in self.minions_dict.items()
            if k < max_minion_level
        ):
            for level in range(
                1, max_minion_level
            ):  # Don't merge max level minions
                qty = self.minions_dict[level]
                if qty >= 2:
                    pairs = qty // 2
                    self.minions_dict[level] = qty % 2
                    self.minions_dict[level + 1] = (
                        self.minions_dict[level + 1] + pairs
                    )


class Station:
    """Station class to represent a station that can spawn materials.
    Stations have a cost per tap and a percent chance to spawna a
    level 1 or 2 material."""

    def __init__(
        self, cost_per_tap: int, level_1_chance: float, level_2_chance: float
    ) -> None:
        self.cost_per_tap = cost_per_tap
        self.level_1_chance = level_1_chance
        self.level_2_chance = level_2_chance

    def tap(self) -> int | None:
        """Simulate tapping the station once. Returns the level of the
        material spawned or None if no material was spawned."""
        roll = random.random()
        if roll < self.level_1_chance:
            return 1
        if roll < self.level_1_chance + self.level_2_chance:
            return 2
        return None


def run_trial(
    station: Station,
    lair: Lair,
    target_minion_level: int,
) -> int:
    """Run a single trial to spawn a minion of the target level.
    Returns the total cost incurred to spawn the minion."""
    total_cost = 0
    while lair.minions_dict[target_minion_level] < 1:
        # Tap the station
        material_level = station.tap()
        total_cost += station.cost_per_tap
        if material_level is not None:
            lair.add_material(material_level)
            lair.merge()
    return total_cost


def main():
    """Main function"""
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)

    random.seed(cfg["random_seed"])
    station = Station(**cfg["station"])
    target_minion_level = cfg["simulation"]["target_minion_level"]
    num_trials = cfg["simulation"]["num_trials"]
    total_costs = []
    for _ in range(num_trials):
        lair = Lair(
            max_minion_level=cfg["simulation"]["target_minion_level"],
            max_material_level=cfg["simulation"]["max_material_level"],
        )
        cost = run_trial(station, lair, target_minion_level)
        total_costs.append(cost)

    totals_costs_series = pd.Series(total_costs)
    print(
        f"Cost to spawn minion level {target_minion_level}:\n"
        f"{totals_costs_series.describe().astype(int)}"
    )


if __name__ == "__main__":
    main()
