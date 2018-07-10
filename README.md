# JupyterHub Options Form Spawner
---
This spawner makes it possible to add an options form to _almost_ any spawner using only JupyterHub configuration, no subclassing required. The options form that is rendered uses HTML5 form validation and applies form values as spawner attributes.

## Installing
To install the `OptionsFormSpawner`, clone the repo and install via pip:
```
pip3 install .
```

## Configuring
The `OptionsFormSpawner` is a subclass of [wrapspawner](https://github.com/jupyterhub/wrapspawner) that adds an additional spawner attribute called `form_fields`, which is a list of option form field instances that you want the spawner to render.

### Basic Example
This is a basic configuration that allow user-definition of the following spawner attributes:
* `LocalProcessSpawner.text_attribute`: A Unicode trait
* `LocalProcessSpawner.select_attribute`: A Float trait

```python
from optionsspawner.forms import (
    TextInputField,
    SelectField,
)

c.JupyterHub.spawner_class = 'optionsspawner.OptionsFormSpawner'
c.OptionsFormSpawner.child_class = 'jupyterhub.spawner.LocalProcessSpawner'
c.OptionsFormSpawner.child_config = {}

test_input = TextInputField('text_attribute',
    label="A required unicode value",
    attr_value='Default value',
    attr_required=True
)

test_select = SelectField('select_attribute',
    label='Select one',
    attr_required=True,
    choices=[(1.0, 'Option 1'), (2.0, 'Option 2')],
    default=2.0
)

c.OptionsFormSpawner.form_fields = [
    test_input,
    test_select,
]
```

### Available Fields
The optionsspawner module provides the below form fields for your configuration. Each field allows for direct access to its associated HTML5 API via keyword arguments to the field constructor. these keyword arguments are the name of the HTML input or select attribute, prefixed by `attr_`.

**Note:** This API is meant to be as permissive as possible, particularly in regards to direct access to the underlying HTML5 form API. The field instances will not check that each attribute, nor combinations of attributes are valid.

#### optionsspawner.forms.TextInputField
Form field for text inputs associated with a Unicode trait. This field will support any text-based input field and attributes.
```python
email_input = TextInputField('user_email',
    label="A required email field",
    attr_type='email',
    attr_placeholder='Please enter your email address',
    attr_required=True
)
```

#### optionsspawner.forms.NumericalInputField
Form field for numerical inputs associated with either Integer or Float traits. This field will support any numerical input field and attributes.
```python
# This will be applied to the spawner as a Float trait
scaling_factor_input = NumericalInputField('scaling_factor',
    label="Scaling Factor",
    attr_min=0,
    attr_max=2,
    attr_step=0.1
)
```

#### optionsspawner.forms.CheckboxInputField
Form field for checkbox inputs. If `attr_value` is provided, then a trait matching the type of that value will be returned, either a Bool or Unicode. Otherwise, a Bool trait will be returned. Unlike the other field types, `attr_value` corresponds to the value of the field if it is checked, and does not influence the actual state of the checkbox. To initialize a checked checkbox, set `attr_checked=True`.
```python
terms_conditions_accept_input = CheckboxInputField('accepted_toc',
    label="I agree to the Terms and Conditions",
    attr_required=True
)

exclusive_mode_input = CheckboxInputField('exclusive_mode',
    label="Spawn in exclusive mode.",
    attr_value='exclusive',
    attr_checked=True
)
```

#### optionsspawner.forms.SelectField
Form field for select inputs. A trait matching the type of the choices will be returned. Takes two special keyword arguments in addition to HTML attributes:
* `choices`: tuple of (value, label) pairs that the rendered select options will represent.
* `default`: the value of the choice selected by default. If no default defined, the first choice will be selected.

**Note:** `attr_value` should not be specified on this field, and will have no effect.
```python
qos_select = SelectField('req_qos',
    label='Select a QoS',
    attr_required=True,
    choices=[('debug', 'Debug'), ('normal', 'Normal')],
    default='normal'
)
```

## Dev Installation
Clone the repo and install editable:
```
pip3 install -e .
```
To run tests, navigate to the repository root and run:
```
python -m unittest discover tests/
```
