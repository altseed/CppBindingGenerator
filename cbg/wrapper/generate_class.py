from cbg.common import *
import cbg.wrapper.generate_function as gen_function
import cbg.wrapper.generate_property as gen_property

def _generate_class(code:Code, class_:Class, definition:Definition):
    for func in class_.functions:
        gen_function._generate_function(code, func, class_, definition)
    for prop in class_.properties:
        gen_property._generate_property(code, prop, class_, definition)
    gen_function._generate_function(code, Function('AddRef'), class_, definition)
    gen_function._generate_function(code, Function('Release'), class_, definition)