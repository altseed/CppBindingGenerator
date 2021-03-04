from cbg.common import *
import cbg.wrapper.generate_function as gen_function

def _generate_property(code:Code, prop:Property, class_:Class, definition:Definition):
    if prop.has_getter:
        gen_function._generate_function(code, prop.getter_as_func(), class_, definition)
    if prop.has_setter:
        gen_function._generate_function(code, prop.setter_as_func(), class_, definition)