# Copyright (c) 2018, Zebula Sampedro, CU Boulder Research Computing

"""
Options Form Spawner
"""

import traitlets
from traitlets.config import LoggingConfigurable
from traitlets import (
    Unicode,
    List,
    Instance,
)
import tornado
import wrapspawner

from .forms import (
    OptionsForm,
    FormField,
)



class OptionsFormSpawner(wrapspawner.WrapSpawner):
    """
    Subclass of WrapSpawner for attaching options form configuration to an arbitrary spawner.
    Configured options form fields will be added as traits to the child_spawner, and will be
    assigned form values when the user submits the form.
    """

    form_fields = List(
        trait=Instance(klass=FormField),
        help="""
        A list of FormField or subclass instances that will be rendered to the spawner options_form.
        The fields will be rendered to the options form in the order they appear in this list.
        """
    ).tag(config=True)

    def __init__(self, *args, **kwargs):
        """Render the options form and sets corresponding traitlets on the spawner."""
        super().__init__(*args, **kwargs)
        self._apply_traits_from_fields()
        self.options_form_builder = OptionsForm(self.form_fields)
        rendered_options_form = self.options_form_builder.render()
        if not self.options_form:
            self.options_form = rendered_options_form

    def options_from_form(self, form_data):
        """Extracts options from form data, and returns a dict of the parsed values."""
        options = self.options_form_builder.get_options_from_form(form_data)
        return options

    def _apply_traits_from_fields(self, spawner_instance=None):
        """Sets traits on a spawner for fields in self.form_fields."""
        if not spawner_instance:
            spawner_instance = self
        traits = {field.trait_name: field.get_trait() for field in self.form_fields}
        spawner_instance.add_traits(**traits)

    def _set_trait_values_from_options(self, spawner_instance=None):
        """Sets the values of traits on a spawner from the options form."""
        if not spawner_instance:
            spawner_instance = self
        normalized_options = self.options_form_builder.get_normalized_user_options(self.user_options)
        for trait_name, value in normalized_options.items():
            setattr(spawner_instance, trait_name, value)

    @tornado.gen.coroutine
    def start(self, *args, **kwargs):
        """Propagates form-defined traits and values to child spawner before starting."""
        self.construct_child()
        self._apply_traits_from_fields(spawner_instance=self.child_spawner)
        self._set_trait_values_from_options(spawner_instance=self.child_spawner)
        super().start(*args, **kwargs)
