"""Emprically calculate the cost to spawn a minion based on its attributes."""


class Lair:
    """Lair class to represent the space in the lair occupied by minions and materials.
    Assumes infinite space for simplicity.
    """

    def __init__(self, desired_minion_level: int):
        self.materials_dict = {
            "material_1": 0,
            "material_2": 0,
        }
        self.minions_dict = {f"minion_level_{i}": 0 for i in range(1, desired_minion_level + 1)}

    def add_material(self, material_level: int) -> None:
        """Add material to the lair."""
        key = f"material_{material_level}"
        if key in self.materials_dict:
            self.materials_dict[key] += 1
        else:
            raise ValueError(f"Invalid material level: {material_level}")

    def merge(self) -> None:
        """Merge materials and minions in the lair to create higher level materials/minions.
        Anything that can be merged will be merged.
        """
        while any(v >= 2 for v in self.materials_dict.values()):
            # iterate levels 1 .. (max_level - 1)
            for level in range(1, len(self.materials_dict)):
                key = f"material_{level}"
                if self.materials_dict[key] >= 2:
                    self.materials_dict[key] -= 2
                    if level ==2:
                        self.minions_dict["minion_level_1"] += 1
                    else:
                        self.materials_dict[f"material_{level + 1}"] += 1

        # continue while any minion level can be merged
        while any(v >= 2 for v in self.minions_dict.values()):
            # iterate levels 1 .. (max_level - 1)
            for level in range(1, len(self.minions_dict)):
                key = f"minion_level_{level}"
                if self.minions_dict[key] >= 2:
                    self.minions_dict[key] -= 2
                    self.minions_dict[f"minion_level_{level + 1}"] += 1

    


def main():
    """Main function"""


if __name__ == "__main__":
    main()
