from typing import List
import ctypes

from .cpp_binding_generator import BindingGenerator, Define, DefineDependency, CacheMode, ArgCalledBy, Class, DefineDependency, Struct, Enum, Code, Property, Function, EnumValue, __get_c_func_name__
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

def camelcase_to_underscore(value : str) -> str:
    result = []
    beforeCharacter = ''
    value_len = len(value)

    for i in range(value_len):
        c = ''
        x = value[i]
        if x.isalnum() and x.isupper() and (beforeCharacter != '_'):
            if result and beforeCharacter.islower():
            # if result:
                c = '_'
            c = c + x.lower()
        else:
            c = x
        result.append(c)
        beforeCharacter = x

    return "".join(result)

keywords = {
    'as', 'box', 'break', 'const', 'continue', 'crate', 'else', 'enum', 'extern', 'false', 'fn',
    'for', 'if', 'impl', 'in', 'let', 'loop', 'match', 'mod', 'move', 'mut', 'pub', 'ref', 'return',
    'self', 'Self', 'static', 'struct', 'super', 'trait', 'true', 'type', 'unsafe', 'use', 'where', 'while'
}

def replaceKeyword(name):
    if name in keywords:
        return name + '_'
    return name

def is_cached(class_ : Class):
    return (class_.cache_mode == CacheMode.Cache or class_.cache_mode == CacheMode.ThreadSafeCache)

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
    def __init__(self, define: Define, dependencies : List[DefineDependency], lang: str):
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
        self.self_ptr_name = 'self_ptr'
        self.lang = lang
        self.ptr_type = '()'
        self.struct_module_name = 'create'
        self.struct_replace_map = {}
        self.base_classes: set = set()
        self.dependencies = dependencies

    def get_dependency_namespace(self, obj):
        for dependency in self.dependencies:
            if obj in dependency.define.classes:
                return dependency.namespace

            if obj in dependency.define.structs:
                return dependency.namespace

            if obj in dependency.define.enums:
                return dependency.namespace

        return ''

    def get_alias_or_name(self, type_) -> str:
        namespace = self.get_dependency_namespace(type_)
        if namespace != "":
            namespace += "::"

        if type_.alias == None:
            return namespace + type_.name
        else:
            return namespace + type_.alias

    def get_base_trait_name(self, class_: Class):
        return f'As{self.get_alias_or_name(class_)}'

    def __get_rs_type__(self, type_, is_return = False, is_property = False, called_by: ArgCalledBy = None) -> str:
        ptr = ''
        if called_by == ArgCalledBy.Out:
            ptr = '&mut '
        elif called_by == ArgCalledBy.Ref:
            ptr = '&'

        if type_ == ctypes.c_byte:
            return ptr + 'u8'

        if type_ == int:
            return ptr + 'i32'

        if type_ == float:
            return ptr + 'f32'

        if type_ == bool:
            return ptr + 'bool'

        if type_ == ctypes.c_void_p:
            return f'*mut {self.ptr_type}'

        if type_ == ctypes.c_wchar_p:
            if is_return or is_property:
                return 'String'
            return '&str'

        defines = [d.define for d in self.dependencies] + [self.define]

        for define in defines:

            if type_ in define.classes:
                type_name = self.get_alias_or_name(type_)
                if is_property:
                    
                    if type_ in self.base_classes:
                        if type_.cache_mode == CacheMode.ThreadSafeCache:
                            type_name = f'Arc<Mutex<dyn {self.get_base_trait_name(type_)}>>'
                        elif type_.cache_mode == CacheMode.Cache:
                            type_name = f'Rc<RefCell<dyn {self.get_base_trait_name(type_)}>>'
                    else:
                        if type_.cache_mode == CacheMode.ThreadSafeCache:
                            type_name = f'Arc<Mutex<{type_name}>>'
                        elif type_.cache_mode == CacheMode.Cache:
                            type_name = f'Rc<RefCell<{type_name}>>'

                    if is_return:
                        type_name = f'Option<{type_name}>'
                    
                    return type_name

                elif is_return:
                    if type_.cache_mode == CacheMode.ThreadSafeCache:
                        # if type_ in self.base_classes:
                        #     type_name = 'Arc<Mutex<dyn {}>>'.format(self.get_base_trait_name(type_))
                        # else:
                        type_name = f'Arc<Mutex<{type_name}>>'
                    elif type_.cache_mode == CacheMode.Cache:
                        # if type_ in self.base_classes:
                        #     type_name = 'Rc<RefCell<dyn {}>>'.format(self.get_base_trait_name(type_))
                        # else:
                        type_name = f'Rc<RefCell<{type_name}>>'
                    
                    return f'Option<{type_name}>'

                elif type_ in self.base_classes:
                    return f'&mut dyn {self.get_base_trait_name(type_)}'
                else:
                    return f'&mut {type_name}'

            if type_ in define.structs:
                return ptr + self.struct_replace_map.get(type_, f'{self.struct_module_name}::{type_.alias}')

            if type_ in define.enums:
                return self.get_alias_or_name(type_)

        if type_ is None:
            return '()'

        print(f'Type: {type_.name}')
        assert(False)

    def __get_rsc_type__(self, type_, is_return = False, called_by: ArgCalledBy = None) -> str:
        ptr = ''
        if called_by == ArgCalledBy.Out:
            ptr = '*mut '
        elif called_by == ArgCalledBy.Ref:
            ptr = '*const '

        if type_ == ctypes.c_void_p:
            return f'*mut {self.ptr_type}'

        if type_ == ctypes.c_byte:
            return ptr + 'c_uchar'

        if type_ == int:
            return ptr + 'c_int'

        if type_ == float:
            return ptr + 'c_float'

        if type_ == bool:
            return ptr + 'bool'

        if type_ == ctypes.c_wchar_p:
            return '*const u16'

        if type_ == ctypes.c_void_p:
            return f'*mut {self.ptr_type}'

        defines = [d.define for d in self.dependencies] + [self.define]

        for define in defines:
            if type_ in define.classes:
                return f'*mut {self.ptr_type}'

            if type_ in define.structs:
                value_ = self.struct_replace_map.get(type_, f'{self.struct_module_name}::{type_.alias}')
                if is_return:
                    return value_
                else:
                    return ptr + value_

            if type_ in define.enums:
                return 'c_int'

        if type_ is None:
            if is_return:
                return '()'
            
            return ''

        print(f'Unsupported Type: {type_}')
        assert(False)

    def __convert_rsc_to_rs__(self, type_, name: str, is_property = False, called_by: ArgCalledBy = None) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_byte:
            if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref:
                return f'{name} as {self.__get_rsc_type__(type_, called_by=called_by)}'
            else:
                return name

        if type_ == ctypes.c_void_p:
            return name

        if type_ == ctypes.c_wchar_p:
            return f'encode_string(&{name}).as_ptr()'

        defines = [d.define for d in self.dependencies] + [self.define]

        for define in defines:
            if type_ in define.classes:
                if is_property:
                    if type_.cache_mode == CacheMode.ThreadSafeCache:
                        return f'{name}.lock().unwrap_or_else(|| panic!("Failed to get lock of {self.get_alias_or_name(type_)}")).{self.self_ptr_name}()'
                    elif type_.cache_mode == CacheMode.Cache:
                        return f'{name}.borrow_mut().{self.self_ptr_name}()'
                
                return f'{name}.{self.self_ptr_name}'

            if type_ in define.structs:
                if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref:
                    return f'{name} as {self.__get_rsc_type__(type_, called_by=called_by)}'
                else:
                    return f'{name}.clone()'

            if type_ in define.enums:
                if type_.isFlag:
                    return f'{name}.bits as i32'
                else:
                    return f'{name} as i32'

        if type_ is None:
            return '()'

        print(f'Type: {type_.name}')
        assert(False)

    def __convert_ret__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_byte or type_ == ctypes.c_void_p:
            return name

        if type_ == ctypes.c_wchar_p:
            return f'decode_string({name})'

        defines = [d.define for d in self.dependencies] + [self.define]

        for define in defines:
            if type_ in define.classes:
                if is_cached(type_):
                    return f'{{ let ret = {self.get_alias_or_name(type_)}::__try_get_from_cache({name})?; Some(ret) }}'
                else:
                    return f'{self.get_alias_or_name(type_)}::cbg_create_raw({name})'

            if type_ in define.structs:
                return name

            if type_ in define.enums:
                if type_.isFlag:
                    return f'{self.get_alias_or_name(type_)}::from_bits_truncate({name})'
                else:
                    return f'unsafe {{ std::mem::transmute({name}) }}'

        print(f'Unsupported Type: {type_}')
        assert(False)

    def __generate__unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [replaceKeyword(arg.name) + ': ' + self.__get_rsc_type__(arg.type_, called_by=arg.called_by)
            for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = [f'{self.self_ptr_name}: *mut {self.ptr_type}'] + args
        
        joined_args = ', '.join(args)
        code(f'fn {fname}({joined_args}) -> {self.__get_rsc_type__(func_.return_value.type_, is_return=True)};')

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

        code(f'#[link(name = "{self.dll_name}", kind="dylib")]')
        with CodeBlock(code, 'extern'):
            release_func = Function('Release')

            for class_ in self.define.classes:
                # extern unmanaged functions
                for func_ in class_.funcs:
                    code(self.__generate__unmanaged_func__(class_, func_))
                for prop_ in class_.properties:
                    code(self.__generate__unmanaged_property_(class_, prop_))

                # releasing function
                code(self.__generate__unmanaged_func__(class_, release_func))

        return code


    def __write_managed_function_body__(self, code: Code, class_: Class, func_: Function, is_property=False):
        fname = __get_c_func_name__(class_, func_)
        # call a function
        args = [self.__convert_rsc_to_rs__(
                arg.type_, camelcase_to_underscore(replaceKeyword(arg.name)), is_property=is_property, called_by=arg.called_by) for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = [f'self.{self.self_ptr_name}'] + args

        joined_args = ', '.join(args)
        
        if func_.is_constructor:
            code(f'Self::cbg_create_raw(unsafe{{ {fname}({joined_args}) }})')
        else:
            func_code = f'unsafe {{ {fname}({joined_args}) }}'
            if func_.return_value.type_ is None:
                code(func_code)
            else:
                code(f'let ret = {func_code};')
                code(self.__convert_ret__(func_.return_value.type_, 'ret'))

    def __generate_func_brief__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        # Markdown comment
        if func_.brief != None:
            code(f'/// {func_.brief.descs[self.lang]}')

            # not empty
            # if func_.args:
            if any(map(lambda x: x.brief != None, func_.args)):
                code('/// # Arguments')

            for arg in func_.args:
                if arg.brief != None:
                    code(f'/// * `{camelcase_to_underscore(replaceKeyword(arg.name))}` - {arg.brief.descs[self.lang]}')
        return code

    def __managed_func_declare__(self, class_: Class, func_: Function, add_accessor=True) -> str:
        args = []
        index_ = 0
        generic_ = []
        for arg in func_.args:
            if arg.type_ in self.base_classes:
                args.append(f'{camelcase_to_underscore(replaceKeyword(arg.name))}: &mut T{index_}')
                generic_.append(f'T{index_}: {self.get_base_trait_name(arg.type_)}')
                index_ += 1
            else:
                arg_str = camelcase_to_underscore(replaceKeyword(arg.name)) \
                    + ' : ' \
                    + self.__get_rs_type__(arg.type_, is_return=False, is_property=False, called_by=arg.called_by)

                args.append(arg_str)

        if not func_.is_static and not func_.is_constructor:
            args = [ "&mut self" ] + args

        # access signature
        access = ''
        func_name = camelcase_to_underscore(func_.name)
        if add_accessor:
            if func_.is_public:
                access = 'pub '
            else:
                access = 'pub(crate) '
                if class_.is_public:
                    func_name = '__' + func_name
        
        joined_types = ', '.join(generic_)
        joined_args = ', '.join(args)

        if func_.is_constructor:
            return f'{access}fn new<{joined_types}>({joined_args}) -> {self.__get_rs_type__(class_, is_return=True)}'
        else:
            return f'{access}fn {func_name}<{joined_types}>({joined_args}) -> {self.__get_rs_type__(func_.return_value.type_, is_return=True)}'


    def __generate__managed_func__(self, class_: Class, func_: Function, add_accessor=True) -> Code:
        code = Code()

        code(self.__generate_func_brief__(class_, func_))

        func_title = self.__managed_func_declare__(class_, func_, add_accessor=add_accessor)
        # function body
        with CodeBlock(code, func_title):
            self.__write_managed_function_body__(code, class_, func_)

        return code

    def __generate__manaded_property_getter__(self, class_: Class, prop_:Property, is_trait=False) -> Code:
        code = Code()
        if not prop_.has_getter:
            return code
        
        type_name_return = self.__get_rs_type__(prop_.type_, is_return=True, is_property=True)

        field_name = camelcase_to_underscore(prop_.name)

        access = ''
        prop_name = 'get_' + field_name
        if not is_trait:
            if prop_.is_public:
                access = 'pub '
            else:
                access = 'pub(crate) '
                if class_.is_public:
                    prop_name = '__get_' + field_name

        # Markdown comment
        if prop_.brief != None:
            code(f'/// {prop_.brief.descs[self.lang]}')
        with CodeBlock(code, f'{access}fn {prop_name}(&mut self) -> {type_name_return}'):
            self.__write_managed_function_body__(code, class_, prop_.getter_as_func())

        return code

    def __generate__manaded_property_setter__(self, class_: Class, prop_:Property, is_trait=False) -> Code:
        code = Code()
        # cannot generate property with no getter and no setter
        if not prop_.has_getter and not prop_.has_setter:
            return code
        
        type_name = self.__get_rs_type__(prop_.type_, is_property=True)

        field_name = camelcase_to_underscore(prop_.name)

        access = ''
        prop_name = 'set_' + field_name
        if not is_trait:
            if prop_.is_public:
                access = 'pub '
            else:
                access = 'pub(crate) '
                if class_.is_public:
                    prop_name = '__set_' + field_name

        if prop_.has_setter:
            # Markdown comment
            if prop_.brief != None:
                code(f'/// {prop_.brief.descs[self.lang]}')

            mut_ = 'mut ' if isinstance(prop_.type_, Struct) else ''

            generic_ = ''
            if prop_.type_ in self.base_classes:
                type_name = 'T'
                if prop_.type_.cache_mode == CacheMode.Cache:
                    type_name = 'Rc<RefCell<T>>'
                elif prop_.type_.cache_mode == CacheMode.ThreadSafeCache:
                    type_name = 'Arc<Mutex<T>>'
                generic_ = f'T: {self.get_base_trait_name(prop_.type_)} + \'static'

            head = f'{access}fn {prop_name}<{generic_}>(&mut self, {mut_}value : {type_name})'

            if is_trait:
                head = f'{access}fn {prop_name}<{generic_}>(&mut self, {mut_}value : {type_name})'

            with CodeBlock(code, head):
                self.__write_managed_function_body__(code, class_, prop_.setter_as_func(), is_property=True)

        return code


    def __generate__managed_property_(self, class_: Class, prop_:Property, is_trait=False) -> Code:
        code = Code()

        if prop_.has_getter:
            code(self.__generate__manaded_property_getter__(class_, prop_, is_trait=is_trait))
        if prop_.has_setter:
            code(self.__generate__manaded_property_setter__(class_, prop_, is_trait=is_trait))

        return code


    def __generate_enum__(self, enum_ : Enum) -> Code:
        code = Code()

        access = 'pub'

        if enum_.isFlag:

            with CodeBlock(code, "bit_flags!"):
                # Markdown comment
                if enum_.brief != None:
                    code(f'/// enum_.brief.descs[self.lang]')

                with CodeBlock(code, f"{access} struct {self.get_alias_or_name(enum_)}: i32"):
                    int_value = 0
                    for val in enum_.values:
                        if val.name == 'MAX':
                            continue
                            
                        if val.brief != None:
                            code(f'/// {val.brief.descs[self.lang]}')

                        val_name = camelcase_to_underscore(val.name).upper()
                        if val.value != None:
                            code(f'const {val_name} = {val.value};')
                            int_value = val.value + 1
                        else:
                            code(f'const {val_name} = {int_value};')
                            int_value += 1
        else:
            # Markdown comment
            if enum_.brief != None:
                code(f'/// {enum_.brief.descs[self.lang]}')
            
            code('#[repr(C)]')
            code('#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]')
            with CodeBlock(code, f"{access} enum {self.get_alias_or_name(enum_)}"):
                int_value = 0
                for val in enum_.values:
                    if val.brief != None:
                        code(f'/// {val.brief.descs[self.lang]}')
                    if val.value != None:
                        code(f'{val.name} = {val.value},')
                    else:
                        code(f'{val.name},')

        return code

    def __generate_class__(self, class_: Class) -> Code:
        code = Code()

        distincted_funcs = {}
        distincted_props = {}

        for f in class_.funcs:
            distincted_funcs[f.name] = (class_, f)

        for p in class_.properties:
            distincted_props[p.name] = (class_, p)

        base_classes = []
        base_funcs = {}
        base_props = {}
        current = class_
        while current.base_class != None:
            if current.base_class == current:
                assert('infinit inheritance')
            base_classes.append(current.base_class)
            for f in current.base_class.funcs:
                if not f.name in distincted_funcs:
                    distincted_funcs[f.name] = (current.base_class, f)
                if not f.name in base_funcs and not (f.is_static or f.is_constructor):
                    base_funcs[f.name] = f
            for p in current.base_class.properties:
                if not p.name in distincted_props:
                    distincted_props[p.name] = (current.base_class, p)
                if not p.name in base_props:
                    base_props[p.name] = (current.base_class, p)
            current = current.base_class

        # Markdown comment
        if class_.brief != None:
            code(f'/// {class_.brief.descs[self.lang]}')
        
        access = ''
        if class_.is_public:
            access = 'pub'
        else:
            access = 'pub(crate)'

        class_name = self.get_alias_or_name(class_)

        code('#[derive(Debug)]')
        with CodeBlock(code, f'{access} struct {class_name}'):
            # unmanaged pointer
            code(f'{self.self_ptr_name} : *mut {self.ptr_type},')

        if class_.cache_mode == CacheMode.ThreadSafeCache:
            code(f'''
unsafe impl Send for {class_name} {{ }}
unsafe impl Sync for {class_name} {{ }}''')

        code(f'''
impl HasRawPtr for {class_name} {{
    fn {self.self_ptr_name}(&mut self) -> *mut {self.ptr_type} {{
        self.{self.self_ptr_name}.clone()
    }}
}}
''')

        if class_ in self.base_classes:
            inherits = f': std::fmt::Debug + HasRawPtr'
            # not empty
            if base_classes:
                inherits = inherits + ' + ' + (' + '.join(map(lambda x: x.name + 'Trait', base_classes)))

            with CodeBlock(code, f'pub trait {self.get_base_trait_name(class_)} {inherits}'):
                for func_ in [pair[1] for pair in distincted_funcs.values() if (len(pair[1].targets) == 0) or ('rust' in pair[1].targets) and (not pair[1] in base_funcs)]:
                    if not (func_.is_static or func_.is_constructor):
                        code(self.__generate_func_brief__(class_, func_))
                        code(self.__managed_func_declare__(class_, func_, add_accessor=False) + ';')

                for prop_ in [pair[1] for pair in distincted_props.values() if (not pair[1] in base_props)]:
                    type_name = self.__get_rs_type__(prop_.type_, is_property=True)
                    type_name_return = self.__get_rs_type__(prop_.type_, is_return=True)
                    field_name = camelcase_to_underscore(prop_.name)

                    if prop_.has_getter:
                        # Markdown comment
                        if prop_.brief != None:
                            code(f'/// {prop_.brief.descs[self.lang]}')
                        code(f'fn get_{field_name}(&mut self) -> {type_name_return};')

                    if prop_.has_setter:
                        # Markdown comment
                        if prop_.brief != None:
                            code(f'/// {prop_.brief.descs[self.lang]}')
                        code(f'fn set_{field_name}(&mut self, value : {type_name});')
            code('')

            base_classes.append(class_)

        for base_class in base_classes:
            with CodeBlock(code, f'impl {self.get_base_trait_name(base_class)} for {class_name}'):
                for func_ in [f for f in base_class.funcs if len(f.targets) == 0 or 'rust' in f.targets]:
                    if not (func_.is_static or func_.is_constructor):
                        code(self.__generate__managed_func__(base_class, func_, add_accessor=False))

                for prop_ in base_class.properties:
                    code(self.__generate__managed_property_(base_class, prop_, is_trait=True))

            code('')

        with CodeBlock(code, f'impl {class_name}'):
            # unmanaged constructor
            ret_type = 'Self'
            if class_.cache_mode == CacheMode.Cache:
                ret_type = 'Rc<RefCell<Self>>'
            elif class_.cache_mode == CacheMode.ThreadSafeCache:
                ret_type = 'Arc<Mutex<Self>>'
            
            with CodeBlock(code, f'fn cbg_create_raw({self.self_ptr_name} : *mut {self.ptr_type}) -> Option<{ret_type}>', True):
                code(f'if {self.self_ptr_name} == NULLPTR {{ return None; }}')

                code('Some(')
                code.inc_indent()
                if class_.cache_mode == CacheMode.Cache:
                    code('Rc::new(RefCell::new(')
                    code.inc_indent()
                elif class_.cache_mode == CacheMode.ThreadSafeCache:
                    code('Arc::new(Mutex::new(')
                    code.inc_indent()
                
                with CodeBlock(code, class_name):
                    code(f'{self.self_ptr_name},'.format())

                if is_cached(class_):
                    code.dec_indent()
                    code('))')
                
                code.dec_indent()
                code(')')

            body = ''
            if class_.cache_mode == CacheMode.Cache:
                body = '''
pub fn __try_get_from_cache({0} : *mut {1}) -> Option<Rc<RefCell<Self>>> {{
    thread_local! {{
        static {2}_CACHE: RefCell<HashMap<RawPtrStorage, rc::Weak<RefCell<{3}>>>> = RefCell::new(HashMap::new());
    }}
    {2}_CACHE.with(|hash_map| {{
        let mut hash_map = hash_map.borrow_mut();
        let storage = RawPtrStorage({0});
        if let Some(x) = hash_map.get(&storage) {{
            match x.upgrade() {{
                Some(o) => {{ return Some(o); }},
                None => {{ hash_map.remove(&storage); }},
            }}
        }}
        let o = Self::cbg_create_raw({0})?;
        hash_map.insert(storage, Rc::downgrade(&o));
        Some(o)
    }})
}}
'''.format(self.self_ptr_name, self.ptr_type, class_name.upper(), class_name)

            elif class_.cache_mode == CacheMode.ThreadSafeCache:
                body = '''
pub fn __try_get_from_cache({0} : *mut {1}) -> Option<Arc<Mutex<Self>>> {{
    lazy_static! {{
        static ref {2}_CACHE: RwLock<HashMap<RawPtrStorage, sync::Weak<Mutex<{3}>>>> = RwLock::new(HashMap::new());
    }}
    let mut hash_map = {2}_CACHE.write().unwrap();
    let storage = RawPtrStorage({0});
    if let Some(x) = hash_map.get(&storage) {{
        match x.upgrade() {{
            Some(o) => {{ return Some(o); }},
            None => {{ hash_map.remove(&storage); }},
        }}
    }}
    let o = Self::cbg_create_raw({0})?;
    hash_map.insert(storage, Arc::downgrade(&o));
    Some(o)
}}
'''.format(self.self_ptr_name, self.ptr_type, class_name.upper(), class_name)

            lines = body.split('\n')
            for line in lines:
                code(line)

            if class_ in self.base_classes:
                for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'rust' in f.targets]:
                    if func_.is_static or func_.is_constructor:
                        code(self.__generate__managed_func__(class_, func_))

                # setter
                for pair in distincted_props.values():
                    code(self.__generate__manaded_property_setter__(pair[0], pair[1]))

            else:
                for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'rust' in f.targets]:
                    if not (func_.name in base_funcs):
                        code(self.__generate__managed_func__(class_, func_))

                for prop_ in class_.properties:
                    if not (prop_.name in base_props):
                        code(self.__generate__manaded_property_getter__(class_, prop_))
                        code(self.__generate__manaded_property_setter__(class_, prop_))

        code('')

        # destructor
        with CodeBlock(code, f'impl Drop for {class_name}'):
            with CodeBlock(code, 'fn drop(&mut self)'):
                # with CodeBlock(code, 'if !self.{}.is_null()'.format(self.self_ptr_name)):
                code(f'unsafe {{ {__get_c_release_func_name__(class_)}(self.{self.self_ptr_name}) }};')
                    # code('self.{} = std::ptr::null_mut();'.format(self.self_ptr_name))

        return code


    def generate(self):
        code = Code()

        # add Waring
        code('// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        code('//')
        code('//   このファイルは自動生成されました。')
        code('//   このファイルへの変更は消失することがあります。')
        code('//')
        code('//   THIS FILE IS AUTO GENERATED.')
        code('//   YOUR COMMITMENT ON THIS FILE WILL BE WIPED. ')
        code('//')
        code('// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        code('')

        # declare module
        if self.module != '':
            code('mod {} {{'.format(self.module))
            code.inc_indent()

        code('''#![allow(dead_code)]
#![allow(unused_imports)]
use std::ffi::c_void;
use std::os::raw::*;

use std::rc::{{self, Rc}};
use std::cell::RefCell;
use std::sync::{{self, Arc, RwLock, Mutex}};
use std::collections::HashMap;

const NULLPTR: *mut {0} = 0 as *mut {0};

pub trait HasRawPtr {{
    fn {1}(&mut self) -> *mut {0};
}}

#[derive(Debug, PartialEq, Eq, Hash)]
struct RawPtrStorage(*mut {0});

unsafe impl Send for RawPtrStorage {{ }}
unsafe impl Sync for RawPtrStorage {{ }}

fn decode_string(source: *const u16) -> String {{
    unsafe {{
        let len = (0..).take_while(|&i| *source.offset(i) != 0).count();
        let slice = std::slice::from_raw_parts(source, len);
        String::from_utf16_lossy(slice)
    }}
}}

fn encode_string(s: &str) -> Vec<u16> {{
    let mut v: Vec<u16> = s.encode_utf16().collect();
    v.push(0);
    v
}}
'''.format(self.ptr_type, self.self_ptr_name))

        # enum group
        for enum_ in self.define.enums:
            if len(enum_.values) > 0:
                code(self.__generate_enum__(enum_))

        code(self.__generate_extern__(self.define.classes))

        for class_ in self.define.classes:
            if class_.base_class != None:
                self.base_classes.add(class_.base_class)
        
        # class group
        for class_ in self.define.classes:
            code(self.__generate_class__(class_))

        # close module
        if self.module != '':
            code.dec_indent()
            code('}')

        if self.output_path == '':
            print('please specify an output path')
        else:
            with open(self.output_path, mode='w', encoding='utf-8', newline="\r\n") as f:
                f.write(str(code))