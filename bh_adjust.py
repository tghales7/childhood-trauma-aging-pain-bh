"""Reproduce BH adjustments using explicit, complete test families (Python >=3.10)."""
import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path


def bh_adjust(p_values):
    """Return monotone Benjamini–Hochberg adjusted p values in input order."""
    p = list(p_values)
    if any(not math.isfinite(x) or not 0 <= x <= 1 for x in p):
        raise ValueError('Every p value must be finite and between 0 and 1.')
    order = sorted(range(len(p)), key=p.__getitem__)
    result = [0.0] * len(p)
    running = 1.0
    for rank in range(len(p), 0, -1):
        index = order[rank - 1]
        running = min(running, p[index] * len(p) / rank)
        result[index] = running
    return result


def read_csv(path):
    with Path(path).open(newline='', encoding='utf-8-sig') as f:
        return list(csv.DictReader(f))


def adjust(tests, families):
    """Check complete family membership, then adjust each family separately."""
    definitions = {}
    for family in families:
        key = family['family_id']
        if not key or key in definitions:
            raise ValueError('Family IDs must be nonempty and unique.')
        definitions[key] = family
    groups = defaultdict(list)
    identifiers = set()
    for test in tests:
        if not test['test_id'] or test['test_id'] in identifiers:
            raise ValueError('Test IDs must be nonempty and unique.')
        identifiers.add(test['test_id'])
        key = test['family_id']
        if key not in definitions:
            raise ValueError(f'Undefined family: {key}')
        groups[key].append(test)
    if set(groups) != set(definitions):
        raise ValueError('One or more declared families contain no tests.')
    output = []
    for key, rows in groups.items():
        family = definitions[key]
        n = int(family['expected_n'])
        if n != len(rows) or n < 1:
            raise ValueError(f'Incomplete family {key}: expected {n}, found {len(rows)}')
        if {r['model'] for r in rows} != {family['model']}:
            raise ValueError(f'Model mismatch in family {key}')
        # Float parsing intentionally rejects threshold strings such as '<0.001'.
        q_values = bh_adjust([float(r['p_value']) for r in rows])
        for row, q in zip(rows, q_values):
            output.append(dict(row, bh_q=repr(q), family_n=n,
                               bh_q_lt_0_05=int(q < 0.05)))
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path('data/tests.csv'))
    parser.add_argument('--families', type=Path, default=Path('data/families.csv'))
    parser.add_argument('--output', type=Path, default=Path('results/bh_results.csv'))
    args = parser.parse_args()
    rows = adjust(read_csv(args.input), read_csv(args.families))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'Adjusted {len(rows)} tests in {len({r["family_id"] for r in rows})} families.')


if __name__ == '__main__':
    main()
