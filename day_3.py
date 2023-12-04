from functools import reduce
import re
from typing import Dict, List, Set, Tuple
from utils import load_data

DATA = load_data(__name__)

EXAMPLE = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598..",
]


def is_symbol(char: str):
    return not (char.isdigit() or char == ".")


def populate_map(
    lines_map: Dict[int, Set[int]], afected_idx: int, line_idx: int
) -> Dict[int, Set[int]]:
    affected_fields = {afected_idx - 1, afected_idx, afected_idx + 1}
    current_content = lines_map.get(line_idx, set())
    lines_map[line_idx] = current_content.union(affected_fields)
    return lines_map


def get_partnumber_map(numbers_data: List[str]):
    lines_map: Dict[int, Set[int]] = {}
    for line_idx, line in enumerate(numbers_data):
        for char_idx, char in enumerate(line):
            if is_symbol(char):
                lines_map = populate_map(lines_map, char_idx, line_idx)
                lines_map = populate_map(lines_map, char_idx, line_idx - 1)
                lines_map = populate_map(lines_map, char_idx, line_idx + 1)
    return lines_map


def get_continuous_numbers(line: str):
    pattern = r"\d+"
    matches = re.finditer(pattern, line)

    result = []
    for match in matches:
        number = int(match.group())
        location = (match.start(), match.end())
        result.append((number, location))

    return result


def get_part_numbers():
    part_numbers = []
    affected_locations = get_partnumber_map(DATA)
    for line_idx, line in enumerate(DATA):
        for number, location in get_continuous_numbers(line):
            line_affectation = affected_locations[line_idx]
            loc_start, loc_end = location
            adjacent_locations = [
                n in line_affectation for n in range(loc_start, loc_end)
            ]
            if any(adjacent_locations):
                part_numbers.append(number)
    return part_numbers


def get_adjacent_numbers(
    data: List[str], line_idx: int, adjacency: Tuple[int, int]
) -> List[int]:  # -> list[Any]:
    adjancent_numbers = []
    start = line_idx - 1 if line_idx > 0 else 0
    for adj_line in data[start : line_idx + 2]:
        for number, location in get_continuous_numbers(adj_line):
            loc_start, loc_end = location
            adjacent_locations = [n in adjacency for n in range(loc_start, loc_end)]
            if any(adjacent_locations):
                adjancent_numbers.append(number)
    return adjancent_numbers


def get_gear_ratios(data=EXAMPLE):
    gear_ratios = []
    gear_list = []
    adjacencies = []
    for line_idx, line in enumerate(data):
        print(line_idx, line)
        gears = [l.start() for l in re.finditer(r"\*", line)]
        for gear_idx in gears:
            gear_list.append(gear_idx)
            gear_start = gear_idx - 1 if gear_idx > 0 else 0
            adjacent_numbers = get_adjacent_numbers(
                data, line_idx, (gear_start, gear_idx + 1)
            )
            if len(adjacent_numbers) == 2:
                adjacencies.append(adjacent_numbers)
                gear_ratios.append(reduce(lambda a, b: a * b, adjacent_numbers))
    print(len(gear_list))
    print("matanga")
    print(len(adjacencies))
    return gear_ratios


ANSWER_1 = sum(get_part_numbers())
