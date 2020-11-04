from typing import List
import ctypes
import os, re, textwrap

from ..cpp_binding_generator import *
from ..cpp_binding_generator import __get_c_func_name__
from ..cpp_binding_generator import __get_c_release_func_name__, __get_c_addref_func_name__

from .code_block import CodeBlock

class BindingGeneratorCPlusPlusSrc(BindingGenerator):
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
                return 'std::shared_ptr<{}>({} != nullptr ? new {}({}) : nullptr)'.format(type_.name, name, type_.name, name)

        if type_ in self.define.structs:
            return '{}'.format(name)

        if type_ in self.define.enums:
            enum_name = type_.name if type_.alias == None else type_.alias
            return '({}){}'.format(enum_name, name)

        assert(False)

    def __generate_unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        func_name = __get_c_func_name__(class_, func_)

        args_def = [self.__get_cppc_type__(arg.type_, False, arg.called_by) + ' ' + arg.name for arg in func_.args]
        args_use = [arg.name for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args_def = ['void* {}'.format(self.self_ptr_name)] + args_def
            args_use = [self.self_ptr_name] + args_use

        return_type = self.__get_cppc_type__(func_.return_value.type_, is_return=True)
        with CodeBlock(code, '{} {}::{}({})'.format(return_type, class_.name, func_name, ', '.join(args_def))):
            code('typedef {} (*proc_t)({});'.format(return_type, ', '.join(args_def)))
            code('static proc_t proc = GetLibrary()->GetProc<proc_t>("{}");'.format(func_name))
            if func_.return_value.type_ == None:
                code('proc({});'.format(', '.join(args_use)))
            else:
                code('return proc({});'.format(', '.join(args_use)))

        return code

    def __generate_unmanaged_prop__(self, class_: Class, prop_: Property) -> Code:
        code = Code()
        result = ''
        if prop_.has_getter:
            result += str(self.__generate_unmanaged_func__(class_,prop_.getter_as_func()))
        if prop_.has_setter:
            result += str(self.__generate_unmanaged_func__(class_,prop_.setter_as_func()))
        code(result)
        return code

    def __write_managed_function_body__(self, code: Code, class_: Class, func_: Function, callByDerived_ = False):
        fname = __get_c_func_name__(class_, func_)
        # call a function
        args = [self.__convert_cppc_to_cpp__(arg.type_, arg.name, arg.called_by) for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = [self.self_ptr_name] + args
        
        for a in func_.args:
            if not a.nullable and isinstance(a.type_, Class):
                code('if({} == nullptr) throw "{}の引数がnullです"'.format(a.name, a.name))

        if func_.is_constructor:
            if callByDerived_:
                code('// Dummy function.')
            else:
                code('{} = {}({});'.format(self.self_ptr_name, fname, ', '.join(args)))
        elif func_.return_value.type_ is None:
            code('{}({});'.format(fname, ', '.join(args)))
        else:
            code('auto ret = {}({});'.format(fname, ', '.join(args)))
            code('return {};'.format(self.__convert_ret__(func_.return_value.type_, 'ret')))

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
            return_type_name = self.__get_cpp_type__(func_.return_value.type_, is_return=True)
            cache_code = 'unordered_map<void*, std::weak_ptr<{}> > cache{};'
            code(cache_code.format(return_type_name, func_.name))

        if func_.is_constructor:
            func_title = '{}::{}({})'.format(class_.name, class_.name, ', '.join(['bool calledByDerived'] + args))
            if class_.base_class != None:
                nameArgs = ', '.join(['calledByDerived'] + [arg.name for arg in func_.args])
                func_title += ' : {}({})'.format(class_.base_class.name, nameArgs)
            with CodeBlock(code, func_title):
                self.__write_managed_function_body__(code, class_, func_, True)
            code('')
            func_title = '{}::{}({})'.format(class_.name, class_.name, ', '.join(args))
            if class_.base_class != None:
                nameArgs = ', '.join(['true'] + [arg.name for arg in func_.args])
                func_title += ' : {}({})'.format(class_.base_class.name, nameArgs)
            with CodeBlock(code, func_title):
                self.__write_managed_function_body__(code, class_, func_)
        else:
            cpp_type = self.__get_cpp_type__(func_.return_value.type_, is_return=True)
            func_title = '{} {}::{}({})'.format(cpp_type, class_.name, func_.name, ', '.join(args))
            with CodeBlock(code, func_title):
                self.__write_managed_function_body__(code, class_, func_)

        return code

    def __write_getter__(self, code: Code, class_: Class, prop_: Property):
        type_name = self.__get_cpp_type__(prop_.type_, is_return=True)
        with CodeBlock(code, '{} {}::get_{}()'.format(type_name, class_.name, prop_.name)):
            if prop_.has_setter:
                code('return _{};'.format(prop_.name))
            self.__write_managed_function_body__(code, class_, prop_.getter_as_func())

    def __write_setter__(self, code: Code, class_: Class, prop_: Property):
        type_name = self.__get_cpp_type__(prop_.type_, is_return=True)
        with CodeBlock(code, 'void {}::set_{}({} value)'.format(class_.name, prop_.name, type_name)):
            if prop_.has_getter:
                if isinstance(prop_.type_, Class):
                    if not prop_.nullable:
                        code('if(value == nullptr) throw "set_{}の引数がnullです"'.format(prop_name))
                    code('_{} = value;'.format(prop_.name))
                else:
                    code('_{} = value;'.format(prop_.name))
            func_ = prop_.setter_as_func()
            if prop_.type_ == ctypes.c_wchar_p:
                func_.args[0] = '{}.c_str()'.format(func_.args[0])
            self.__write_managed_function_body__(code, class_, prop_.setter_as_func())

    def __generate_managed_prop__(self, class_: Class, prop_: Property) -> Code:
        code = Code()

        # cannot generate property with no getter and no setter
        if not prop_.has_getter and not prop_.has_setter:
            return code

        if prop_.has_getter:
            self.__write_getter__(code, class_, prop_)
        if prop_.has_setter:
            self.__write_setter__(code, class_, prop_)

        return code

    def __write_cache_getter__(self, code: Code, class_: Class, thread_safe_mode = False):
        release_func_name = __get_c_func_name__(class_, Function('Release'))

        func_head = 'std::shared_ptr<{}> {}::TryGetFromCache(void* native)'

        with CodeBlock(code, func_head.format(class_.name, class_.name)):
            code('if(native == nullptr) return nullptr;')
            code('')
            with CodeBlock(code, 'if(cacheRepo.count(native))'):
                code('std::shared_ptr<{}> cacheRet = cacheRepo[native].lock();'.format(class_.name))
                with CodeBlock(code, 'if(cacheRet.get() != nullptr)'):
                    code('{}(native);'.format(release_func_name))
                    code('return cacheRet;')
                with CodeBlock(code, 'else'):
                    if thread_safe_mode:
                        code('if(cacheRepo.count(native)) cacheRepo.erase(native);')
                    else:
                        code('cacheRepo.erase(native);')
            code('')
            code('std::shared_ptr<{0}> newObject(new {0}(native));'.format(class_.name))
            if thread_safe_mode:
                code('if(!cacheRepo.count(native)) cacheRepo[native] = newObject;')
            else:
                code('cacheRepo[native] = newObject;')
            code('return newObject;')
        code('')

    def __generate_class__(self, class_: Class) -> Code:
        code = Code()

        # mutex
        code('std::mutex {}::mtx;'.format(class_.name))
        code('')

        # cache repo
        code('std::unordered_map<void*, std::weak_ptr<{}> > {}::cacheRepo;'.format(class_.name, class_.name))
        if class_.cache_mode == CacheMode.Cache:
            self.__write_cache_getter__(code, class_, False)
        elif class_.cache_mode == CacheMode.ThreadSafeCache:
            self.__write_cache_getter__(code, class_, True)
        code('')

        # extern unmanaged functions
        for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'cplusplus' in f.targets]:
            code(str(self.__generate_unmanaged_func__(class_,func_)))
        for prop_ in class_.properties:
            if prop_.has_getter:
                code(str(self.__generate_unmanaged_func__(class_,prop_.getter_as_func())))
            if prop_.has_setter:
                code(str(self.__generate_unmanaged_func__(class_,prop_.setter_as_func())))

        # releasing function
        addref_func = Function('AddRef')
        code(self.__generate_unmanaged_func__(class_, addref_func))

        # releasing function
        release_func = Function('Release')
        code(self.__generate_unmanaged_func__(class_, release_func))

        # constructor
        class_title = '{}::{}(void* handle)'.format(class_.name, class_.name)
        if class_.base_class != None:
            class_title += ' : {}(handle)'.format(class_.base_class.name)
        with CodeBlock(code, class_title, True):
            code('{} = handle;'.format(self.self_ptr_name))
                
        # properties
        for prop_ in class_.properties:
            code(self.__generate_managed_prop__(class_, prop_))

        # managed functions
        for func_ in [f for f in class_.funcs if not f.onlyExtern and (len(f.targets) == 0 or 'cplusplus' in f.targets)]:
            code(self.__generate_managed_func__(class_, func_))

        # destructor
        with CodeBlock(code, '{}::~{}()'.format(class_.name, class_.name)):
            code('std::lock_guard<std::mutex> lock(mtx);')
            with CodeBlock(code, 'if ({} != nullptr)'.format(self.self_ptr_name)):
                code('{}({});'.format(__get_c_release_func_name__(class_), self.self_ptr_name))
                code('{} = nullptr;'.format(self.self_ptr_name))

        return code

    def generate(self):
        header_path = self.output_path
        source_path = re.sub('.h$', '.cpp', self.output_path)

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

        # add waring
        code(warning)

        # write include
        code('#include "{}"'.format(os.path.basename(header_path)))
        code('')

        with CodeBlock(code, 'namespace {}'.format(self.namespace)):

            code('static std::shared_ptr<DynamicLinkLibrary> dll = nullptr;')

            with CodeBlock(code, 'std::shared_ptr<DynamicLinkLibrary>& GetLibrary()'):
                code('if(dll != nullptr) return dll;')
                code('dll = std::shared_ptr<DynamicLinkLibrary>(new DynamicLinkLibrary());')
                code('if(!dll->Load(ConvertSharedObjectPath("{}").c_str())) dll = nullptr;'.format(self.dll_name))
                code('return dll;')
            code('')

            # class group
            for class_ in self.define.classes:
                code(self.__generate_class__(class_))

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(source_path, mode='w', encoding='utf-8', newline="\r\n") as f:
                f.write(str(code))