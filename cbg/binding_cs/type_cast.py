import ctypes
from typing import TypeVar
from cbg.common import *
import cbg.wrapper.type_name as type_name
import cbg.binding_cs.generate_binding as gen_binding

# 入力された型をC#形式にキャストする処理を文字列で取得
T = TypeVar('T')
def _type_cast(type_:T, name:str, definition:Definition, called_by:ArgCalledBy):
    generator = gen_binding.BindingGeneratorCS()
    ptr = ''
    if called_by == ArgCalledBy.Out: ptr = 'out '
    if called_by == ArgCalledBy.Ref: ptr = 'ref '
    if type_ in [ctypes.c_byte, int, float, bool, ctypes.c_wchar_p, ctypes.c_void_p]: return ptr + name
    if isinstance(type_, Class): return '{0} != null ? {0}.{1} : IntPtr.Zero'.format(name, generator.self_ptr_name)
    if isinstance(type_, Struct): return ptr + name
    if isinstance(type_, Enum): return '(int)' + name
    if type_ is None: return 'void'
    assert(False)

# 戻り値をC#形式にキャストする処理を文字列で取得
U = TypeVar('U')
def _return_cast(type_:T, name:str, definition:Definition):
    generator = gen_binding.BindingGeneratorCS()
    if type_ in [ctypes.c_byte, int, float, bool, ctypes.c_void_p]: return name
    if type_ in [ctypes.c_wchar_p]: return 'System.Runtime.InteropServices.Marshal.PtrToStringUni(' + name + ')'
    if isinstance(type_, Class):
        class_name = type_name._get_alias_or_name(type_, definition)
        if type_.cache_mode != CacheMode.NoCache: return '{}.TryGetFromCache({})'.format(class_name, name)
        else: return '{1} != null ? new {0}(new MemoryHandle({1})) : null'.format(class_name, name)
    if isinstance(type_, Struct): return name
    if isinstance(type_, Enum): return '({}){}'.format(type_name._get_alias_or_name(type_, definition), name)
    if type_ is None: return 'void'
    assert(False)