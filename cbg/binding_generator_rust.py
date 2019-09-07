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

def camelcase_to_underscore(value : str) -> str:
    result = []
    beforeCharacter = ''
    for x in list(value):
        result.append("_" + x.lower()
        if x.isalnum() and x.isupper() and (beforeCharacter != '_')
        else x)
        beforeCharacter = x

    return "".join(result)

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

class BindingGeneratorRust(BindingGenerator):
    def __init__(self, define: Define, lang: str):
        '''
        generator for Rust

        Parameters
        ----------
        self_ptr_name : str
            pointer name in the Class

        '''
        super().__init__(define)
        self.module = ''
        self.output_path = ''
        self.dll_name = ''
        self.self_ptr_name = 'selfPtr'
        self.lang = lang
        self.PtrEnumName = 'PhantomRawPtr'

    def __get_rs_type__(self, type_, is_return = False) -> str:
        if type_ == int:
            return 'i32'

        if type_ == float:
            return 'f32'

        if type_ == bool:
            return 'bool'

        if type_ == ctypes.c_wchar_p:
            if is_return:
                return 'String'
            return '&str'

        if type_ in self.define.classes:
            # return type_.name
            return '*mut {}'.format(self.PtrEnumName)

        if type_ in self.define.structs:
            if is_return:
                return type_.name
            else:
                return '&' + type_.name

        if type_ in self.define.enums:
            return type_.name

        if type_ is None:
            return '()'

        assert(False)

    def __get_rsc_type__(self, type_, is_return = False) -> str:
        if type_ == int:
            return 'c_int'

        if type_ == float:
            return 'c_float'

        if type_ == bool:
            return 'bool'

        if type_ == ctypes.c_wchar_p:
            if is_return:
                return '*const c_char'
            return '*const c_char'

        if type_ in self.define.classes:
            return '*mut {}'.format(self.PtrEnumName)

        if type_ in self.define.structs:
            if is_return:
                return '{}'.format(type_.name)
            else:
                return '&{}'.format(type_.name)

        if type_ in self.define.enums:
            return 'c_int'

        if type_ is None:
            if is_return:
                return '()'
            
            return ''

        print('Type: {}'.format(type_))
        assert(False)

    # def __convert_rsc_to_rs__(self, type_, name: str) -> str:
    #     if type_ == int or type_ == float or type_ == bool:
    #         return name

    #     if type_ == ctypes.c_wchar_p:
    #         return 'CString::new({}).unwrap().as_ptr()'.format(name)

    #     if type_ in self.define.classes:
    #         return '{} != null ? {}.{} : IntPtr.Zero'.format(name, name, self.self_ptr_name)

    #     if type_ in self.define.structs:
    #         return '&{}'.format(name)

    #     if type_ in self.define.enums:
    #         return '{} as int'.format(name)

    #     if type_ is None:
    #         return '()'

    #     assert(False)

    # def __convert_ret__(self, type_, name: str) -> str:
    #     if type_ == int or type_ == float or type_ == bool:
    #         return name

    #     if type_ == ctypes.c_wchar_p:
    #         return 'CString::from_raw({}).into_string.unwrap()'.format(name)

    #     if type_ in self.define.classes:
    #         if type_.do_cache:
    #             # ???????
    #             return '{}.TryGetFromCache({})'.format(type_.name, name)
    #         else:
    #             # ???????
    #             return '{} != null ? new {}(new MemoryHandle({})) : null'.format(name, type_.name, name)

    #     if type_ in self.define.structs:
    #         return '{}'.format(name)

    #     if type_ in self.define.enums:
    #         return '({}){}'.format(type_.name, name)

    #     assert(False)

    def __generate__unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = camelcase_to_underscore(__get_c_func_name__(class_, func_))

        args = [arg.name + ' : ' + self.__get_rsc_type__(arg.type_)
            for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = ['{} : *mut {}'.format(self.self_ptr_name, self.PtrEnumName)] + args

        # if(func_.return_value.type_ == bool):
        #     code('[return: MarshalAs(UnmanagedType.U1)]')
            
        code('fn {}({}) -> {};'.format(
            fname,
            ', '.join(args),
            self.__get_rsc_type__(func_.return_value.type_, is_return=True)
        ))

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

    def __generate_extern__(self, classes : List[str]) -> Code:
        code = Code()
        # extern unmanaged
        code('#[link(name = "{}")]'.format(self.dll_name))
        with CodeBlock(code, 'extern'):
            for class_ in self.define.classes:
                # extern unmanaged functions
                for func_ in class_.funcs:
                    code(self.__generate__unmanaged_func__(class_, func_))
                for prop_ in class_.properties:
                    code(self.__generate__unmanaged_property_(class_, prop_))

                # releasing function
                release_func = Function('Release')
                code(self.__generate__unmanaged_func__(class_, release_func))
                code('')

        return code


    # def __write_managed_function_body__(self, code: Code, class_: Class, func_: Function):
    #     fname = __get_c_func_name__(class_, func_)
    #     # call a function
    #     args = [self.__convert_rsc_to_rs__(
    #             arg.type_, arg.name) for arg in func_.args]

    #     if not func_.is_static and not func_.is_constructor:
    #         args = ["self." + self.self_ptr_name] + args

    #     if func_.is_constructor:
    #         code('{} {{ {} : {}({}) }}'.format(class_.name, self.self_ptr_name, fname, ', '.join(args)))
    #     else:
    #         if func_.return_value.type_ is None:
    #             code('{}({});'.format(fname, ','.join(args)))
    #         else:
    #             code('let ret = {}({});'.format(fname, ','.join(args)))
    #             code('{}'.format(
    #                 self.__convert_ret__(func_.return_value.type_, 'ret')))



    # def __generate__managed_func__(self, class_: Class, func_: Function) -> Code:
    #     code = Code()

    #     args = [arg.name + ' : ' + self.__get_cs_type__(arg.type_) for arg in func_.args]

    #     if not func_.is_static and not func_.is_constructor:
    #         args = [ "&self" ] + args

    #     # Markdown comment
    #     if func_.brief != None:
    #         code('/// {}'.format(func_.brief.descs[self.lang]))

    #         # not empty
    #         if func_.args:
    #             code('///')
    #             code('/// # Arguments')

    #         for arg in func_.args:
    #             code('///')
    #             code('/// * `{}` - {}'.format(arg.name, arg.desc.descs[self.lang]))

    #     # cache repo
    #     # if func_.return_value.do_cache():
    #     #     return_type_name = self.__get_cs_type__(func_.return_value.type_, is_return=True)
    #     #     cache_code = 'private Dictionary<IntPtr, WeakReference<{}>> cache{} = new Dictionary<IntPtr, WeakReference<{}>>();'
    #     #     code(cache_code.format(return_type_name, func_.name, return_type_name))

    #     # determine signature
    #     if func_.is_constructor:
    #         func_title = 'pub fn new({}) -> {}'.format(', '.join(args), class_.name)
    #     else:
    #         func_title = 'pub fn {}({}) -> {}'.format(
    #             camelcase_to_underscore(func_.name),
    #             ', '.join(args),
    #             self.__get_cs_type__(func_.return_value.type_, is_return=True))

    #     # function body
    #     with CodeBlock(code, func_title):
    #         self.__write_managed_function_body__(code, class_, func_)

    #     return code


    # def __generate_class__(self, class_: Class) -> Code:
    #     code = Code()

    #     with CodeBlock(code, 'pub struct {}'.format(class_.name)):
    #         # # cache repo
    #         # if class_.do_cache:
    #         #     # hoge

    #         # unmanaged pointer
    #         code('{} : *mut {},'.format(self.self_ptr_name, self.PtrEnumName))

    #     with CodeBlock(code, 'impl {}'.format(class_.name)):
    #         # unmanaged constructor
    #         # with CodeBlock(code, 'pub(crate) fn create(self.self_ptr_name : *mut {}) -> {}'.format(self.PtrEnumName, class_.name), True):
    #         #     with CodeBlock(code, class_.name):
    #         #         code('{},'.format(self.self_ptr_name))
    #         #         # other fields

    #         for prop_ in class_.properties:
    #             code(self.__generate__managed_property_(class_, prop_))

    #         # managed functions
    #         for func_ in class_.funcs:
    #             code(self.__generate__managed_func__(class_, func_))

    #     # destructor
    #     with CodeBlock(code, 'impl Drop for {}'.format(class_.name)):
    #         with CodeBlock(code, 'fn drop(&mut self)'):
    #             # with CodeBlock(code, 'if !self.{}.is_null()'.format(self.self_ptr_name)):
    #             code('unsafe {{ {}({}) }};'.format(__get_c_release_func_name__(class_), self.self_ptr_name))
    #                 # code('self.{} = std::ptr::null_mut();'.format(self.self_ptr_name))
            
    #     return code


    def generate(self):
        code = Code()

        # declare use
        code('use std::os::raw::*;')
        code('use std::ffi::CString;')
        code('')

        # declare module
        if self.module != '':
            code('mod {} {{'.format(self.module))
            code.inc_indent()

        code('enum {} {{ }}'.format(self.PtrEnumName))
        code('')

        # a struct for memory management
        # with CodeBlock(code, 'struct MemoryHandle', True):
        #     code('public IntPtr selfPtr;')
        #     with CodeBlock(code, 'public MemoryHandle(IntPtr p)'):
        #         code('this.selfPtr = p;')

        # # enum group
        # for enum_ in self.define.enums:
        #     code(self.__generate_enum__(enum_))

        code(self.__generate_extern__(self.define.classes))
        
        # # class group
        # for class_ in self.define.classes:
        #     code(self.__generate_class__(class_))

        # close module
        if self.module != '':
            code.dec_indent()
            code('}')

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(self.output_path, mode='w') as f:
                f.write(str(code))