# Copyright (c) 2018, Zebula Sampedro, CU Research Computing

import logging
import os
import signal
import sys
import tempfile
import time
import unittest
import contextlib
from getpass import getuser
from traitlets.config.loader import Config
from traitlets import (
    Unicode,
    Float,
)

from jupyterhub.spawner import LocalProcessSpawner
from jupyterhub import orm

from optionsspawner import OptionsFormSpawner
from optionsspawner.forms import (
    OptionsForm,
    TextInputField,
    NumericalInputField,
)



_echo_sleep = """
import sys, time
print(sys.argv)
time.sleep(10)
"""

@contextlib.contextmanager
def suppress_output():
    """Prevent noisy spawners from cluttering the test logs."""
    with open(os.devnull, "w") as devnull:
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = original_stdout
            sys.stderr = original_stderr

def get_db():
    """Get a db session"""
    db = orm.new_session_factory('sqlite:///:memory:', echo=True)()
    user = orm.User(
        name=getuser(),
        server=orm.Server(),
    )
    hub = orm.Hub(
        server=orm.Server(),
    )
    db.add(user)
    db.add(hub)
    db.commit()
    return db

def get_config(**kwargs):
    """
    Returns reasonable default config for spawners. Values can be added or modified via kwargs.
    """
    default_config = {
        'JupyterHub': {
            'spawner_class': 'optionsspawner.OptionsFormTestSpawner',
        },
        'OptionsFormSpawner': {
            'form_fields': [],
            'child_class': 'jupyterhub.spawner.LocalProcessSpawner',
            'child_config': {},
        },
        'Spawner': {
            'notebook_dir': '/',
            'start_timeout': 10,
            'default_url': '/tree/home/{username}',
            'http_timeout': 10,
        }
    }
    default_config.update(kwargs)
    return Config(default_config)

def new_spawner(db=None, spawner_class=OptionsFormSpawner, **kwargs):
    """Create a new spawner instance."""
    if not db:
        db = get_db()
    kwargs.setdefault('cmd', [sys.executable, '-c', _echo_sleep])
    kwargs.setdefault('user', db.query(orm.User).first())
    kwargs.setdefault('hub', db.query(orm.Hub).first())
    kwargs.setdefault('notebook_dir', os.getcwd())
    kwargs.setdefault('default_url', '/user/{username}/lab')
    kwargs.setdefault('poll_interval', 1)
    return spawner_class(db=db, **kwargs)


class OptionsFormSpawnerTestCase(unittest.TestCase):
    """Tests for optionsspawner.optionsspawner.OptionsFormSpawner"""

    def test_apply_traits_to_spawner(self):
        field1 = TextInputField('test_attr_text',
            label='Test Text',
            attr_value='default'
        )
        field2 = NumericalInputField('test_attr_numerical',
            label='Test Numerical',
            attr_value=2,
            attr_step='any'
        )
        form_fields = [field1, field2]
        config = get_config()
        config['OptionsFormSpawner']['form_fields'] = form_fields
        with suppress_output():
            spawner = new_spawner(config=config)

        spawner._apply_traits_from_fields()
        self.assertTrue(spawner.has_trait('test_attr_text'))
        self.assertTrue(spawner.has_trait('test_attr_numerical'))

    def test_set_trait_values_on_spawner(self):
        field1 = TextInputField('test_attr_text',
            label='Test Text',
            attr_value='default'
        )
        field2 = NumericalInputField('test_attr_numerical',
            label='Test Numerical',
            attr_value=2,
            attr_step='any'
        )
        form_fields = [field1, field2]
        config = get_config()
        config['OptionsFormSpawner']['form_fields'] = form_fields
        with suppress_output():
            spawner = new_spawner(config=config)

        spawner.user_options = {
            'test_attr_text': ['not_default'],
            'test_attr_numerical': [4.0]
        }
        spawner._set_trait_values_from_options()
        self.assertEqual(spawner.test_attr_text, 'not_default')
        self.assertEqual(spawner.test_attr_numerical, 4.0)


if __name__ == '__main__':
    unittest.main()
