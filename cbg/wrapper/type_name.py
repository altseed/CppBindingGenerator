import ctypes
from typing import TypeVar
from cbg.common.definition import Definition
from cbg.common.options import ArgCalledBy
from cbg.common.class_ import Class
from cbg.common.enum import Enum
from cbg.common.struct import Struct

# 入力された型をC++形式で文字列で取得
T = TypeVar('T')
def _get_cpp_type(type_:T, definition:Definition, called_by:ArgCalledBy = None):
    ptr = '*' if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref else ''
    if type_ == ctypes.c_byte: return 'int8_t' + ptr
    if type_ == int: return 'int32_t' + ptr
    if type_ == float: return 'float' + ptr
    if type_ == bool: return 'bool' + ptr
    if type_ == ctypes.c_wchar_p: return 'const char16_t*'
    if type_ == ctypes.c_void_p: return 'void*'
    if isinstance(type_, Class): return 'std::shared_ptr<{}>'.format(_get_cpp_fullname(type_, definition))
    if isinstance(type_, Struct): return _get_cpp_fullname(type_, definition) + ptr
    if isinstance(type_, Enum): return _get_cpp_fullname(type_, definition)
    if type_ is None: return 'void'
    raise ValueError("{} is not supported in cpp.".format(str(type_)))

# 入力された型をC言語形式で文字列で取得
U = TypeVar('U')
def _get_c_type(type_:U, definition:Definition, called_by:ArgCalledBy = None):
    ptr = '*' if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref else ''
    if type_ == ctypes.c_byte: return 'int8_t' + ptr
    if type_ == int: return 'int32_t' + ptr
    if type_ == float: return 'float' + ptr
    if type_ == bool: return 'bool' + ptr
    if type_ == ctypes.c_wchar_p: return 'const char16_t*'
    if type_ == ctypes.c_void_p: return 'void*'
    if isinstance(type_, Class): return 'void*'
    if isinstance(type_, Struct): return _get_cpp_fullname(type_, definition) + ptr
    if isinstance(type_, Enum): return 'int32_t'
    if type_ is None: return 'void'
    raise ValueError("{} is not supported in clang.".format(str(type_)))

# クラスや列挙型や構造体の型名を名前空間を含めて文字列で取得
V = TypeVar('V')
def _get_cpp_fullname(type_:V, definition:Definition):
    for dependency in definition.dependencies:
        if type_ in dependency.define.classes:
            if dependency.namespace == '': return type_.name
            return dependency.namespace + '::' + type_.name
    if type_.namespace == '': return type_.name
    return type_.namespace + '::' + type_.name
