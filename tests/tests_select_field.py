# Copyright (c) 2018, Zebula Sampedro, CU Research Computing

import unittest
from traitlets import (
    Unicode,
    Integer,
    Float,
)
from optionsspawner.forms import SelectField



class SelectFieldTestCase(unittest.TestCase):
    """Tests for optionsspawner.forms.selectfield.SelectField."""

    def test_render_required_unicode_with_default(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<select id="id_test_attr" class="form-control" name="test_attr" required>\n"""
        """<option id="id_test_attr_option_0" value="option1">Option 1</option>\n"""
        """<option id="id_test_attr_option_1" value="option2" selected>Option 2</option>\n"""
        """</select>\n""")
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[('option1', 'Option 1'), ('option2', 'Option 2')],
            default='option2'
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_render_required_unicode_no_default(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<select id="id_test_attr" class="form-control" name="test_attr" required>\n"""
        """<option id="id_test_attr_option_0" value="option1" selected>Option 1</option>\n"""
        """<option id="id_test_attr_option_1" value="option2">Option 2</option>\n"""
        """</select>\n""")
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[('option1', 'Option 1'), ('option2', 'Option 2')]
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_render_required_integer_with_default(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<select id="id_test_attr" class="form-control" name="test_attr" required>\n"""
        """<option id="id_test_attr_option_0" value="1">Option 1</option>\n"""
        """<option id="id_test_attr_option_1" value="2" selected>Option 2</option>\n"""
        """</select>\n""")
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[(1, 'Option 1'), (2, 'Option 2')],
            default=2
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_render_required_float_with_default(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<select id="id_test_attr" class="form-control" name="test_attr" required>\n"""
        """<option id="id_test_attr_option_0" value="1.0">Option 1</option>\n"""
        """<option id="id_test_attr_option_1" value="2.0" selected>Option 2</option>\n"""
        """</select>\n""")
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[(1.0, 'Option 1'), (2.0, 'Option 2')],
            default=2.0
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_mismatched_choice_values(self):
        kwargs = dict(
            label='Test Attribute',
            attr_required=True,
            choices=[('option1', 'Option 1'), (2, 'Option 2')]
        )
        self.assertRaises(TypeError, SelectField, 'test_attr', **kwargs)

    def test_duplicated_choice_values(self):
        kwargs = dict(
            label='Test Attribute',
            attr_required=True,
            choices=[(2, 'Option 1'), (2, 'Option 2')]
        )
        self.assertRaises(ValueError, SelectField, 'test_attr', **kwargs)

    def test_returns_unicode_trait_with_unicode_choices(self):
        expected = Unicode(default_value='option2').tag(config=True)
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[('option1', 'Option 1'), ('option2', 'Option 2')],
            default='option2'
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Unicode)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_returns_integer_trait_with_integer_choices(self):
        expected = Integer(default_value=1).tag(config=True)
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[(1, 'Option 1'), (2, 'Option 2')]
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Integer)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_returns_float_trait_with_float_choices(self):
        expected = Float(default_value=2.0).tag(config=True)
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[(1.0, 'Option 1'), (2.0, 'Option 2')],
            default=2.0
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Float)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_normalize_unicode_selection(self):
        expected = 'option1'
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[('option1', 'Option 1'), ('option2', 'Option 2')],
            default='option1'
        )
        normalized = field.normalize_user_option(['option1'])
        self.assertEqual(normalized, expected)

    def test_normalize_integer_selection(self):
        expected = 2
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[(1, 'Option 1'), (2, 'Option 2')],
            default=1
        )
        normalized = field.normalize_user_option(['2'])
        self.assertEqual(normalized, expected)

    def test_normalize_float_selection(self):
        expected = 2.0
        field = SelectField('test_attr',
            label='Test Attribute',
            attr_required=True,
            choices=[(1.0, 'Option 1'), (2.0, 'Option 2')],
            default=1.0
        )
        normalized = field.normalize_user_option(['2.0'])
        self.assertEqual(normalized, expected)


if __name__ == '__main__':
    unittest.main()
