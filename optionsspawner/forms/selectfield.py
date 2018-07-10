# Copyright (c) 2018, Zebula Sampedro, CU Boulder Research Computing

from traitlets import (
    Unicode,
    Integer,
    Float,
)
from .base import FormField



class SelectField(FormField):
    """
    Form field for select inputs. A trait matching the type of the choices will be returned. Takes
    two special keyword arguments in addition to HTML attributes:
    * choices: tuple of (value, label) pairs that the rendered select options will represent.
    * default: the value of the choice selected by default. If no default defined, the first
               choice will be selected.

    NOTE: `attr_value` should not be specified on this field, and will have no effect.
    """

    select_template = ("""<label for="{trait_name}">{label}</label>\n"""
    """<select id="id_{trait_name}" class="form-control" {attributes}>\n"""
    """{options}"""
    """</select>\n""")

    option_template = ("""<option id="id_{trait_name}_option_{enumeration}" value="{value}"{selected}>{display}</option>\n""")

    def __init__(self, *args, choices=[], default=None, **kwargs):
        """
        All choices must be of the same type.
        """
        kwargs.pop('attr_value', None)
        # Multiselection isn't supported yet.
        kwargs.pop('attr_multiple', None)
        self._choices = choices
        choice_values = [choice[0] for choice in choices]

        if len(set(choice_values)) < len(choice_values):
            raise ValueError('All choice values must be unique.')
        if len(set(type(val) for val in choice_values)) > 1:
            raise TypeError('All types in select options must be the same.')

        self._default_value = default if default in choice_values else choice_values[0]
        super().__init__(*args, **kwargs)

    @property
    def default_value(self):
        return self._default_value

    def _render_options(self, choices):
        rendered_options = []
        for i in range(len(self._choices)):
            value, display = self._choices[i]
            selected = ' selected' if value == self.default_value else ''
            rendered_option = self.option_template.format(
                value=value,
                display=display,
                selected=selected,
                trait_name=self.trait_name,
                enumeration=i
            )
            rendered_options.append(rendered_option)

        return ''.join(rendered_options)

    def render(self):
        rendered_options = self._render_options(self._choices)
        attributes = self._render_attribute_list()
        rendered_select = self.select_template.format(
            trait_name=self.trait_name,
            label=self.label,
            attributes=attributes,
            options=rendered_options
        )
        return rendered_select

    def get_trait(self):
        """
        Returns one of Unicode, Integer, or Float traits dependent upon the type of the field
        choices.
        """
        trait_class = Unicode
        value, _ = self._choices[0]
        if isinstance(value, int):
            trait_class = Integer
        elif isinstance(value, float):
            trait_class = Float

        trait_kwargs = {}
        if self.default_value:
            trait_kwargs['default_value'] = self.default_value
        trait = trait_class(**trait_kwargs)
        trait.name = self.trait_name
        trait.tag(config=True)

        return trait

    def normalize_user_option(self, option):
        """
        Returns the option as a Unicode, Integer, or Float, dependent upon the traitlet
        associated with this field. Raises a ValueError if the value cannot be converted, or
        if the selection is not present in the choice list.
        """
        value = option[0]
        traitlet = self.get_trait()
        value_type = str
        if isinstance(traitlet, Integer):
            value_type = int
        elif isinstance(traitlet, Float):
            value_type = float

        try:
            selection = value_type(value)
        except ValueError:
            error_message = 'Cannot convert to {}: {}'.format(value_type, value)
            raise ValueError(error_message)

        choice_values = [choice[0] for choice in self._choices]
        if selection not in choice_values:
            error_message = 'Invalid selection: {}'.format(selection)
            raise ValueError(error_message)

        normalized_option = selection
        return normalized_option
