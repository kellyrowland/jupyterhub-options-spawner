# Copyright (c) 2018, Zebula Sampedro, CU Boulder Research Computing

import abc



class OptionsForm:
    """
    Instances of this class are used to render a spawner options form for a set of form fields.
    """

    validation_style = ("""<style>.form-control:invalid {border-color:red;color:red;}</style>\n""")

    def __init__(self, form_fields=[]):
        """Takes an optional list of FormField subclasses and initializes a form builder."""
        self._fields = form_fields

    @property
    def fields(self):
        return self._fields

    def render(self):
        rendered_fields = [self.validation_style]
        for field in self._fields:
            rendered_fields.append(field.render())
        return '\n'.join(rendered_fields)

    def get_options_from_form(self, form_data):
        """Returns parsed user options from form data."""
        options = {}
        for field in self._fields:
            value = form_data.get(field.trait_name, None)
            options[field.trait_name] = value
        return options

    def get_normalized_user_options(self, user_options):
        """
        Takes user options from spawner and returns the values normalized for the
        traitlet associated with each form field.
        """
        normalized_options = {}
        for field in self._fields:
            trait_name = field.trait_name
            option = user_options.get(trait_name, None)
            normalized_option = field.normalize_user_option(option)
            normalized_options[trait_name] = normalized_option
        return normalized_options


class FormField(abc.ABC):
    """
    Abstract base class for form fields.
    """

    @abc.abstractmethod
    def __init__(self, trait_name, label=None, **kwargs):
        """
        This constructor will accept HTML5 input attributes as keyword arguments and
        apply them to the rendered field. These attributes must be prefixed by `attr`.
        Example: to specify an email input, provide `attr_type='email'` as a parameter.
        """
        self._trait_name = trait_name
        self._label = label or trait_name
        self._attributes = {}
        for key in [k for k in kwargs.keys() if k.startswith('attr_')]:
            attribute_name = key[5:]
            self._attributes[attribute_name] = kwargs.pop(key)
        if 'name' not in self._attributes:
            self._attributes['name'] = trait_name

    @property
    def trait_name(self):
        return self._trait_name

    @property
    def label(self):
        return self._label

    @property
    def default_value(self):
        value = self._attributes.get('value', None)
        return value

    @property
    def required(self):
        required = self._attributes.get('required', False)
        return required

    def _render_attribute_list(self):
        """
        Renders the field attributes in a format appropriate for direct insertion into
        a rendered for field.
        """
        rendered_attributes = []
        for attribute in sorted(self._attributes.keys()):
            value = self._attributes[attribute]
            if type(value) == bool:
                rendered_attribute = attribute * value
            else:
                rendered_attribute = '{}="{}"'.format(attribute, value)
            rendered_attributes.append(rendered_attribute)
        return ' '.join([val for val in rendered_attributes if val])

    @abc.abstractmethod
    def render(self):
        """Returns a string representing the form field rendered to HTML."""
        pass

    @abc.abstractmethod
    def get_trait(self):
        """Returns an appropriately configured Traitlet for this form field."""
        pass

    @abc.abstractmethod
    def normalize_user_option(self, option):
        """Returns the normalized value for the field trait given a user option."""
        pass
