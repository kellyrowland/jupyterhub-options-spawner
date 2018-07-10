# Copyright (c) 2018, Zebula Sampedro, CU Research Computing

import unittest
from optionsspawner.forms import (
    OptionsForm,
    TextInputField,
)



class OptionsFormTestCase(unittest.TestCase):
    """Tests for optionsspawner.forms.base.OptionsForm."""

    def test_render_two_text_fields(self):
        field1 = TextInputField('text_attr_1',
            label="First Input"
        )
        field2 = TextInputField('text_attr_2',
            label="Second Input",
        )
        field_list = [field1, field2]
        form = OptionsForm(form_fields=field_list)

        expected = '\n'.join([
            form.validation_style,
            field1.render(),
            field2.render(),
        ])
        rendered = form.render()
        self.assertEqual(rendered, expected)

    def test_get_options_from_form(self):
        expected = {
            'text_attr_1': ['test1'],
            'text_attr_2': ['test2'],
        }
        field1 = TextInputField('text_attr_1',
            label="First Input"
        )
        field2 = TextInputField('text_attr_2',
            label="Second Input",
        )
        field_list = [field1, field2]
        form = OptionsForm(form_fields=field_list)

        form_data = {
            'text_attr_1': ['test1'],
            'text_attr_2': ['test2'],
        }
        options = form.get_options_from_form(form_data)
        self.assertEqual(options, expected)

    def test_get_options_from_empty_form(self):
        expected = {
            'text_attr_1': None,
            'text_attr_2': None,
        }
        field1 = TextInputField('text_attr_1',
            label="First Input"
        )
        field2 = TextInputField('text_attr_2',
            label="Second Input",
        )
        field_list = [field1, field2]
        form = OptionsForm(form_fields=field_list)

        form_data = {}
        options = form.get_options_from_form(form_data)
        self.assertEqual(options, expected)

    def test_get_normalized_options(self):
        expected = {
            'text_attr': 'test',
        }
        field = TextInputField('text_attr',
            label="First Input"
        )
        field_list = [field]
        form = OptionsForm(form_fields=field_list)

        user_options = {
            'text_attr': ['test'],
        }
        normalized_options = form.get_normalized_user_options(user_options)
        self.assertEqual(normalized_options, expected)


if __name__ == '__main__':
    unittest.main()
