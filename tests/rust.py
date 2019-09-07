import cbg
import ctypes
import sys

# Struct
StructA = cbg.Struct('HelloWorld', 'StructA')
with StructA as struct:
    struct.add_field(float, 'X')
    struct.add_field(float, 'Y')
    struct.add_field(float, 'Z')

# EnumA
EnumA = cbg.Enum('HelloWorld', 'EnumA')
with EnumA as enum:
    enum.add('Mosue')
    enum.add('Cow')
    enum.add('Tiger', '3')

# ClassB
ClassB = cbg.Class('HelloWorld', 'ClassB', True)
with ClassB as class_:
    constructor = class_.add_constructor()

    with class_.add_func('SetValue') as func:
        func.add_arg(float, 'value')

    with class_.add_func('SetEnum') as func:
        func.add_arg(EnumA, 'enumValue')

    with class_.add_func('GetEnum') as func:
        func.return_value = cbg.ReturnValue(EnumA)
        func.add_arg(int, 'id')

    with class_.add_property(int, 'MyProperty') as prop:
        prop.has_getter = True
        prop.has_setter = True
        prop.brief = cbg.Description()
        prop.brief.add('ja', 'Gets or sets some integer.')

    class_.add_property(float, 'MyFloat')

    with class_.add_property(bool, 'MyBool') as prop:
        prop.has_setter = True

# ClassA
ClassA = cbg.Class('HelloWorld', 'ClassA', False)
with ClassA as class_:
    class_.add_constructor()
    class_.add_func('FuncSimple')

    with class_.add_func('FuncArgInt') as func:
        func.add_arg(int, 'value')
    
    with class_.add_func('FuncArgFloatBoolStr') as func:
        func.add_arg(float, 'value1')
        func.add_arg(bool, 'value2')
        func.add_arg(ctypes.c_wchar_p, 'value3')

    with class_.add_func('FuncArgStruct') as func:
        with func.add_arg(StructA, 'value1') as arg:
            arg.desc = cbg.Description()
            arg.desc.add('en', 'StructA input.')
        func.brief = cbg.Description()
        func.brief.add('en', 'Processes a structA.')
    
    with class_.add_func('FuncArgClass') as func:
        func.add_arg(ClassB, 'value1')

    with class_.add_func('FuncReturnInt') as func:
        func.return_value = cbg.ReturnValue(int)
        func.brief = cbg.Description()
        func.brief.add('en', 'Returns some integer.')

    with class_.add_func('FuncReturnBool') as func:
        func.return_value.type_ = bool

    with class_.add_func('FuncReturnFloat') as func:
        func.return_value.type_ = float

    with class_.add_func('FuncReturnStruct') as func:
        func.return_value.type_ = StructA

    with class_.add_func('FuncReturnClass') as func:
        func.return_value.type_ = ClassB
        func.return_value.cache = True

    with class_.add_func('FuncReturnString') as func:
        func.return_value.type_ = ctypes.c_wchar_p

    with ClassA.add_property(ClassB, 'BReference') as prop:
        prop.has_getter = True

# define
define = cbg.Define()
define.classes.append(ClassA)
define.classes.append(ClassB)
define.structs.append(StructA)
define.enums.append(EnumA)

# generate
sharedObjectGenerator = cbg.SharedObjectGenerator(define)

sharedObjectGenerator.header = '''
#include "HelloWorld.h"
'''

sharedObjectGenerator.func_name_create_and_add_shared_ptr = 'HelloWorld::CreateAndAddSharedPtr'
sharedObjectGenerator.func_name_add_and_get_shared_ptr = 'HelloWorld::AddAndGetSharedPtr'

sharedObjectGenerator.output_path = 'tests/results/so/so.cpp'
sharedObjectGenerator.generate()

args = sys.argv
lang = 'en'
if len(args) >= 3 and args[1] == '-lang':
    if args[2] in ['ja', 'en']:
        lang = args[2]
    else:
        print('python rust.py -lang [ja|en]')

from cbg.binding_generator_rust import BindingGeneratorRust

bindingGenerator = BindingGeneratorRust(define, lang)
bindingGenerator.output_path = 'tests/results/rust/rust.rs'
bindingGenerator.dll_name = 'Common'
bindingGenerator.namespace = 'HelloWorld'
bindingGenerator.generate()
