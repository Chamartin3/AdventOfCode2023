from typing import List


def load_data(filename: str) -> List[str]:
    with open(f"./data/{filename}.txt", "r") as data:
        return [line.strip() for line in data]
