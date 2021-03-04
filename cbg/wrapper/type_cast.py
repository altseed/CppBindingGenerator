import ctypes
from typing import TypeVar
from cbg.common import *
import cbg.wrapper.generate_wrapper as gen_wrapper
import cbg.wrapper.type_name as type_name

# 入力された型をC++形式にキャストする処理を文字列で取得
T = TypeVar('T')
def _type_cast(type_:T, name:str, definition:Definition):
    if type_ in [ctypes.c_byte, int, float, bool, ctypes.c_wchar_p, ctypes.c_void_p] + definition.structs:
        return name
    elif type_ in definition.classes:
        generator = gen_wrapper.WrapperGenerator()
        func_name = generator.shared_ptr_creator_name
        type_name = type_name._get_cpp_fullname(type_, definition)
        return '{0}<{1}>(({1}*){2})'.format(func_name, type_name, name)
    elif type_ in definition.enums:
        return '({}::{}){}'.format(type_.namespace, type_.name, name)
    for dependency in type_.dependencies:
        if dependency.define.classes:
            generator = gen_wrapper.WrapperGenerator()
            func_name = generator.shared_ptr_creator_name_dependence
            type_name = type_name._get_cpp_fullname(type_, definition)
            return '{0}<{1}>(({1}*){2})'.format(func_name, type_name, name)
        if dependency.define.enums:
            return '({}::{}){}'.format(type_.namespace, type_.name, name)
    assert(False)

# 戻り値をC++形式にキャストする処理を文字列で取得
U = TypeVar('U')
def _return_cast(type_:T, name:str, definition:Definition):
    if type_ in [ctypes.c_byte, int, float, bool, ctypes.c_wchar_p, ctypes.c_void_p]:
        return name
    elif type_ in definition.classes:
        generator = gen_wrapper.WrapperGenerator()
        func_name = generator.shared_ptr_getter_name
        type_name = type_name._get_cpp_fullname(type_, definition)
        return '{0}<{1}>(({1}*){2})'.format(func_name, type_name, name)
    elif type_ in definition.structs:
        return '({})'.format(name)
    elif type_ in definition.enums:
        return '(int32_t){}'.format(name)
    for dependency in type_.dependencies:
        if type_ in definition.classes:
            generator = gen_wrapper.WrapperGenerator()
            func_name = generator.shared_ptr_getter_name_dependence
            type_name = type_name._get_cpp_fullname(type_, definition)
            return '{0}<{1}>(({1}*){2})'.format(func_name, type_name, name)
        elif type_ in definition.structs:
            return '({})'.format(name)
        elif type_ in definition.enums:
            return '(int32_t){}'.format(name)
        assert(False)
    return name
