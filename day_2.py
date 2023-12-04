from functools import reduce
from typing import List, Tuple
from utils import load_data


CONSTRAINTS = {"red": 12, "green": 13, "blue": 14}


def process_gameset(gset: List[str]):
    pset = []
    for cubes_str in gset:
        total, color = cubes_str.strip().split(" ")
        pset.append((total, color))
    return pset


def get_minimal_required(game_sets: List[Tuple[str, str]]):
    minimal_required = {"red": 0, "green": 0, "blue": 0}
    for total, color in game_sets:
        if minimal_required[color] < int(total):
            minimal_required[color] = int(total)
    return minimal_required


def parsed_data():
    data = load_data("day_2")
    games = []
    for game in data:
        gamename, gamesets = game.split(":")
        game_id = gamename.replace("Game", "").strip()
        game_sets = [process_gameset(gset.split(",")) for gset in gamesets.split(";")]
        merged_sets = [item for cubes in game_sets for item in cubes]
        set_viability = [
            int(total) < CONSTRAINTS[color] for total, color in merged_sets
        ]
        game_minimals = get_minimal_required(merged_sets)
        games.append(
            {
                "id": int(game_id),
                "is_possible": all(set_viability),
                "game_minimals": game_minimals,
                "power": reduce(lambda a, b: a * b, game_minimals.values()),
            }
        )
    return games


ANSWER_1 = sum([game["id"] for game in parsed_data() if game["is_possible"]])
ANSWER_2 = sum([game["power"] for game in parsed_data()])
