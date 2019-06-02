from typing import List
import ctypes

from cbg.cpp_binding_generator import BindingGenerator, Define, Class, Struct, Enum, Code, Function, __get_c_func_name__
from cbg.cpp_binding_generator import __get_c_release_func_name__


class BindingGeneratorCSharp(BindingGenerator):
    def __init__(self, define: Define):
        super().__init__(define)
        self.namespace = ''
        self.output_path = ''
        self.dll_name = ''

    def __get_cs_type__(self, type_) -> str:
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
            return '[MarshalAs(UnmanagedType.LPWStr)] string'

        if type_ in self.define.classes:
            return 'IntPtr'

        if type_ in self.define.structs:
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
            return '{}.selfPtr'.format(name)

        if type_ in self.define.structs:
            return 'ref {}'.format(name)

        if type_ in self.define.enums:
            return '({}){}'.format(type_.name, name)

        if type_ is None:
            return 'void'

        assert(False)

    def __convert_ret__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_wchar_p:
            return name

        if type_ in self.define.classes:
            return 'new {}({})'.format(type_.name, name)

        if type_ in self.define.structs:
            return 'ref {}'.format(type_.name)

        if type_ in self.define.enums:
            return '({}){}'.format(type_.name, name)

        assert(False)

    def __generate__unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [self.__get_csc_type__(arg.type_) +
                ' ' + arg.name for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = ['IntPtr selfPtr'] + args

        code('[DllImport("{}")]'.format(self.dll_name))

        if(func_.return_type == bool):
            code('[return: MarshalAs(UnmanagedType.U1)]')
            
        code('internal static extern {} {}({});'.format(
            self.__get_csc_type__(func_.return_type, is_return=True), fname, ','.join(args)))

        return code

    def __generate__managed_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [self.__get_cs_type__(
            arg.type_) + ' ' + arg.name for arg in func_.args]

        if func_.is_constructor:
            code('public {}({}) {{'.format(class_.name, ','.join(args)))
        else:
            code('public {} {}({}) {{'.format(self.__get_cs_type__(
                func_.return_type), func_.name, ','.join(args)))

        code.inc_indent()

        # call a function
        args = [self.__convert_csc_to_cs__(
                arg.type_, arg.name) for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = ['selfPtr'] + args

        if func_.is_constructor:
            code('selfPtr = {}({});'.format(fname, ','.join(args)))
        else:
            if func_.return_type is None:
                code('{}({});'.format(fname, ','.join(args)))
            else:
                code('var ret = {}({});'.format(fname, ','.join(args)))
                code('return {};'.format(
                    self.__convert_ret__(func_.return_type, 'ret')))
        code.dec_indent()

        code('}')

        return code

    def __generate_class__(self, class_: Class) -> Code:
        code = Code()

        code('public class {} {{'.format(class_.name))

        code.inc_indent()

        code('IntPtr selfPtr = IntPtr.Zero;')
        code('')

        # unmanaged
        for func_ in class_.funcs:
            code(self.__generate__unmanaged_func__(class_, func_))

        # generate release
        release_func = Function('Release')
        code(self.__generate__unmanaged_func__(class_, release_func))

        code('')

        # managed
        for func_ in class_.funcs:
            code(self.__generate__managed_func__(class_, func_))

        # destructor
        code('~{}() {{'.format(class_.name))
        code.inc_indent()

        code('lock (this) {')
        code('if (selfPtr != IntPtr.Zero) {')
        code.inc_indent()

        code('{}(selfPtr);'.format(__get_c_release_func_name__(class_)))
        code('selfPtr = IntPtr.Zero;')

        code.dec_indent()

        code('}')

        code.dec_indent()
        code('}')
        code('')

        code.dec_indent()
        code('}')
        code('}')
        code('')

        return str(code)

    def generate(self):
        code = Code()

        code('using System;')
        code('using System.Runtime.InteropServices;')
        code('')

        if self.namespace != '':
            code('namespace {} {{'.format(self.namespace))
            code.inc_indent()

        for class_ in self.define.classes:
            code(self.__generate_class__(class_))

        if self.namespace != '':
            code.dec_indent()
            code('}')

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(self.output_path, mode='w') as f:
                f.write(str(code))
