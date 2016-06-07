# -*- coding: utf-8 -*-

"""
    frink.types
    ~~~~~~~~~~~~~
    Extensions of Schematics BaseType to handle relationships.
"""

from schematics.types import BaseType

from frink.registry import model_registry

import logging
log = logging.getLogger(__name__)


class HasOne(BaseType):
    """
        For use when your model has a thing.
        Pass model_class as a str if you have issues with circular imports.
    """
    def __init__(self, model_class, **kwargs):
        if isinstance(model_class, str):
            # We need to defer initialising this relationship until the
            # model is initialised
            pass
        else:
            log.debug(model_class)
            self._initialise(model_class, **kwargs)

    def __repr__(self):
        return object.__repr__(self)[:-1] + ' for %s>' % self.model_class

    def _initialise(self, model_class, **kwargs):
        log.debug('HasOne.__init__')
        self.model_class = model_class
        self.fields = self.model_class.fields

        validators = kwargs.pop("validators", [])
        self.strict = kwargs.pop("strict", True)

        def validate_model(model_instance):
            model_instance.validate()
            return model_instance

        super(HasOne, self).__init__(validators=[validate_model] + validators, **kwargs)
