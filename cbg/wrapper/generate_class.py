from cbg.common import *
from cbg.wrapper.wrapper_generator import WrapperGenerator

def _generate_class(self:WrapperGenerator, code:Code, class_:Class, definition:Definition):
    for func in class_.functions:
        self._generate_function(code, func, class_, definition)
    for prop in class_.properties:
        self._generate_property(code, prop, class_, definition)
    self._generate_function(code, Function('AddRef'), class_, definition)
    self._generate_function(code, Function('Release'), class_, definition)

WrapperGenerator._generate_class = _generate_class