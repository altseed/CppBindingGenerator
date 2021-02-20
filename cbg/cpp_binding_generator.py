from typing import List
import ctypes
import enum
import json
import copy

# Data structure
# Define
# └─Enum
#   └─EnumValue
# └─Class
#   └─Description
#   └─Property
#   └─Function { return_type, is_static, is_constructor }
#     └─Description(brief)
#     └─Description(desc)
#     └─Argument { type, name }
#       └─Description
# └─Struct
#   └─Description
#   └─Field


class Description:
    '''
    a description for any objects    
    '''

    def __init__(self):
        self.descs = {'ja': '', 'en': ''}

    def add(self, lang: str, desc: str):
        '''
        add a description

        Parameters
        ----------
        lang : str
            language(ja,en)

        desc : str
            a description

        '''
        self.descs[lang] = desc


class ArgCalledBy(enum.Enum):
    Default = 1
    Ref = 2
    Out = 3


class Argument:
    '''
    an argument of function    
    '''

    def __init__(self, type_, name: str, called_by: ArgCalledBy = ArgCalledBy.Default):
        '''
        add a description

        Parameters
        ----------
        type
            the type of argument

        name : str
            name

        '''

        self.type_ = type_
        self.name = name
        self.brief = None  # type: Description
        self.called_by = called_by
        self.nullable = True

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name


Arguments = List[Argument]


class CacheMode(enum.Enum):
    NoCache = 1
    Cache = 2
    ThreadSafeCache = 3


class ReturnValue:
    def __init__(self, type_):
        self.type_ = type_
        self.brief = None  # type: Description
        self.desc = None  # type: Description

    def cache_mode(self) -> CacheMode:
        if self.type_ != Class:
            return CacheMode.NoCache
        return self.type_.cache_mode

    def __str__(self):
        return 'return'

class Function:
    '''
    an argument of function

    Parameters
    ----------
        targets
            target languages to export it. if this is empty, functions are exported to all languages
    '''

    def __init__(self, name: str):
        self.name = name
        self.brief = None  # type: Description
        self.desc = None  # type: Description
        self.args = []  # type: Arguments
        self.return_value = ReturnValue(None)
        self.is_static = False
        self.is_constructor = False
        self.is_public = True
        self.onlyExtern = False
        self.is_overload = False
        self.targets = []

    def add_arg(self, type_, name: str) -> Argument:
        arg = Argument(type_, name)
        self.args.append(arg)
        return arg

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name


Functions = List[Function]


class Property:
    def __init__(self, type_, name: str, has_getter: bool, has_setter: bool):
        self.type_ = type_
        self.name = name
        self.has_getter = has_getter
        self.has_setter = has_setter
        self.brief = None  # type: Description
        self.cache_set_value = False
        self.serialized = False
        self.is_public = True
        self.null_deserialized = True
        self.nullable = True
        self.onlyExtern = False

    def getter_as_func(self) -> Function:
        f = Function('Get' + self.name)
        f.return_value = ReturnValue(self.type_)
        return f

    def setter_as_func(self) -> Function:
        f = Function('Set' + self.name)
        f.add_arg(self.type_, 'value')
        return f

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name


class EnumValue:
    def __init__(self, name: str, value=None):
        self.name = name
        self.desc = None  # type: Description
        self.brief = None  # type: Description
        self.value = value

    def __str__(self):
        return self.name

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self


class Enum:
    def __init__(self, namespace: str, name: str, alias:str=None):
        self.brief = None  # type: Description
        self.values = []  # type: List[EnumValue]
        self.name = name
        self.alias = alias
        self.namespace = namespace
        self.isFlag = False

    def add(self, name: str, value=None) -> EnumValue:
        '''
        add an enum value
        '''
        v = EnumValue(name, value)
        self.values.append(v)
        return v

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name


Enums = List[Enum]


class Field:
    def __init__(self, type_, name: str):
        self.brief = None  # type: Description
        self.name = name
        self.type_ = type_


Fields = List[Field]


class Struct:
    def __init__(self, namespace='', name='', alias=''):
        self.namespace = namespace
        self.name = name
        self.alias = alias
        self.fields = []  # type: Fields
        self.brief = None  # type: Description

    def add_field(self, type_, name: str):
        field = Field(type_, name)
        self.fields.append(field)

    def cpp_fullname(self) -> str:
        if self.namespace == '':
            return self.name

        return self.namespace + '::' + self.name

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name


Structs = List[Struct]


class Class:
    def __init__(self, namespace='', name='', cache_mode: CacheMode = CacheMode.Cache):
        self.namespace = namespace  # type: str
        self.name = name  # type: str
        self.alias = None # type: str
        self.funcs = []  # type: Functions
        self.properties = []  # type: List[Property]
        self.base_class = None  # type: Class
        self.constructor_count = 0
        self.cache_mode = cache_mode
        self.brief = None  # type: Description
        self.is_public = True
        self.SerializeType = SerializeType.Disable
        self.CallBackType = CallBackType.Disable
        self.is_Sealed = False
        self.handleCache = True

    def add_constructor(self) -> Function:
        func = Function('Constructor_' + str(self.constructor_count))
        func.is_constructor = True
        func.return_value = ReturnValue(self)
        self.funcs.append(func)
        self.constructor_count += 1
        return func

    def add_func(self, name: str) -> Function:
        func = Function(name)
        self.funcs.append(func)
        return func

    def add_property(self, type_, name: str) -> Property:
        property = Property(type_, name, False, False)
        self.properties.append(property)
        return property

    def __enter__(self):
        return self

    def __exit__(self, exit_type, exit_value, traceback):
        return self

    def __str__(self):
        return self.name


Classes = List[Class]

def merge_str_dict(a, b):
    dst = {}

    def store(d):
        for k, v in d.items():
            if k in dst.keys():
                if isinstance(dst[k],dict) and isinstance(v,dict):
                    dst[k] = merge_str_dict(dst[k], v)
                elif isinstance(dst[k],str) and isinstance(v,str):
                    dst[k] = v
                else:
                    print('Warning : {} is not assigned. type({},{})'.format(k, type(dst[k]), type(v)))
            else:
                dst[k] = copy.deepcopy(v)

    store(a)
    store(b)
    
    return dst

class Define:
    def __init__(self):
        self.enums = [] # type: Enums
        self.classes = []  # type: Classes
        self.structs = []  # type: Structs
        self.text_dicts = {}

    def load_text_from_json_text(self, text):
        dicts = json.loads(text)
        self.text_dicts = merge_str_dict(self.text_dicts, dicts)

    def load_text_from_json_file(self, path):
        json_open = open(path, 'r', encoding='utf8')
        dicts = json.load(json_open)
        self.text_dicts = merge_str_dict(self.text_dicts, dicts)
        
    def get_text(self, lang : str, elements : List, fallback = ''):
        '''
        Get text from dictionary
        '''

        keys = [lang] + [str(e) for e in elements]

        dicts = self.text_dicts
        for key in keys:
            if key in dicts.keys():
                dicts = dicts[key]
            else:
                return fallback

        if "@brief" in dicts.keys():
            return dicts["@brief"]
        return fallback


def __get_cpp_overload_type__(type_, called_by: ArgCalledBy = None) -> str:
    ptr = ''
    if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref:
        ptr = 'p'

    if type_ == ctypes.c_byte:
        return 'byte' + ptr

    if type_ == int:
        return 'int' + ptr

    if type_ == float:
        return 'float' + ptr

    if type_ == bool:
        return 'bool' + ptr

    if type_ == ctypes.c_wchar_p:
        return 'char16p'

    if type_ == ctypes.c_void_p:
        return 'voidp'

    if type(type_) is Class:
        return type_.name

    if type(type_) is Struct:
        return type_.name + ptr

    if type(type_) is Enum:
        return type_.name

    if type_ is None:
        return 'void'

    assert(False)

def __get_c_func_name__(class_: Class, func_: Function) -> str:
    if func_.is_overload:
        return 'cbg_' + class_.name + '_' + func_.name + '_' + '_'.join(map(lambda arg: __get_cpp_overload_type__(arg.type_, arg.called_by), func_.args))
    return 'cbg_' + class_.name + '_' + func_.name

def __get_c_addref_func_name__(class_: Class) -> str:
    return 'cbg_' + class_.name + '_' + 'AddRef'

def __get_c_release_func_name__(class_: Class) -> str:
    return 'cbg_' + class_.name + '_' + 'Release'

class DefineDependency:
    def __init__(self):
        self.namespace = ''
        self.define = None # type: Define

class Code:
    '''
    support to generate a code
    '''

    def __init__(self):
        self.lines = []
        self.indent = 0

    def inc_indent(self):
        self.indent += 1

    def dec_indent(self):
        self.indent -= 1

    def __call__(self, obj):
        self.lines.append((self.indent, obj))

    def __str__(self):
        code = ''
        for line in self.lines:
            indent = line[0]
            o = line[1]

            if isinstance(o, Code):
                ss = str(o).split('\n')

                for s in ss:
                    for i in range(indent):
                        code += '    '
                    code += s
                    code += '\n'

            else:
                for i in range(indent):
                    code += '    '

                code += str(o)
                code += '\n'

        return code


class SharedObjectGenerator:
    def __init__(self, define: Define, dependencies : List[DefineDependency]):
        self.define = define
        self.dependencies = dependencies
        self.output_path = ''

        self.header = ''  # header code inserted
        self.func_name_create_and_add_shared_ptr = 'CreateAndAddSharedPtr'
        self.func_name_add_and_get_shared_ptr = 'AddAndGetSharedPtr'
        self.func_name_create_and_add_shared_ptr_dependence = 'CreateAndAddSharedPtr_Dependence'
        self.func_name_add_and_get_shared_ptr_dependence = 'AddAndGetSharedPtr_Dependence'

    def __get_class_fullname__(self, type_: Class) -> str:
        for dependency in self.dependencies:
            if type_ in dependency.define.classes:
                if dependency.namespace == '':
                    return type_.name

                return dependency.namespace + '::' + type_.name
                
        if type_.namespace == '':
            return type_.name

        return type_.namespace + '::' + type_.name

    def __get_cpp_type__(self, type_, called_by: ArgCalledBy = None) -> str:
        ptr = ''
        if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref:
            ptr = '*'

        if type_ == ctypes.c_byte:
            return 'int8_t' + ptr

        if type_ == int:
            return 'int32_t' + ptr

        if type_ == float:
            return 'float' + ptr

        if type_ == bool:
            return 'bool' + ptr

        if type_ == ctypes.c_wchar_p:
            return 'const char16_t*'

        if type_ == ctypes.c_void_p:
            return 'void*'

        if type_ in self.define.classes:
            return 'std::shared_ptr<{}>'.format(self.__get_class_fullname__(type_))

        if type_ in self.define.structs:
            return type_.cpp_fullname() + ptr

        if type_ in self.define.enums:
            return '{}::{}'.format(type_.namespace, type_.name)

        for dependency in self.dependencies:
            if type_ in dependency.define.classes:
                return 'std::shared_ptr<{}>'.format(self.__get_class_fullname__(type_))

            if type_ in dependency.define.structs:
                return type_.cpp_fullname() + ptr

            if type_ in dependency.define.enums:
                return '{}::{}'.format(type_.namespace, type_.name)

        if type_ is None:
            return 'void'

        assert(False)

    def __get_c_type__(self, type_, is_return=False, called_by: ArgCalledBy = None) -> str:
        ptr = ''
        if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref:
            ptr = ' *'

        if type_ == ctypes.c_byte:
            return 'int8_t' + ptr

        if type_ == int:
            return 'int32_t' + ptr

        if type_ == float:
            return 'float' + ptr

        if type_ == bool:
            return 'bool' + ptr

        if type_ == ctypes.c_wchar_p:
            return 'const char16_t*'

        if type_ == ctypes.c_void_p:
            return 'void*'

        if type_ in self.define.classes:
            return 'void*'

        if type_ in self.define.structs:
            return type_.cpp_fullname() + ptr

        if type_ in self.define.enums:
            return 'int32_t'

        for dependency in self.dependencies:
            if type_ in dependency.define.classes:
                return 'void*'

            if type_ in dependency.define.structs:
                return type_.cpp_fullname() + ptr

            if type_ in dependency.define.enums:
                return 'int32_t'

        if type_ is None:
            return 'void'

        raise ValueError("{} is not supported in cpp.".format(str(type_)))

    def __convert_c_to_cpp__(self, type_, name: str) -> str:
        if type_ == ctypes.c_byte or type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_wchar_p or type_ == ctypes.c_void_p or type_ in self.define.structs:
            return name

        if type_ in self.define.classes:
            return '{}<{}>(({}*){})'.format(self.func_name_create_and_add_shared_ptr, self.__get_class_fullname__(type_), self.__get_class_fullname__(type_), name)

        if type_ in self.define.enums:
            return '({}::{}){}'.format(type_.namespace, type_.name, name)

        for dependency in self.dependencies:
            if dependency.define.classes:
                return '{}<{}>(({}*){})'.format(self.func_name_create_and_add_shared_ptr_dependence, self.__get_class_fullname__(type_), self.__get_class_fullname__(type_), name)

            if dependency.define.enums:
                return '({}::{}){}'.format(type_.namespace, type_.name, name)


        assert(False)

    def __convert_ret__(self, type_, name: str) -> str:
        if type_ == ctypes.c_byte or type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_wchar_p or type_ == ctypes.c_void_p:
            return name

        if type_ in self.define.classes:
            return '(void*){}<{}>({})'.format(self.func_name_add_and_get_shared_ptr, self.__get_class_fullname__(type_), name)

        if type_ in self.define.structs:
            return '({})'.format(name)

        if type_ in self.define.enums:
            return '(int32_t){}'.format(name)

        for dependency in self.dependencies:
            if dependency.define.classes:
                return '(void*){}<{}>({})'.format(self.func_name_add_and_get_shared_ptr_dependence, self.__get_class_fullname__(type_), name)

            if dependency.define.structs:
                return '({})'.format(name)

            if dependency.define.enums:
                return '(int32_t){}'.format(name)


    def __generate_property__(self, class_: Class, prop_: Property) -> str:
        result = ''
        if prop_.has_getter:
            result += self.__generate_func__(class_, prop_.getter_as_func())
        if prop_.has_setter:
            result += self.__generate_func__(class_, prop_.setter_as_func())
        return result

    def __generate_func__(self, class_: Class, func_: Function) -> str:
        code = Code()

        fname = __get_c_func_name__(class_, func_)

        args = [self.__get_c_type__(arg.type_, False, arg.called_by) +
                ' ' + arg.name for arg in func_.args]

        # function name and args
        if not func_.is_static and not func_.is_constructor:
            args = ['void* cbg_self'] + args

        # function header
        if func_.is_constructor:
            code('CBGEXPORT ' + self.__get_c_type__(class_, is_return=True) + ' CBGSTDCALL ' +
                 fname + '(' + ', '.join(args) + ') {')
        else:
            code('CBGEXPORT ' + self.__get_c_type__(func_.return_value.type_, is_return=True) + ' CBGSTDCALL ' +
                 fname + '(' + ', '.join(args) + ') {')
        code.inc_indent()

        count = 0
        args = []

        if not func_.is_static and not func_.is_constructor:
            code(
                'auto cbg_self_ = ({}*)(cbg_self);\n'.format(self.__get_class_fullname__(class_)))

        # convert ctype into c++type
        for arg in func_.args:
            ex_name = 'cbg_arg' + str(count)
            
            if arg.type_ in self.define.structs and arg.called_by != ArgCalledBy.Default:
                cpp_type = '{}::{}*'.format(arg.type_.namespace, arg.type_.alias)
                c_value = '({})'.format(cpp_type) + arg.name
                code('{} {} = {};'.format(cpp_type, ex_name, c_value))
            else:
                cpp_type = self.__get_cpp_type__(arg.type_, arg.called_by)
                c_value = self.__convert_c_to_cpp__(
                    arg.type_, arg.name)
                code('{} {} = {};'.format(cpp_type, ex_name, c_value))
            args.append(ex_name)
            count += 1

        # call function and return
        if func_.is_constructor:
            class_fullname = self.__get_class_fullname__(class_)
            code('return new {}({});'.format(class_fullname, ', '.join(args)))
        else:
            caller = 'cbg_self_->'
            if func_.is_static:
                class_fullname = self.__get_class_fullname__(class_)
                caller = class_fullname + '::'

            if func_.return_value.type_ is None:
                code('{}{}({});'.format(caller, func_.name, ', '.join(args)))
            else:
                return_type = self.__get_cpp_type__(func_.return_value.type_)
                return_value = self.__convert_ret__(
                    func_.return_value.type_, 'cbg_ret')
                code('{} cbg_ret = {}{}({});'.format(
                    return_type, caller, func_.name, ', '.join(args)))
                code('return {};'.format(return_value))

        code.dec_indent()
        code('}')
        code('')

        return str(code)

    def generate(self):

        code = ''

        header = '''\
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//
//   このファイルは自動生成されました。
//   このファイルへの変更は消失することがあります。
//
//   THIS FILE IS AUTO GENERATED.
//   YOUR COMMITMENT ON THIS FILE WILL BE WIPED.
//
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#include <stdint.h>
#include <stdio.h>

#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#include <Windows.h>
#endif

#ifndef CBGEXPORT
#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#define CBGEXPORT __declspec(dllexport)
#else
#define CBGEXPORT
#endif
#endif

#ifndef CBGSTDCALL
#if defined(_WIN32) || defined(__WIN32__) || defined(__CYGWIN__)
#define CBGSTDCALL __stdcall
#else
#define CBGSTDCALL
#endif
#endif

'''

        code += header

        code += self.header

        code += '''\

extern "C" {

'''

        for class_ in self.define.classes:
            for func in class_.funcs:
                code += self.__generate_func__(class_, func)

            for prop in class_.properties:
                code += self.__generate_property__(class_, prop)

            # generate addref
            addref_func = Function('AddRef')
            code += self.__generate_func__(class_, addref_func)

            # generate release
            release_func = Function('Release')
            code += self.__generate_func__(class_, release_func)

        footer = '''\

}

'''

        code += footer

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(self.output_path, mode='w', encoding='utf-8', newline="\n") as f:
                f.write(code)

class BindingGenerator:
    def __init__(self, define: Define):
        self.define = define

    def generate(self):
        return

class SerializeType(enum.IntEnum):
    Disable = 0
    AttributeOnly = 1
    Interface = 2
    Interface_Usebase = 3

class CallBackType(enum.IntEnum):
    Disable = 0
    Enable = 1
    Enable_Usebase = 2
