from typing import List
import ctypes

from cbg.cpp_binding_generator import BindingGenerator, Define, Class, Struct, Enum, Code, Function, EnumValue, __get_c_func_name__
from cbg.cpp_binding_generator import __get_c_release_func_name__

# 生成処理の流れ
# generate
# └─__generate_class__
#   └─__generate_managed_func__
#     └─__get_cs_type__
#     └─__convert_csc_to_cs__
#     └─__convert_ret__
#   └─__generate_unmanaged_func__
#     └─__get_csc_type__
#     └─__convert_csc_to_cs__
#     └─__convert_ret__
#   └─(destructor)

# with式を使ってコードブロックの書き出しを視覚的にするためのクラス
class CodeBlock:
    def __init__(self, coder: Code, title: str, after_space : bool = False):
        self.title = title
        self.coder = coder
        self.after_space = after_space
    def __enter__(self):
        self.coder(self.title + ' {')
        self.coder.inc_indent()
        return self
    def __exit__(self, exit_type, exit_value, traceback):
        self.coder.dec_indent()
        self.coder('}')
        if self.after_space:
            self.coder('')

class BindingGeneratorCSharp(BindingGenerator):
    def __init__(self, define: Define):
        '''
        generator for C#

        Parameters
        ----------
        self_ptr_name : str
            pointer name in the Class

        '''
        super().__init__(define)
        self.namespace = ''
        self.output_path = ''
        self.dll_name = ''
        self.self_ptr_name = 'selfPtr'

    def __generate_enum__(self, enum_: Enum) -> Code:
        code = Code()
        with CodeBlock(code, 'public enum {} : int'.format(enum_.name)):
            for val in enum_.values:
                line = val.name
                if val.value != None:
                    line = '{} = {}'.format(line, val.value)
                code(line + ',')
        return code

    def __get_cs_type__(self, type_, is_return = False) -> str:
        if type_ == int:
            return 'int'

        if type_ == float:
            return 'float'

        if type_ == bool:
            return 'bool'

        if type_ == ctypes.c_wchar_p:
            return 'string'

        if type_ in self.define.classes:
            return type_.name

        if type_ in self.define.structs:
            if is_return:
                return '{}'.format(type_.name)
            else:
                return 'ref {}'.format(type_.name)

        if type_ in self.define.enums:
            return type_.name

        if type_ is None:
            return 'void'

        assert(False)

    def __get_csc_type__(self, type_, is_return = False) -> str:
        if type_ == int:
            return 'int'

        if type_ == float:
            return 'float'

        if type_ == bool:
            if is_return:
                return 'bool'
            else:
                return '[MarshalAs(UnmanagedType.Bool)] bool'

        if type_ == ctypes.c_wchar_p:
            if is_return:
                return 'IntPtr'
            return '[MarshalAs(UnmanagedType.LPWStr)] string'

        if type_ in self.define.classes:
            return 'IntPtr'

        if type_ in self.define.structs:
            if is_return:
                return '{}'.format(type_.name)
            else:
                return 'ref {}'.format(type_.name)

        if type_ in self.define.enums:
            return 'int'

        if type_ is None:
            return 'void'

        assert(False)

    def __convert_csc_to_cs__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_wchar_p:
            return name

        if type_ in self.define.classes:
            return '{} != null ? {}.{} : IntPtr.Zero'.format(name, name, self.self_ptr_name)

        if type_ in self.define.structs:
            return 'ref {}'.format(name)

        if type_ in self.define.enums:
            return '(int){}'.format(name)

        if type_ is None:
            return 'void'

        assert(False)

    def __convert_ret__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool:
            return name

        if type_ == ctypes.c_wchar_p:
            return 'System.Runtime.InteropServices.Marshal.PtrToStringUni({})'.format(name)

        if type_ in self.define.classes:
            return 'ret != null ? new {}(new MemoryHandle({})) : null'.format(type_.name, name)

        if type_ in self.define.structs:
            return '{}'.format(name)

        if type_ in self.define.enums:
            return '({}){}'.format(type_.name, name)

        assert(False)

    def __generate__unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [self.__get_csc_type__(arg.type_) +
                ' ' + arg.name for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = ['IntPtr {}'.format(self.self_ptr_name)] + args

        code('[DllImport("{}")]'.format(self.dll_name))

        if(func_.return_type == bool):
            code('[return: MarshalAs(UnmanagedType.U1)]')
            
        code('private static extern {} {}({});'.format(
            self.__get_csc_type__(func_.return_type, is_return=True), fname, ','.join(args)))

        return code

    def __generate__managed_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [self.__get_cs_type__(
            arg.type_) + ' ' + arg.name for arg in func_.args]

        # determine signature
        if func_.is_constructor:
            func_title = 'public {}({})'.format(class_.name, ','.join(args))
        else:
            func_title = 'public {} {}({})'.format(self.__get_cs_type__(
                func_.return_type, is_return=True), func_.name, ','.join(args))

        # function body
        with CodeBlock(code, func_title):
            # call a function
            args = [self.__convert_csc_to_cs__(
                    arg.type_, arg.name) for arg in func_.args]

            if not func_.is_static and not func_.is_constructor:
                args = [self.self_ptr_name] + args

            if func_.is_constructor:
                code('{} = {}({});'.format(self.self_ptr_name, fname, ','.join(args)))
            else:
                if func_.return_type is None:
                    code('{}({});'.format(fname, ','.join(args)))
                else:
                    code('var ret = {}({});'.format(fname, ','.join(args)))
                    code('return {};'.format(
                        self.__convert_ret__(func_.return_type, 'ret')))

        return code

    def __generate_class__(self, class_: Class) -> Code:
        code = Code()

        # class body
        with CodeBlock(code, 'public class {}'.format(class_.name)):
            # unmanaged pointer
            code('internal IntPtr {} = IntPtr.Zero;'.format(self.self_ptr_name))
            code('')

            # extern unmanaged functions
            for func_ in class_.funcs:
                code(self.__generate__unmanaged_func__(class_, func_))

            # releasing function
            release_func = Function('Release')
            code(self.__generate__unmanaged_func__(class_, release_func))
            code('')

            # constructor
            with CodeBlock(code, 'internal {}(MemoryHandle handle)'.format(class_.name), True):
                code('this.{} = handle.selfPtr;'.format(self.self_ptr_name))

            # managed functions
            for func_ in class_.funcs:
                code(self.__generate__managed_func__(class_, func_))

            # destructor
            with CodeBlock(code, '~{}()'.format(class_.name)):
                with CodeBlock(code, 'lock (this) '):
                    with CodeBlock(code, 'if ({} != IntPtr.Zero)'.format(self.self_ptr_name)):
                        code('{}({});'.format(__get_c_release_func_name__(class_), self.self_ptr_name))
                        code('{} = IntPtr.Zero;'.format(self.self_ptr_name))

        return code

    def generate(self):
        code = Code()

        # using宣言
        code('using System;')
        code('using System.Runtime.InteropServices;')
        code('')

        # namespace宣言
        if self.namespace != '':
            code('namespace {} {{'.format(self.namespace))
            code.inc_indent()

        # メモリ管理用に固定で生成する構造体
        with CodeBlock(code, 'struct MemoryHandle', True):
            code('public IntPtr selfPtr;')
            with CodeBlock(code, 'public MemoryHandle(IntPtr p)'):
                code('this.selfPtr = p;')

        # enum群
        for enum_ in self.define.enums:
            code(self.__generate_enum__(enum_))
        
        # class群
        for class_ in self.define.classes:
            code(self.__generate_class__(class_))

        # namespace閉じる
        if self.namespace != '':
            code.dec_indent()
            code('}')

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(self.output_path, mode='w') as f:
                f.write(str(code))
