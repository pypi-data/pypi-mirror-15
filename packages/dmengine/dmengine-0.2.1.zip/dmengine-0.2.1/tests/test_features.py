# test_features.py

import unittest

from dmengine.features import FeatureSystem


class TestFeatureSystem(unittest.TestCase):

    def test_init(self):
        fs = FeatureSystem([
            {'value': '+1', 'category': 'person'},
            {'value': '-1', 'category': 'person'},
            {'value': '+2', 'category': 'person'},
            {'value': '-2', 'category': 'person'},
            {'value': '+3', 'category': 'person'},
            {'value': '-3', 'category': 'person'},
            {'value': '+sg', 'category': 'number'},
            {'value': '+pl', 'category': 'number'},
            {'value': '-sg', 'category': 'number'},
            {'value': '-pl', 'category': 'number'},
        ])
        self.assertEqual(
            [(f.value, f.category) for f in fs.FeatureSet('+1 +sg').features],
            [('+1', 'person'), ('+sg', 'number')])
