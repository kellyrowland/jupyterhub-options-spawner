# Copyright (c) 2018, Zebula Sampedro, CU Research Computing

import unittest
from traitlets import (
    Unicode,
    Bool,
)
from optionsspawner.forms import CheckboxInputField



class CheckboxInputFieldTestCase(unittest.TestCase):
    """Tests for optionsspawner.forms.checkboxfield.CheckboxInputField."""

    def test_render_unicode_value_checked_by_default(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<input id="id_test_attr" class="form-control" checked name="test_attr" type="checkbox" value="test">\n""")
        field = CheckboxInputField('test_attr',
            label='Test Attribute',
            attr_value='test',
            attr_checked=True
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_render_unicode_value(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<input id="id_test_attr" class="form-control" name="test_attr" type="checkbox" value="test">\n""")
        field = CheckboxInputField('test_attr',
            label='Test Attribute',
            attr_value='test'
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_render_no_value(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<input id="id_test_attr" class="form-control" name="test_attr" type="checkbox">\n""")
        field = CheckboxInputField('test_attr',
            label='Test Attribute'
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_returns_bool_trait_with_no_value(self):
        expected = Bool().tag(config=True)
        field = CheckboxInputField('test_attr',
            label='Test Attribute'
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Bool)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_returns_unicode_trait_with_unciode_value(self):
        expected = Unicode().tag(config=True)
        field = CheckboxInputField('test_attr',
            label='Test Attribute',
            attr_value='test'
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Unicode)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_normalize_checkbox_no_value_unchecked(self):
        expected = False
        field = CheckboxInputField('test_attr',
            label='Test Attribute'
        )
        normalized = field.normalize_user_option(None)
        self.assertEqual(normalized, expected)

    def test_normalize_checkbox_no_value_checked(self):
        expected = True
        field = CheckboxInputField('test_attr',
            label='Test Attribute'
        )
        normalized = field.normalize_user_option(['on'])
        self.assertEqual(normalized, expected)

    def test_normalize_checkbox_unicode_value_unchecked(self):
        expected = ''
        field = CheckboxInputField('test_attr',
            label='Test Attribute',
            attr_value='test'
        )
        normalized = field.normalize_user_option(None)
        self.assertEqual(normalized, expected)

    def test_normalize_checkbox_unicode_value_checked(self):
        expected = 'test'
        field = CheckboxInputField('test_attr',
            label='Test Attribute',
            attr_value='test'
        )
        normalized = field.normalize_user_option(['test'])
        self.assertEqual(normalized, expected)


if __name__ == '__main__':
    unittest.main()
