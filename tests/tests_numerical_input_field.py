# Copyright (c) 2018, Zebula Sampedro, CU Research Computing

import unittest
from traitlets import (
    Float,
    Integer,
)
from optionsspawner.forms import NumericalInputField



class NumericalInputFieldTestCase(unittest.TestCase):
    """Tests for optionsspawner.forms.characterfield.NumericalInputField."""

    def test_render_required_bounded_integer_with_default(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<input id="id_test_attr" class="form-control" max="2" min="1" name="test_attr" required type="number" value="1">\n""")
        field = NumericalInputField('test_attr',
            label='Test Attribute',
            attr_required=True,
            attr_min=1,
            attr_max=2,
            attr_value=1
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_returns_integer_trait_with_default(self):
        expected = Integer(default_value=1).tag(config=True)
        field = NumericalInputField('test_attr',
            label='Test Attribute',
            attr_required=True,
            attr_min=1,
            attr_max=2,
            attr_value=1
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Integer)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_returns_float_trait_with_default(self):
        expected = Float(default_value=1.0).tag(config=True)
        field = NumericalInputField('test_attr',
            label='Test Attribute',
            attr_required=True,
            attr_min=1,
            attr_max=2,
            attr_value=1,
            attr_step=0.1
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Float)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_returns_float_trait_with_step_any(self):
        expected = Float().tag(config=True)
        field = NumericalInputField('test_attr',
            label='Test Attribute',
            attr_step='any'
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Float)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_normalize_integer(self):
        expected = 1234
        field = NumericalInputField('test_attr',
            label='Test Attribute',
        )
        normalized = field.normalize_user_option(['1234'])
        self.assertEqual(normalized, expected)

    def test_normalize_float(self):
        expected = 1.0
        field = NumericalInputField('test_attr',
            label='Test Attribute',
            attr_step='any'
        )
        normalized = field.normalize_user_option(['1.0'])
        self.assertEqual(normalized, expected)

    def test_normalize_invalid_value(self):
        # Should be an int type since default step is 1
        field = NumericalInputField('test_attr',
            label='Test Attribute'
        )
        self.assertRaises(ValueError, field.normalize_user_option, ['1.0'])

    def test_normalize_empty_field_with_default(self):
        expected = 1234
        field = NumericalInputField('test_attr',
            label='Test Attribute',
            attr_value=1234
        )
        normalized = field.normalize_user_option([''])
        self.assertEqual(normalized, expected)

    def test_normalize_empty_field_no_default_required(self):
        expected = 0
        field = NumericalInputField('test_attr',
            label='Test Attribute',
            attr_required=True
        )
        normalized = field.normalize_user_option([''])
        self.assertEqual(normalized, expected)


if __name__ == '__main__':
    unittest.main()
