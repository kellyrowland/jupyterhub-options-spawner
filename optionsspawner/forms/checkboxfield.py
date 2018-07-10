# Copyright (c) 2018, Zebula Sampedro, CU Boulder Research Computing

from traitlets import (
    Unicode,
    Bool,
    Integer,
    Float,
)
from .base import FormField



class CheckboxInputField(FormField):
    """
    Form field for checkbox inputs. If `attr_value` is provided, then a trait matching
    the type of that value will be returned, either a Bool or Unicode. Otherwise, a Bool
    trait will be returned. Unlike the other field types, `attr_value` corresponds to the value
    of the field if it is checked, and does not influence the actual state of the checkbox. To
    initialize a checked checkbox, set `attr_checked=True`.
    """

    template = ("""<label for="{trait_name}">{label}</label>\n"""
    """<input id="id_{trait_name}" class="form-control" {attributes}>\n""")

    def __init__(self, *args, attr_type='checkbox', **kwargs):
        """Defaults to a checkbox represented by a boolean."""
        if attr_type != 'checkbox':
            raise ValueError("Only 'checkbox' type is supported.")
        super().__init__(*args, attr_type=attr_type, **kwargs)

    @property
    def default_value(self):
        checked_by_default = self._attributes.get('checked', False)
        value = self._attributes.get('value', True)
        if type(value) == bool:
            default = value and checked_by_default
        else:
            default = value if checked_by_default else None
        return default

    def render(self):
        format_values = {
            'trait_name': self.trait_name,
            'label': self.label,
            'attributes': self._render_attribute_list(),
        }
        return self.template.format(**format_values)

    def get_trait(self):
        """
        Returns either a Bool or Unicode trait depending on the type of the value associated with
        the field. If no value was provided, a Bool is returned.
        """
        checkbox_value = self._attributes.get('value', True)
        value_type = type(checkbox_value)
        trait_class = Bool if value_type == bool else Unicode

        default_value = self.default_value
        trait_kwargs = {}
        trait_kwargs['default_value'] = default_value
        if default_value == None:
            trait_kwargs['allow_none'] = True
        trait = trait_class(**trait_kwargs)
        trait = trait_class()
        trait.name = self.trait_name
        trait.tag(config=True)

        return trait

    def normalize_user_option(self, option):
        """
        Returns a boolean if no `attr_value` is found, otherwise returns the `attr_value` if
        checked, or a NoneType. Raises a ValueError if the field is required but unchecked.
        """
        is_checked = option != None

        if not is_checked and self.required:
            error_message = 'Required field cannot be empty: {}.'.format(self.label)
            raise ValueError(error_message)

        value = self._attributes.get('value', True)
        if type(value) == bool:
            normalized = is_checked
        else:
            normalized = value if is_checked else None
        return normalized
