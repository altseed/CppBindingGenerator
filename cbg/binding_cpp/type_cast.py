import ctypes
from typing import TypeVar
from cbg.common import *
from cbg.binding_cpp.binding_generator import BindingGeneratorCPP

# 入力された型をC++形式にキャストする処理を文字列で取得
T = TypeVar('T')
def _type_cast(self:BindingGeneratorCPP, type_:T, name:str, definition:Definition, called_by:ArgCalledBy):
    ptr = ''
    is_ref = called_by in [ArgCalledBy.Out, ArgCalledBy.Ref]
    if type_ in [ctypes.c_byte, int, float, bool, ctypes.c_void_p]: return '{}.get()'.format(name) if is_ref else name
    if type_ in [ctypes.c_wchar_p]: return name + '.c_str()'
    if isinstance(type_, Class): return '{} != nullptr ? ({}->{}) : nullptr'.format(name, name, self.self_ptr_name)
    if isinstance(type_, Struct): return '{}.get()'.format(name) if is_ref else name
    if isinstance(type_, Enum): return '(int){}'.format(name)
    if type_ is None: return 'void'
    assert(False)

BindingGeneratorCPP._type_cast = _type_cast

# 戻り値をC++形式にキャストする処理を文字列で取得
U = TypeVar('U')
def _return_cast(self:BindingGeneratorCPP, type_:T, name:str, definition:Definition):
    if type_ in [ctypes.c_byte, int, float, bool, ctypes.c_void_p, ctypes.c_wchar_p]: return name
    if isinstance(type_, Class):
        class_name = self._get_alias_or_name(type_, definition)
        if type_.cache_mode != CacheMode.NoCache: return '{}::TryGetFromCache({})'.format(class_name, name)
        else: return '{1} != nullptr ? new {0}({1}) : nullptr'.format(class_name, name)
    if isinstance(type_, Struct): return name
    if isinstance(type_, Enum): return '({}){}'.format(self._get_alias_or_name(type_, definition), name)
    if type_ is None: return 'void'
    assert(False)

BindingGeneratorCPP._return_cast = _return_cast
