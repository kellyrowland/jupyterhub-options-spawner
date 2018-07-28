# Copyright (c) 2018, Zebula Sampedro, CU Boulder Research Computing

from traitlets import (
    Unicode,
    Bool,
    Integer,
    Float,
)
from .base import FormField



class TextInputField(FormField):
    """
    Form field for text inputs associated with a Unicode trait. This field will
    support any text-based input field and attributes.
    """

    template = ("""<label for="{trait_name}">{label}</label>\n"""
    """<input id="id_{trait_name}" class="form-control" {attributes}>\n""")

    def __init__(self, *args, attr_type='text', **kwargs):
        """Defaults to a text input with no validation."""
        super().__init__(*args, attr_type=attr_type, **kwargs)

    @property
    def default_value(self):
        value = self._attributes.get('value', '')
        return value

    def render(self):
        format_values = {
            'trait_name': self.trait_name,
            'label': self.label,
            'attributes': self._render_attribute_list(),
        }
        return self.template.format(**format_values)

    def get_trait(self):
        """
        Returns a Unicode traitlet for this field configuration.
        """
        trait_class = Unicode

        trait_kwargs = {}
        trait_kwargs['default_value'] = self.default_value
        trait = trait_class(**trait_kwargs)
        trait.name = self.trait_name
        trait.tag(config=True)

        return trait

    def normalize_user_option(self, option):
        """
        Returns the option as Unicode. Returns and empty string if handed an empty string or
        NoneType and no default has been set for the field. Raises a ValueError if this field is
        required but empty.
        """
        value = option[0]
        if not value:
            normalized_option = self.default_value
        elif not type(value) == str:
            normalized_option = str(value)
        else:
            normalized_option = value

        if self.required and not normalized_option:
            error_message = 'Required field cannot be empty: {}.'.format(self.label)
            raise ValueError(error_message)

        return normalized_option

class NumericalInputField(TextInputField):
    """
    Form field for numerical inputs associated with either Integer or Float traits. This field
    will support any numerical input field and attributes.
    """

    def __init__(self, *args, attr_type='number', **kwargs):
        """Defaults to a numerical input with no validation."""
        super().__init__(*args, attr_type=attr_type, **kwargs)

    def get_trait(self):
        """
        Returns either an Integer or Float traitlet for this field configuration.
        """
        is_float = False
        if 'step' in self._attributes:
            step = self._attributes['step']
            is_float = type(step) == float or step == 'any'

        trait_class = Float if is_float else Integer

        trait_kwargs = {}
        if self.default_value:
            trait_kwargs['default_value'] = self.default_value
        trait = trait_class(**trait_kwargs)
        trait.name = self.trait_name
        trait.tag(config=True)

        return trait

    def normalize_user_option(self, option):
        """
        Returns the option as either an Integer or a Float, dependent upon the traitlet
        associated with this field. Returns None if handed a NoneType and no default is set.
        Raises a ValueError if field is required but option is None, or if the value cannot be converted.
        """
        value = option[0]
        traitlet = self.get_trait()
        value_type = int if isinstance(traitlet, Integer) else float
        if value == None or value == '':
            normalized_option = self.default_value or None
        elif not type(value) == value_type:
            try:
                normalized_option = value_type(value)
            except ValueError:
                error_message = 'Cannot convert to {}: {}'.format(value_type, value)
                raise ValueError(error_message)
        else:
            normalized_option = value

        if normalized_option == None and self.required:
            error_message = 'Required field cannot be empty: {}.'.format(self.label)
            raise ValueError(error_message)

        return normalized_option
