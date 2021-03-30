from cbg.common import *
from cbg.wrapper.wrapper_generator import WrapperGenerator

def _generate_class(self:WrapperGenerator, code:Code, class_:Class):
    for func in class_.functions: self._generate_function(code, func, class_)
    for prop in class_.properties: self._generate_property(code, prop, class_)
    self._generate_function(code, Function('AddRef'), class_)
    self._generate_function(code, Function('Release'), class_)

WrapperGenerator._generate_class = _generate_class