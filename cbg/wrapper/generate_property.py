from cbg.common import *
from cbg.wrapper.wrapper_generator import WrapperGenerator

def _generate_property(self:WrapperGenerator, code:Code, prop:Property, class_:Class):
    if prop.has_getter: self._generate_function(code, prop.getter_as_func(), class_)
    if prop.has_setter: self._generate_function(code, prop.setter_as_func(), class_)

WrapperGenerator._generate_property = _generate_property