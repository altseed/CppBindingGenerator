from typing import List
import ctypes

from .cpp_binding_generator import BindingGenerator, Define, CacheMode, Class, Struct, Enum, Code, Property, Function, EnumValue, __get_c_func_name__
from .cpp_binding_generator import __get_c_release_func_name__

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
    def __init__(self, coder: Code, title: str, after_space: bool = False):
        '''
        a class for generating code block easily
        '''
        self.title = title
        self.coder = coder
        self.after_space = after_space

    def __enter__(self):
        self.coder(self.title)
        self.coder('{')
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

        # XML Comment
        if enum_.brief != None:
            code('/// <summary>')
            code('/// {}'.format(enum_.brief.descs[self.lang]))
            code('/// </summary>')
        with CodeBlock(code, 'public enum {} : int'.format(enum_.name)):
            for val in enum_.values:
                # XML Comment
                if val.brief != None:
                    code('/// <summary>')
                    code('/// {}'.format(val.brief.descs[self.lang]))
                    code('/// </summary>')

                # Enum Value Body
                line = val.name
                if val.value != None:
                    line = '{} = {}'.format(line, val.value)
                code(line + ',')
        return code

    def __get_cs_type__(self, type_, is_return=False) -> str:
        if type_ == int:
            return 'int'

        if type_ == float:
            return 'float'

        if type_ == bool:
            return 'bool'

        if type_ == ctypes.c_wchar_p:
            return 'string'

        if type_ == ctypes.c_void_p:
            return 'IntPtr'

        if type_ in self.define.classes:
            return type_.name

        if type_ in self.define.structs:
            if is_return:
                return '{}'.format(type_.alias)
            else:
                return 'ref {}'.format(type_.alias)

        if type_ in self.define.enums:
            return type_.name

        if type_ is None:
            return 'void'

        assert(False)

    def __get_csc_type__(self, type_, is_return=False) -> str:
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

        if type_ == ctypes.c_void_p:
            return 'IntPtr'

        if type_ in self.define.classes:
            return 'IntPtr'

        if type_ in self.define.structs:
            if is_return:
                return '{}'.format(type_.alias)
            else:
                return 'ref {}'.format(type_.alias)

        if type_ in self.define.enums:
            return 'int'

        if type_ is None:
            return 'void'

        assert(False)

    def __convert_csc_to_cs__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_wchar_p or type_ == ctypes.c_void_p:
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
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_void_p:
            return name

        if type_ == ctypes.c_wchar_p:
            return 'System.Runtime.InteropServices.Marshal.PtrToStringUni({})'.format(name)

        if type_ in self.define.classes:
            if type_.cache_mode != CacheMode.NoCache:
                return '{}.TryGetFromCache({})'.format(type_.name, name)
            else:
                return '{} != null ? new {}(new MemoryHandle({})) : null'.format(name, type_.name, name)

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
            self.__get_csc_type__(func_.return_value.type_, is_return=True), fname, ', '.join(args)))

        return code

    def __generate__unmanaged_property_(self, class_: Class, prop_: Property) -> Code:
        code = Code()
        result = ''
        if prop_.has_getter:
            result += str(self.__generate__unmanaged_func__(class_,
                                                            prop_.getter_as_func()))
        if prop_.has_setter:
            result += str(self.__generate__unmanaged_func__(class_,
                                                            prop_.setter_as_func()))
        code(result)
        return code

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
                code('{}({});'.format(fname, ', '.join(args)))
            else:
                code('var ret = {}({});'.format(fname, ', '.join(args)))
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
                if arg.brief != None:
                    code('/// <param name="{}">{}</param>'.format(arg.name,
                                                                  arg.brief.descs[self.lang]))

            if func_.return_value.brief != None:
                code(
                    '/// <returns>{}</returns>'.format(func_.return_value.brief.descs[self.lang]))

        # cache repo
        if func_.return_value.cache_mode() == CacheMode.Cache:
            return_type_name = self.__get_cs_type__(
                func_.return_value.type_, is_return=True)
            cache_code = 'private Dictionary<IntPtr, WeakReference<{}>> cache{} = new Dictionary<IntPtr, WeakReference<{}>>();'
            code(cache_code.format(return_type_name, func_.name, return_type_name))
        elif func_.return_value.cache_mode() == CacheMode.ThreadSafeCache:
            return_type_name = self.__get_cs_type__(
                func_.return_value.type_, is_return=True)
            cache_code = 'private ConcurrentDictionary<IntPtr, WeakReference<{}>> cache{} = new ConcurrentDictionary<IntPtr, WeakReference<{}>>();'
            code(cache_code.format(return_type_name, func_.name, return_type_name))

        # determine signature
        determines = []

        if func_.is_public:
            determines += ['public']
        else:
            determines += ['internal']

        if func_.is_static:
            determines += ['static']

        if func_.is_constructor:
            func_title = '{} {}({})'.format(
                ' '.join(determines), class_.name, ', '.join(args))
        else:
            func_title = '{} {} {}({})'.format(' '.join(determines), self.__get_cs_type__(
                func_.return_value.type_, is_return=True), func_.name, ', '.join(args))

        # function body
        with CodeBlock(code, func_title):
            self.__write_managed_function_body__(code, class_, func_)

        return code

    def __write_getter_(self, code: Code, class_: Class, prop_: Property):
        with CodeBlock(code, 'get'):
            if prop_.has_setter:
                with CodeBlock(code, 'if (_{} != null)'.format(prop_.name)):
                    if isinstance(prop_.type_, Class) or (prop_.type_ == ctypes.c_wchar_p):
                        code('return _{};'.format(prop_.name))
                    else:
                        code('return _{}.Value;'.format(prop_.name))
            self.__write_managed_function_body__(
                code, class_, prop_.getter_as_func())

    def __write_setter_(self, code: Code, class_: Class, prop_: Property):
        with CodeBlock(code, 'set'):
            if prop_.has_getter:
                code('_{} = value;'.format(prop_.name))
            self.__write_managed_function_body__(
                code, class_, prop_.setter_as_func())

    def __generate__managed_property_(self, class_: Class, prop_: Property) -> Code:
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
                self.__write_getter_(code, class_, prop_)
            if prop_.has_setter:
                self.__write_setter_(code, class_, prop_)

        if prop_.has_setter and prop_.has_getter:
            back_type = type_name
            if not (isinstance(prop_.type_, Class) or (prop_.type_ == ctypes.c_wchar_p)):
                back_type += '?'
            code('private {} _{};'.format(back_type, prop_.name))

        return code

    def __write_cache_getter__(self, code: Code, class_: Class):
        release_func_name = __get_c_func_name__(class_, Function('Release'))

        new_ = ''
        if class_.base_class != None:
            new_ = 'new'

        body = '''internal static {2} {0} TryGetFromCache(IntPtr native)
{{
    if(native == IntPtr.Zero) return null;

    if(cacheRepo.ContainsKey(native))
    {{
        {0} cacheRet;
        cacheRepo[native].TryGetTarget(out cacheRet);
        if(cacheRet != null)
        {{
            {1}(native);
            return cacheRet;
        }}
        else
        {{
            cacheRepo.Remove(native);
        }}
    }}

    var newObject = new {0}(new MemoryHandle(native));
    cacheRepo[native] = new WeakReference<{0}>(newObject);
    return newObject;
}}
'''.format(class_.name, release_func_name, new_)
        lines = body.split('\n')
        for line in lines:
            code(line)

    def __write_threadsafe_cache_getter__(self, code: Code, class_: Class):
        release_func_name = __get_c_func_name__(class_, Function('Release'))

        new_ = ''
        if class_.base_class != None:
            new_ = 'new'

        body = '''internal static {2} {0} TryGetFromCache(IntPtr native)
{{
    if(native == IntPtr.Zero) return null;

    if(cacheRepo.ContainsKey(native))
    {{
        {0} cacheRet;
        cacheRepo[native].TryGetTarget(out cacheRet);
        if(cacheRet != null)
        {{
            {1}(native);
            return cacheRet;
        }}
        else
        {{
            cacheRepo.TryRemove(native, out _);
        }}
    }}

    var newObject = new {0}(new MemoryHandle(native));
    cacheRepo.TryAdd(native, new WeakReference<{0}>(newObject));
    return newObject;
}}
'''.format(class_.name, release_func_name, new_)
        lines = body.split('\n')
        for line in lines:
            code(line)

    def __generate_class__(self, class_: Class) -> Code:
        code = Code()

        # XML comment
        if class_.brief != None:
            code('/// <summary>')
            code('/// {}'.format(class_.brief.descs[self.lang]))
            code('/// </summary>')

        # inheritance
        inheritance = ""
        if class_.base_class != None:
            inheritance = ' : {}'.format(class_.base_class.name)

        # class body

        access = 'internal'
        if class_.is_public:
            access = 'public'

        with CodeBlock(code, '{} partial class {}{}'.format(access, class_.name, inheritance)):
            code('#region unmanaged')
            code('')

            # cache repo
            if class_.cache_mode == CacheMode.Cache:
                cache_code = 'private static Dictionary<IntPtr, WeakReference<{}>> cacheRepo = new Dictionary<IntPtr, WeakReference<{}>>();'
                code(cache_code.format(class_.name, class_.name))
                code('')
                self.__write_cache_getter__(code, class_)
            elif class_.cache_mode == CacheMode.ThreadSafeCache:
                cache_code = 'private static ConcurrentDictionary<IntPtr, WeakReference<{}>> cacheRepo = new ConcurrentDictionary<IntPtr, WeakReference<{}>>();'
                code(cache_code.format(class_.name, class_.name))
                code('')
                self.__write_threadsafe_cache_getter__(code, class_)

            # unmanaged pointer
            if class_.base_class == None:
                code('internal IntPtr {} = IntPtr.Zero;'.format(self.self_ptr_name))

            # extern unmanaged functions
            for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'csharp' in f.targets]:
                code(self.__generate__unmanaged_func__(class_, func_))
            for prop_ in class_.properties:
                code(self.__generate__unmanaged_property_(class_, prop_))

            # releasing function
            release_func = Function('Release')
            code(self.__generate__unmanaged_func__(class_, release_func))
            code('#endregion')
            code('')

            # constructor
            if class_.base_class == None:
                with CodeBlock(code, 'internal {}(MemoryHandle handle)'.format(class_.name), True):
                    code('{} = handle.selfPtr;'.format(self.self_ptr_name))
            else:
                with CodeBlock(code, 'internal {}(MemoryHandle handle) : base(handle)'.format(class_.name), True):
                    code('{} = handle.selfPtr;'.format(self.self_ptr_name))

            # properties
            for prop_ in class_.properties:
                code(self.__generate__managed_property_(class_, prop_))

            # managed functions
            for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'csharp' in f.targets]:
                code(self.__generate__managed_func__(class_, func_))

            # destructor
            with CodeBlock(code, '~{}()'.format(class_.name)):
                with CodeBlock(code, 'lock (this) '):
                    with CodeBlock(code, 'if ({} != IntPtr.Zero)'.format(self.self_ptr_name)):
                        code('{}({});'.format(__get_c_release_func_name__(
                            class_), self.self_ptr_name))
                        code('{} = IntPtr.Zero;'.format(self.self_ptr_name))

        return code

    def generate(self):
        code = Code()

        # add Waring
        code('// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        code('// !!                                          !!')
        code('// !!  THIS FILE IS AUTO GENERATED.            !!')
        code('// !!  YOUR COMMIT ON THI FILE WILL BE WIPED.  !!')
        code('// !!                                          !!')
        code('// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        # declare using
        code('using System;')
        code('using System.Runtime.InteropServices;')
        code('using System.Collections.Generic;')
        code('using System.Collections.Concurrent;')
        code('')

        # declare namespace
        if self.namespace != '':
            code('namespace {}'.format(self.namespace))
            code('{')
            code.inc_indent()

        # a struct for memory management
        with CodeBlock(code, 'struct MemoryHandle', True):
            code('public IntPtr selfPtr;')  # internal?
            with CodeBlock(code, 'public MemoryHandle(IntPtr p)'):  # internal?
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
            with open(self.output_path, mode='w', encoding='utf-8') as f:
                f.write(str(code))
