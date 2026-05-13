import csv
from typing import List

def save_to_csv(path: str, headers: List[str], rows: List[List[str]]) -> None:
    with open(path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(headers)

        for row in rows:
            writer.writerow(row)

def load_from_csv(path: str) -> List[List[str]]:
    with open(path, "r") as file:
        reader = csv.reader(file)
        next(reader)
        return [row for row in reader]
