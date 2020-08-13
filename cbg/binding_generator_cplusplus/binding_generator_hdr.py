from typing import List
import ctypes
import os, textwrap

from ..cpp_binding_generator import *
from ..cpp_binding_generator import __get_c_func_name__
from ..cpp_binding_generator import __get_c_release_func_name__

from .code_block import CodeBlock

class BindingGeneratorCPlusPlusHdr(BindingGenerator):
    def __init__(self, define: Define, lang: str):
        '''
        generator for C++

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
        self.includes = []

    def __generate_enum__(self, enum_: Enum) -> Code:
        code = Code()

        if enum_.brief != None:
            code('/**')
            code(' @brief {}'.format(enum_.brief.descs[self.lang]))
            code(' */')

        enum_name = enum_.alias if enum_.alias != None else enum_.name
        
        with CodeBlock(code, 'enum class {} : int'.format(enum_name), False, True):
            for val in enum_.values:

                # Doxygen Comment
                if val.brief != None:
                    code('/**')
                    code(' @brief {}'.format(val.brief.descs[self.lang]))
                    code(' */')

                # Enum Value Body
                if val.value != None:
                    code('{} = {},'.format(val.name, val.value))
                else:
                    code('{},'.format(val.name))
                
                
        return code

    def __get_cpp_type__(self, type_, is_return=False, called_by: ArgCalledBy = None) -> str:

        is_ref = called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref

        if type_ == ctypes.c_byte:
            return 'std::shared_ptr<uint8_t>' if is_ref else 'uint8_t'

        if type_ == int:
            return 'std::shared_ptr<int>' if is_ref else 'int'

        if type_ == float:
            return 'std::shared_ptr<float>' if is_ref else 'float'

        if type_ == bool:
            return 'std::shared_ptr<bool>' if is_ref else 'bool'

        if type_ == ctypes.c_wchar_p:
            return 'std::basic_string<char16_t>'

        if type_ == ctypes.c_void_p:
            return 'void*'

        if type_ in self.define.classes:
            return 'std::shared_ptr<{}>'.format(type_.name)

        if type_ in self.define.structs:
            c_struct = '{}_C'.format(type_.alias)
            return 'std::shared_ptr<{}>'.format(c_struct) if is_ref else c_struct

        if type_ in self.define.enums:
            return type_.name if type_.alias == None else type_.alias

        if type_ is None:
            return 'void'

        assert(False)

    def __get_cppc_type__(self, type_, is_return=False, called_by: ArgCalledBy = None) -> str:

        is_ref = called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref

        if type_ == ctypes.c_byte:
            return 'uint8_t*' if is_ref else 'uint8_t'

        if type_ == int:
            return 'int*' if is_ref else 'int'

        if type_ == float:
            return 'float*' if is_ref else 'float'

        if type_ == bool:
            return 'int*' if is_ref else 'int'

        if type_ == ctypes.c_wchar_p:
            return 'const char16_t*'

        if type_ == ctypes.c_void_p:
            return 'void*'

        if type_ in self.define.classes:
            return 'void*'

        if type_ in self.define.structs:
            return 'void*' if is_ref else '{}_C'.format(type_.alias)

        if type_ in self.define.enums:
            return 'int'

        if type_ is None:
            return 'void'

        print('Unsupported Type:{}'.format(type_))

        assert(False)

    def __convert_cppc_to_cpp__(self, type_, name: str, called_by: ArgCalledBy = None) -> str:

        is_ref = called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref

        if type_ == ctypes.c_byte or type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_void_p:
            return '{}.get()'.format(name) if is_ref else name

        if type_ == ctypes.c_wchar_p:
            return name + '.c_str()'

        if type_ in self.define.classes:
            return '{} != nullptr ? ({}->{}) : nullptr'.format(name, name, self.self_ptr_name)

        if type_ in self.define.structs:
            return '{}.get()'.format(name) if is_ref else name

        if type_ in self.define.enums:
            return '(int){}'.format(name)

        if type_ is None:
            return 'void'

        assert(False)

    def __convert_ret__(self, type_, name: str) -> str:

        if type_ == ctypes.c_byte or type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_void_p or type_ == ctypes.c_wchar_p:
            return name

        if type_ in self.define.classes:
            if type_.cache_mode != CacheMode.NoCache:
                return '{}::TryGetFromCache({})'.format(type_.name, name)
            else:
                return '{} != nullptr ? new {}({}) : nullptr'.format(name, type_.name, name)

        if type_ in self.define.structs:
            return '{}'.format(name)

        if type_ in self.define.enums:
            enum_name = type_.name if type_.alias == None else type_.alias
            return '({}){}'.format(enum_name, name)

        assert(False)

    def __generate_unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()

        return_type = self.__get_cppc_type__(func_.return_value.type_, is_return=True)
        func_name = __get_c_func_name__(class_, func_)
        args = [self.__get_cppc_type__(arg.type_, False, arg.called_by) + ' ' + arg.name for arg in func_.args]
        if not func_.is_static and not func_.is_constructor:
            args = ['void* {}'.format(self.self_ptr_name)] + args

        code('static {} {}({});'.format(return_type, func_name, ', '.join(args)))
        
        return code

    def __generate_unmanaged_prop__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        result = ''
        if prop_.has_getter:
            result += str(self.__generate__unmanaged_func__(class_,prop_.getter_as_func()))
        if prop_.has_setter:
            result += str(self.__generate__unmanaged_func__(class_,prop_.setter_as_func()))
        code(result)
        return code

    def __generate_managed_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [self.__get_cpp_type__(arg.type_, False, arg.called_by) + ' ' + arg.name for arg in func_.args]

        # Doxygen comment
        if func_.brief != None:
            code('/**')
            code(' @brief {}'.format(func_.brief.descs[self.lang]))
            for arg in func_.args:
                if arg.brief != None:
                    code(' @param {} {}'.format(arg.name,arg.brief.descs[self.lang]))
            code(' */')

            if func_.return_value.brief != None:
                code(' @return {}'.format(func_.return_value.brief.descs[self.lang]))

        # cache repo
        is_cache_mode = False
        is_cache_mode |= func_.return_value.cache_mode() == CacheMode.Cache
        is_cache_mode |= func_.return_value.cache_mode() == CacheMode.ThreadSafeCache
        if is_cache_mode:
            code.dec_indent()
            code('private:')
            code.inc_indent()
            return_type_name = self.__get_cpp_type__(func_.return_value.type_, is_return=True)
            cache_code = 'unordered_map<void*, std::weak_ptr<{}> > cache{};'
            code(cache_code.format(return_type_name, func_.name))

        if func_.is_constructor:
            code('{}({});'.format(class_.name, ', '.join(args)))
        elif func_.is_static:
            cpp_type = self.__get_cpp_type__(func_.return_value.type_, is_return=True)
            code('static {} {}({});'.format(cpp_type, func_.name, ', '.join(args)))
        else:
            cpp_type = self.__get_cpp_type__(func_.return_value.type_, is_return=True)
            code('{} {}({});'.format(cpp_type, func_.name, ', '.join(args)))

        return code

    def __generate_managed_prop__(self, class_: Class, prop_: Property) -> Code:
        code = Code()

        # cannot generate property with no getter and no setter
        if not prop_.has_getter and not prop_.has_setter:
            return code

        # Doxygen comment
        if prop_.brief != None:
            code('/**')
            code(' @brief {}'.format(prop_.brief.descs[self.lang]))
            code(' */')

        type_name = self.__get_cpp_type__(prop_.type_, is_return=True)
        if prop_.has_getter:
            code('{} get_{}();'.format(type_name, prop_.name))
        if prop_.has_setter:
            code('void set_{}({} value);'.format(prop_.name, type_name))

        return code

    def __generate_class__(self, class_: Class) -> Code:
        code = Code()

        # Doxygen comment
        if class_.brief != None:
            code('/**')
            code(' @brief {}'.format(class_.brief.descs[self.lang]))
            code(' */')

        # inheritance
        inheritance = ""
        inheritCount = 0
        if class_.base_class != None:
            inheritCount += 1
            inheritance = ' : public {}'.format(class_.base_class.name)

        # class body
        with CodeBlock(code, 'class {}{}'.format(class_.name, inheritance), False, True):

            # mutex
            code.dec_indent()
            code('private:')
            code.inc_indent()
            code('static std::mutex mtx;')

            # cache repo
            code('static std::unordered_map<void*, std::weak_ptr<{}> > cacheRepo;'.format(class_.name))
            code('')
            code.dec_indent()
            code('public:')
            code.inc_indent()
            code('static std::shared_ptr<{}> TryGetFromCache(void* native);'.format(class_.name))
            code('')
                

            # unmanaged pointer
            if class_.base_class == None:
                code.dec_indent()
                code('public:')
                code.inc_indent()
                code('void* {} = nullptr;'.format(self.self_ptr_name))
                code('')

            # extern unmanaged functions
            code.dec_indent()
            code('private:')
            code.inc_indent()
            for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'cplusplus' in f.targets]:
                code(str(self.__generate_unmanaged_func__(class_,func_)))
            for prop_ in class_.properties:
                if prop_.has_getter:
                    code(str(self.__generate_unmanaged_func__(class_,prop_.getter_as_func())))
                if prop_.has_setter:
                    code(str(self.__generate_unmanaged_func__(class_,prop_.setter_as_func())))

            # releasing function
            release_func = Function('Release')
            code(self.__generate_unmanaged_func__(class_, release_func))
            code('')

            # constructor
            code.dec_indent()
            code('public:')
            code.inc_indent()
            code('{}(void* handle);'.format(class_.name))
            code('')
                    
            # properties
            code.dec_indent()
            code('private:')
            code.inc_indent()
            for prop_ in class_.properties:
                if prop_.has_setter and prop_.has_getter:
                    type_name = self.__get_cpp_type__(prop_.type_, is_return=True)
                    code('{} _{};'.format(type_name, prop_.name))
            code('')
            code.dec_indent()
            code('public:')
            code.inc_indent()
            for prop_ in class_.properties:
                code(self.__generate_managed_prop__(class_, prop_))

            # managed functions
            for func_ in [f for f in class_.funcs if not f.onlyExtern and (len(f.targets) == 0 or 'cplusplus' in f.targets)]:
                code(self.__generate_managed_func__(class_, func_))

            # destructor
            code('/**')
            code(' @brief {}のインスタンスを削除します。'.format(class_.name))
            code(' */')
            code('~{}();'.format(class_.name))

        return code

    def generate(self):
        header_path = self.output_path

        code = Code()

        warning = textwrap.dedent('''\
            // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            //
            //   このファイルは自動生成されました。
            //   このファイルへの変更は消失することがあります。
            //
            //   THIS FILE IS AUTO GENERATED.
            //   YOUR COMMITMENT ON THIS FILE WILL BE WIPED. 
            //
            // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            // !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ''')

        code = Code()

        # add waring
        code(warning)

        # write include
        code('#pragma once')
        code('')
        code('#include <memory>')
        code('#include <mutex>')
        code('#include <string>')
        code('#include <unordered_map>')
        code('')
        code('#include "DynamicLinkLibrary.h"')
        for include in self.includes:
            code('#include "{}"'.format(include))
        code('')

        with CodeBlock(code, 'namespace {}'.format(self.namespace)):

            # load dynamic link library
            code('static std::shared_ptr<DynamicLinkLibrary> dll = nullptr;')
            code('')
            code('bool LoadLibrary();')
            code('')

            # enum group
            for enum_ in self.define.enums:
                code(self.__generate_enum__(enum_))

            # class prototype declaration
            for class_ in self.define.classes:
                code('class {};'.format(class_.name))
            code('')

            # class group
            for class_ in self.define.classes:
                code(self.__generate_class__(class_))

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(header_path, mode='w', encoding='utf-8', newline="\r\n") as f:
                f.write(str(code))