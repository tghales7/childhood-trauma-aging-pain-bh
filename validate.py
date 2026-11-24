"""Validate results against the independently retained spreadsheet q values."""
import math
from pathlib import Path
from bh_adjust import adjust, read_csv

base = Path(__file__).resolve().parent
rows = adjust(read_csv(base/'data/tests.csv'), read_csv(base/'data/families.csv'))
expected = {r['test_id']: r for r in read_csv(base/'validation/expected_q.csv')}
assert len(expected) == len(rows)
maximum = 0.0
for row in rows:
    reference = expected.pop(row['test_id'])
    delta = abs(float(row['bh_q']) - float(reference['expected_q']))
    maximum = max(maximum, delta)
    assert math.isclose(float(row['bh_q']), float(reference['expected_q']),
                        rel_tol=1e-12, abs_tol=1e-15), (row['test_id'], delta)
    assert int(row['family_n']) == int(reference['expected_n'])
assert not expected
print(f'PASS: {len(rows)} q values reproduced; maximum absolute difference {maximum:.3g}.')
