# Copyright (c) 2018, Zebula Sampedro, CU Research Computing

import unittest
from traitlets import Unicode
from optionsspawner.forms import TextInputField



class TextInputFieldTestCase(unittest.TestCase):
    """Tests for optionsspawner.forms.characterfield.TextInputField."""

    def test_render_optional_free_text(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<input id="id_test_attr" class="form-control" name="test_attr" type="text">\n""")
        field = TextInputField('test_attr',
            label='Test Attribute'
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_render_required_free_text_default_value(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<input id="id_test_attr" class="form-control" name="test_attr" required type="text" value="DEFAULT">\n""")
        field = TextInputField('test_attr',
            label='Test Attribute',
            attr_required=True,
            attr_value='DEFAULT'
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_render_required_email(self):
        expected = ("""<label for="test_attr">Test Attribute</label>\n"""
        """<input id="id_test_attr" class="form-control" name="test_attr" required type="email">\n""")
        field = TextInputField('test_attr',
            label='Test Attribute',
            attr_type='email',
            attr_required=True
        )
        rendered = field.render()
        self.assertEqual(rendered, expected)

    def test_returns_unicode_trait(self):
        expected = Unicode().tag(config=True)
        field = TextInputField('test_attr',
            label='Test Attribute',
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Unicode)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_returns_unicode_trait_with_default(self):
        expected = Unicode(default_value='default').tag(config=True)
        field = TextInputField('test_attr',
            label='Test Attribute',
            attr_value='default'
        )
        traitlet = field.get_trait()
        self.assertIsInstance(traitlet, Unicode)
        self.assertEqual(traitlet.metadata, expected.metadata)
        self.assertEqual(traitlet.default_value, expected.default_value)

    def test_normalize_non_empty_string_with_default(self):
        expected = 'a test string'
        field = TextInputField('test_attr',
            label='Test Attribute',
            attr_value='default'
        )
        normalized = field.normalize_user_option(['a test string'])
        self.assertEqual(normalized, expected)

    def test_normalize_non_string(self):
        expected = '1234'
        field = TextInputField('test_attr',
            label='Test Attribute'
        )
        normalized = field.normalize_user_option([1234])
        self.assertEqual(normalized, expected)

    def test_normalize_empty_string_with_default(self):
        expected = 'default'
        field = TextInputField('test_attr',
            label='Test Attribute',
            attr_value='default'
        )
        normalized = field.normalize_user_option([''])
        self.assertEqual(normalized, expected)

    def test_normalize_empty_string_no_default(self):
        expected = None
        field = TextInputField('test_attr',
            label='Test Attribute'
        )
        normalized = field.normalize_user_option([''])
        self.assertEqual(normalized, expected)

    def test_normalize_empty_string_no_default_required(self):
        field = TextInputField('test_attr',
            label='Test Attribute',
            attr_required=True
        )
        self.assertRaises(ValueError, field.normalize_user_option, [''])


if __name__ == '__main__':
    unittest.main()
