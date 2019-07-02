from typing import List
import ctypes

from cbg.cpp_binding_generator import BindingGenerator, Define, Class, Struct, Enum, Code, Property, Function, EnumValue, __get_c_func_name__
from cbg.cpp_binding_generator import __get_c_release_func_name__

# A flow of generating code
# generate
# └─__generate_class__
#   └─__generate_unmanaged_property__
#   └─__generate_unmanaged_func__
#   └─__generate_managed_property__
#     └─__write_managed_func_body__
#   └─__generate_managed_func__
#     └─__write_managed_func_body__
#   └─(destructor)

class CodeBlock:
    def __init__(self, coder: Code, title: str, after_space : bool = False):
        '''
        a class for generating code block easily
        '''
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
    def __init__(self, define: Define, lang: str):
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
        self.lang = lang

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

        if(func_.return_value.type_ == bool):
            code('[return: MarshalAs(UnmanagedType.U1)]')
            
        code('private static extern {} {}({});'.format(
            self.__get_csc_type__(func_.return_value.type_, is_return=True), fname, ','.join(args)))

        return code

    def __generate__unmanaged_property_(self, class_: Class, prop_: Property) -> Code:
        code = Code()
        result = ''
        if prop_.has_getter:
            result += str(self.__generate__unmanaged_func__(class_, prop_.getter_as_func()))
        if prop_.has_setter:
            result += str(self.__generate__unmanaged_func__(class_, prop_.setter_as_func()))
        code(result)
        return code

    def __write_caching_function_body__(self, code: Code, class_: Class, func_: Function):
        return_type_name = self.__get_cs_type__(func_.return_value.type_, is_return=True)
        native_func_name = __get_c_func_name__(class_, func_)
        release_name = __get_c_func_name__(class_, Function('Release'))
        body = '''var native = {2}(selfPtr);
if(cache{0}.ContainsKey(native))
{{
    {1} cacheRet;
    cache{0}[native].TryGetTarget(out cacheRet);
    if(cacheRet != null)
    {{
        {3}(native);
        return cacheRet;
    }}
    else
    {{
        cache{0}.Remove(native);
    }}
}}

var ret = new {1}();
ret.selfPtr = native;
cache{0}.Add(native, new WeakReference<{1}>(ret));
return ret;'''
        body = body.format(func_.name, return_type_name, native_func_name, release_name)
        lines = body.split('\n')
        for line in lines:
            code(line)

    def __write_managed_function_body__(self, code: Code, class_: Class, func_: Function):
        fname = __get_c_func_name__(class_, func_)
        # call a function
        args = [self.__convert_csc_to_cs__(
                arg.type_, arg.name) for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = [self.self_ptr_name] + args

        if func_.is_constructor:
            code('{} = {}({});'.format(self.self_ptr_name, fname, ', '.join(args)))
        else:
            if func_.return_value.type_ is None:
                code('{}({});'.format(fname, ','.join(args)))
            elif func_.return_value.do_cache():
                self.__write_caching_function_body__(code, class_, func_)
            else:
                code('var ret = {}({});'.format(fname, ','.join(args)))
                code('return {};'.format(
                    self.__convert_ret__(func_.return_value.type_, 'ret')))

    def __generate__managed_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [self.__get_cs_type__(
            arg.type_) + ' ' + arg.name for arg in func_.args]

        # XML comment
        if func_.brief != None:
            code('/// <summary>')
            code('/// {}'.format(func_.brief.descs[self.lang]))
            code('/// </summary>')
            for arg in func_.args:
                code('/// <param name="{}">{}</param>'.format(arg.name, arg.desc.descs[self.lang]))

        # cache repo
        if func_.return_value.do_cache():
            return_type_name = self.__get_cs_type__(func_.return_value.type_, is_return=True)
            cache_code = 'private Dictionary<IntPtr, WeakReference<{}>> cache{} = new Dictionary<IntPtr, WeakReference<{}>>();'
            code(cache_code.format(return_type_name, func_.name, return_type_name))

        # determine signature
        if func_.is_constructor:
            func_title = 'public {}({})'.format(class_.name, ', '.join(args))
        else:
            func_title = 'public {} {}({})'.format(self.__get_cs_type__(
                func_.return_value.type_, is_return=True), func_.name, ', '.join(args))

        # function body
        with CodeBlock(code, func_title):
            self.__write_managed_function_body__(code, class_, func_)

        return code

    def __generate__managed_property_(self, class_: Class, prop_:Property) -> Code:
        code = Code()

        # cannot generate property with no getter and no setter
        if not prop_.has_getter and not prop_.has_setter:
            return code
        
        # XML comment
        if prop_.brief != None:
            code('/// <summary>')
            code('/// {}'.format(prop_.brief.descs[self.lang]))
            code('/// </summary>')
        
        type_name = self.__get_cs_type__(prop_.type_, is_return=True)
        with CodeBlock(code, 'public {} {}'.format(type_name, prop_.name)):
            if prop_.has_getter:
                with CodeBlock(code, 'get'):
                    self.__write_managed_function_body__(code, class_, prop_.getter_as_func())
            if prop_.has_setter:
                with CodeBlock(code, 'set'):
                    self.__write_managed_function_body__(code, class_, prop_.setter_as_func())
        
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
            for prop_ in class_.properties:
                code(self.__generate__unmanaged_property_(class_, prop_))

            # releasing function
            release_func = Function('Release')
            code(self.__generate__unmanaged_func__(class_, release_func))
            code('')

            # constructor
            with CodeBlock(code, 'internal {}(MemoryHandle handle)'.format(class_.name), True):
                code('this.{} = handle.selfPtr;'.format(self.self_ptr_name))

            for prop_ in class_.properties:
                code(self.__generate__managed_property_(class_, prop_))

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

        # declare using
        code('using System;')
        code('using System.Runtime.InteropServices;')
        code('using System.Collections.Generic;')
        code('')

        # declare namespace
        if self.namespace != '':
            code('namespace {} {{'.format(self.namespace))
            code.inc_indent()

        # a struct for memory management
        with CodeBlock(code, 'struct MemoryHandle', True):
            code('public IntPtr selfPtr;')
            with CodeBlock(code, 'public MemoryHandle(IntPtr p)'):
                code('this.selfPtr = p;')

        # enum group
        for enum_ in self.define.enums:
            code(self.__generate_enum__(enum_))
        
        # class group
        for class_ in self.define.classes:
            code(self.__generate_class__(class_))

        # close namespace
        if self.namespace != '':
            code.dec_indent()
            code('}')

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(self.output_path, mode='w') as f:
                f.write(str(code))
