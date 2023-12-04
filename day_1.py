from ast import Tuple
from typing import List, Callable, Optional, Tuple
import random
from utils import load_data

def is_number(char: str) -> bool:
    try:
        int(char)
        return True
    except ValueError:
        return False


string_numbers = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def get_first_number(case: str):
    for idx, char in enumerate(case):
        if is_number(char):
            return idx, char

    raise Exception("No number found")


def get_first_substrnum(txt: str, inverse: bool = False) -> Tuple[Optional[int], str]:
    found_idx = None
    found_num = ""
    found = []
    for numidx, num in enumerate(string_numbers):
        num_to_find = num[::-1] if inverse else num
        idx = txt.find(num_to_find)
        if idx >= 0:
            found.append((num, idx))
            if found_idx is None or idx < found_idx:
                found_idx = idx
                found_num = numidx + 1

    return found_idx, f"{found_num}"


def get_numbers(txt: str):
    first_number_idx, first_number = get_first_number(txt)
    first_str_idx, first_str = get_first_substrnum(txt)

    first = (
        first_number
        if first_str_idx is None or first_number_idx < first_str_idx
        else first_str
    )

    last_number_idx, last_number = get_first_number(txt[::-1])
    last_str_idx, last_str = get_first_substrnum(txt[::-1], True)
    last = (
        last_number
        if last_str_idx is None or last_number_idx < last_str_idx
        else last_str
    )

    try:
        return int(first + last)
    except Exception as e:
        import pdb

        pdb.set_trace()


def evaluate_case(callback: Callable, index: int = None):
    """Evaluate a specific case from the list or random if no value is passed"""
    cases = load_data()
    total_cases = len(cases)
    if index is not None and index > total_cases:
        print("Warning: The index is bigger than the list")
        return None
    idx = index if index is not None else random.randint(1, len(cases))
    return callback(cases[idx])


def run():
    return [get_numbers(d) for d in load_data()]

