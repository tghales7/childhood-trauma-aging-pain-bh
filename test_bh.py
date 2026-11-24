import math
import unittest
from bh_adjust import bh_adjust, adjust


class BHTests(unittest.TestCase):
    def test_known_example_and_input_order(self):
        self.assertEqual(bh_adjust([.04, .001, .03, .01]), [.04, .004, .04, .02])

    def test_ties_boundaries_and_singleton(self):
        self.assertEqual(bh_adjust([0, .02, .02, 1]), [0, .02*4/3, .02*4/3, 1])
        self.assertEqual(bh_adjust([.3]), [.3])
        self.assertEqual(bh_adjust([]), [])

    def test_invalid_values(self):
        for p in [-.1, 1.1, math.nan, math.inf]:
            with self.assertRaises(ValueError):
                bh_adjust([p])

    def test_incomplete_family_rejected(self):
        with self.assertRaises(ValueError):
            adjust([dict(test_id='a', family_id='f', model='1', p_value='.1')],
                   [dict(family_id='f', model='1', expected_n='2')])

    def test_models_remain_separate(self):
        tests = [dict(test_id=str(i), family_id=f'f{i}', model=str(i), p_value=str(p))
                 for i, p in enumerate([.01, .9], 1)]
        families = [dict(family_id=f'f{i}', model=str(i), expected_n='1') for i in [1, 2]]
        self.assertEqual([float(r['bh_q']) for r in adjust(tests, families)], [.01, .9])


if __name__ == '__main__':
    unittest.main()
