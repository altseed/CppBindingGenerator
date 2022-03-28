import cbg
import ctypes
import sys

# Struct
StructA = cbg.Struct('HelloWorld', 'StructA_C', 'StructA')
with StructA as struct:
    struct.add_field(float, 'X')
    struct.add_field(float, 'Y')
    struct.add_field(float, 'Z')

ReplaceStructA = cbg.Struct(
    'HelloWorld', 'ReplaceStructA', 'CSReplaceStructA')
with ReplaceStructA as struct:
    struct.add_field(float, 'X')
    struct.add_field(float, 'Y')

# EnumA
EnumA = cbg.Enum('HelloWorld', 'EnumA', 'Animal')
with EnumA as enum:
    enum.add('Mosue')
    enum.add('Cow')
    enum.add('Tiger', '3')

ClassA = cbg.Class('HelloWorld', 'ClassA', cbg.CacheMode.NoCache)
ClassB = cbg.Class('HelloWorld', 'ClassB', cbg.CacheMode.Cache)
ClassC = cbg.Class('HelloWorld', 'ClassC', cbg.CacheMode.ThreadSafeCache)

# ClassC
with ClassC as class_:
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

    with class_.add_property(ctypes.c_wchar_p, 'StringProperty') as prop:
        prop.has_getter = True
        prop.has_setter = True
        prop.brief = cbg.Description()
        prop.brief.add('ja', 'Gets or sets some string.')

    class_.add_property(float, 'MyFloat')

    with class_.add_property(bool, 'MyBool') as prop:
        prop.has_setter = True

    with class_.add_func('FuncHasRefArg') as func:
        with func.add_arg(int, 'intRef') as arg:
            arg.called_by = cbg.ArgCalledBy.Ref

# ClassB
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

    with class_.add_property(ClassA, 'ClassProperty') as prop:
        prop.has_getter = True
        prop.has_setter = True
        prop.brief = cbg.Description()
        prop.brief.add('ja', 'Gets or sets some ClassA.')

    class_.add_property(float, 'MyFloat')

    with class_.add_property(bool, 'MyBool') as prop:
        prop.has_setter = True

# ClassA
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
            arg.called_by = cbg.ArgCalledBy.Ref
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

    with class_.add_func('FuncReturnStatic') as func:
        func.return_value = cbg.ReturnValue(int)
        func.is_static = True

    with class_.add_property(EnumA, 'EnumA') as prop:
        prop.has_getter = True
        prop.has_setter = True

# ClassAlias
ClassAlias = cbg.Class('HelloWorld', 'ClassAlias_Cpp', cbg.CacheMode.NoCache)
with ClassAlias as class_:
    class_.alias = 'ClassAlias_CS'
    class_.add_constructor()
    with class_.add_func('FuncSimple') as func_:
        func_.return_value.type_ = ClassAlias

# Inheritance
BaseClass = cbg.Class('HelloWorld', 'BaseClass', cbg.CacheMode.NoCache)
with BaseClass as class_:
    class_.add_constructor()
    with class_.add_func('GetBaseClassField') as func:
        func.return_value = cbg.ReturnValue(int)
    with class_.add_func('SetBaseClassField') as func:
        func.add_arg(int, 'value')

DerivedClass = cbg.Class('HelloWorld', 'DerivedClass', False)
with DerivedClass as class_:
    class_.add_constructor()
    class_.base_class = BaseClass
    with class_.add_func('GetBaseClassFieldFromDerivedClass') as func:
        func.return_value = cbg.ReturnValue(int)


# define
define = cbg.Define()
define.classes.append(ClassAlias)
define.classes.append(ClassA)
define.classes.append(ClassB)
define.classes.append(ClassC)
define.structs.append(StructA)
define.structs.append(ReplaceStructA)
define.enums.append(EnumA)
define.classes.append(BaseClass)
define.classes.append(DerivedClass)

json_text =  r'''

{
    "en" : {
        "ClassA" : {
            "@brief" : "ClassA-Desc"
        }
    }
}

'''

define.load_text_from_json_text(json_text)

# Cpp

ClassCppD = cbg.Class('HelloWorldCpp', 'ClassCppD', cbg.CacheMode.NoCache)
with ClassCppD as class_:
    class_.add_constructor()
    with class_.add_func('FuncReturnClass') as func:
        func.return_value.type_ = ClassB
        func.return_value.cache = True

define_cpp = cbg.Define()
define_cpp.classes.append(ClassCppD)

