import ctypes
from typing import TypeVar
from cbg.common import *
from cbg.binding_cs.binding_generator import BindingGeneratorCS

# エイリアスを取得
T = TypeVar('T')
def _get_alias_or_name(self:BindingGeneratorCS, type_:T, definition:Definition):
    namespace = ''
    for dependency in definition.dependencies:
        if type_ in dependency.classes + dependency.structs + dependency.enums:
            namespace = dependency.namespace + '.'
            break
    return namespace + (type_.name if type_.alias == None else type_.alias)

BindingGeneratorCS._get_alias_or_name = _get_alias_or_name

# 入力された型をC#形式で文字列で取得
U = TypeVar('U')
def _get_cs_type(self:BindingGeneratorCS, type_:U, definition:Definition, called_by:ArgCalledBy = None):
    ptr = ''
    if called_by == ArgCalledBy.Out: ptr = 'out'
    if called_by == ArgCalledBy.Ref: ptr = 'ref'
    if type_ == ctypes.c_byte: return ptr + 'byte'
    if type_ == int: return ptr + 'int'
    if type_ == float: return ptr + 'float'
    if type_ == bool: return ptr + 'bool'
    if type_ == ctypes.c_wchar_p: return 'string'
    if type_ == ctypes.c_void_p: return 'IntPtr'
    if isinstance(type_, Class): return self._get_alias_or_name(type_, definition)
    if isinstance(type_, Struct): return ('' if called_by == None else ptr) + type_.alias
    if isinstance(type_, Enum): return self._get_alias_or_name(type_, definition)
    if type_ is None: return 'void'
    raise ValueError("{} is not supported in cs.".format(str(type_)))

BindingGeneratorCS._get_cs_type = _get_cs_type

# 入力された型をC言語形式で文字列で取得
V = TypeVar('V')
def _get_csc_type(self:BindingGeneratorCS, type_:V, definition:Definition, called_by:ArgCalledBy = None):
    ptr = ''
    if called_by == ArgCalledBy.Out: ptr = '[Out] out'
    if called_by == ArgCalledBy.Ref: ptr = '[In,Out] ref'
    if type_ == ctypes.c_byte: return ptr + 'byte'
    if type_ == int: return ptr + 'int'
    if type_ == float: return ptr + 'float'
    if type_ == bool: return ('' if called_by == None else '[MarshalAs(UnmanagedType.Bool)] ' + ptr) + 'bool'
    if type_ == ctypes.c_wchar_p: return 'IntPtr' if called_by == None else '[MarshalAs(UnmanagedType.LPWStr)] string'
    if type_ == ctypes.c_void_p: return 'IntPtr'
    if isinstance(type_, Class): return 'IntPtr'
    if isinstance(type_, Struct): return ('' if called_by == None else ptr) + type_.alias
    if isinstance(type_, Enum): return 'int'
    if type_ is None: return 'void'
    raise ValueError("{} is not supported in cs.".format(str(type_)))

BindingGeneratorCS._get_csc_type = _get_csc_type