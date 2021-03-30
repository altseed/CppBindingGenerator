import ctypes
from typing import TypeVar
from cbg.common import *
from cbg.binding_cpp.binding_generator import BindingGeneratorCPP

# エイリアスを取得
T = TypeVar('T')
def _get_alias_or_name(self:BindingGeneratorCPP, type_:T, definition:Definition):
    namespace = ''
    for dependency in definition.dependencies:
        if type_ in dependency.classes + dependency.structs + dependency.enums:
            namespace = dependency.namespace + '::'
            break
    return namespace + (type_.name if type_.alias == None else type_.alias)

BindingGeneratorCPP._get_alias_or_name = _get_alias_or_name

# 入力された型をC++形式で文字列で取得
U = TypeVar('U')
def _get_cpp_type(self:BindingGeneratorCPP, type_:U, definition:Definition, called_by:ArgCalledBy = None):
    type_str = 'std::shared_ptr<{}>' if called_by in [ArgCalledBy.Out, ArgCalledBy.Ref] else '{}'
    if type_ == ctypes.c_byte: return type_str.format('uint8_t')
    if type_ == int: return type_str.format('int')
    if type_ == float: return type_str.format('float')
    if type_ == bool: return type_str.format('bool')
    if type_ == ctypes.c_wchar_p: return 'std::shared_ptr<char16_t>'
    if type_ == ctypes.c_void_p: return 'void*'
    if isinstance(type_, Class): return 'std::shared_ptr<{}>'.format(self._get_alias_or_name(type_, definition))
    if isinstance(type_, Struct): return type_str.format('{}_C'.format(type_.alias))
    if isinstance(type_, Enum): return self._get_alias_or_name(type_, definition)
    if type_ is None: return 'void'
    raise ValueError("{} is not supported in cpp.".format(str(type_)))

BindingGeneratorCPP._get_cpp_type = _get_cpp_type

# 入力された型をC言語形式で文字列で取得
V = TypeVar('V')
def _get_cppc_type(self:BindingGeneratorCPP, type_:V, definition:Definition, called_by:ArgCalledBy = None):
    type_str = '{}*' if called_by in [ArgCalledBy.Out, ArgCalledBy.Ref] else '{}'
    if type_ == ctypes.c_byte: return type_str.format('uint8_t')
    if type_ == int: return type_str.format('int')
    if type_ == float: return type_str.format('float')
    if type_ == bool: return type_str.format('bool')
    if type_ == ctypes.c_wchar_p: return 'const char16_t*'
    if type_ == ctypes.c_void_p: return 'void*'
    if isinstance(type_, Class): return 'void*'
    if isinstance(type_, Struct): return 'void*' if called_by in [ArgCalledBy.Out, ArgCalledBy.Ref] else '{}_C'.format(self._get_alias_or_name(type_, definition))
    if isinstance(type_, Enum): return 'int'
    if type_ is None: return 'void'
    raise ValueError("{} is not supported in cpp.".format(str(type_)))

BindingGeneratorCPP._get_cppc_type = _get_cppc_type