from typing import List
import ctypes

from .cpp_binding_generator import BindingGenerator, Define, CacheMode, ArgCalledBy, Class, Struct, Enum, Code, Property, Function, EnumValue, __get_c_func_name__
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

def get_base_trait_name(class_: Class):
    return 'As{}'.format(class_.name)

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
        self.self_ptr_name = 'self_ptr'
        self.lang = lang
        self.PtrEnumName = 'RawPtr'
        self.structModName = 'crate::structs'
        self.structsReplaceMap = {}
        self.bitFlags: set = set()
        self.baseClasses: set = set()

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
            return '*mut {}'.format(self.PtrEnumName)

        if type_ == ctypes.c_wchar_p:
            if is_return or is_property:
                return 'String'
            return '&str'

        if type_ in self.define.classes:
            if is_property:
                type_name = type_.name
                
                if type_ in self.baseClasses:
                    if type_.cache_mode == CacheMode.ThreadSafeCache:
                        type_name = 'Arc<Mutex<dyn {}>>'.format(get_base_trait_name(type_))
                    elif type_.cache_mode == CacheMode.Cache:
                        type_name = 'Rc<RefCell<dyn {}>>'.format(get_base_trait_name(type_))
                else:
                    if type_.cache_mode == CacheMode.ThreadSafeCache:
                        type_name = 'Arc<Mutex<{}>>'.format(type_.name)
                    elif type_.cache_mode == CacheMode.Cache:
                        type_name = 'Rc<RefCell<{}>>'.format(type_.name)

                if is_return:
                    type_name = 'Option<{}>'.format(type_name)
                
                return type_name

            elif is_return:
                type_name = type_.name
                
                if type_.cache_mode == CacheMode.ThreadSafeCache:
                    # if type_ in self.baseClasses:
                    #     type_name = 'Arc<Mutex<dyn {}>>'.format(get_base_trait_name(type_))
                    # else:
                    type_name = 'Arc<Mutex<{}>>'.format(type_.name)
                elif type_.cache_mode == CacheMode.Cache:
                    # if type_ in self.baseClasses:
                    #     type_name = 'Rc<RefCell<dyn {}>>'.format(get_base_trait_name(type_))
                    # else:
                    type_name = 'Rc<RefCell<{}>>'.format(type_.name)
                
                return 'Option<{}>'.format(type_name)

            elif type_ in self.baseClasses:
                return '&mut dyn {}'.format(get_base_trait_name(type_))
            else:
                return '&mut ' + type_.name

        if type_ in self.define.structs:
            return ptr + self.structsReplaceMap.get(type_, '{}::{}'.format(self.structModName, type_.alias))

        if type_ in self.define.enums:
            return type_.name

        if type_ is None:
            return '()'

        print('Type: {}'.format(type_))
        assert(False)

    def __get_rsc_type__(self, type_, is_return = False, called_by: ArgCalledBy = None) -> str:
        ptr = ''
        if called_by == ArgCalledBy.Out:
            ptr = '*mut '
        elif called_by == ArgCalledBy.Ref:
            ptr = '*const '

        if type_ == ctypes.c_void_p:
            return '*mut {}'.format(self.PtrEnumName)

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
            return '*mut {}'.format(self.PtrEnumName)

        if type_ in self.define.classes:
            return '*mut {}'.format(self.PtrEnumName)

        if type_ in self.define.structs:
            value_ = self.structsReplaceMap.get(type_, '{}::{}'.format(self.structModName, type_.alias))
            if is_return:
                return value_
            else:
                return ptr + value_

        if type_ in self.define.enums:
            return 'c_int'

        if type_ is None:
            if is_return:
                return '()'
            
            return ''

        print('Type: {}'.format(type_))
        assert(False)

    def __convert_rsc_to_rs__(self, type_, name: str, is_property = False, called_by: ArgCalledBy = None) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_byte:
            if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref:
                return  '{} as {}'.format(name, self.__get_rsc_type__(type_, called_by=called_by))
            else:
                return name

        if type_ == ctypes.c_void_p:
            return name

        if type_ == ctypes.c_wchar_p:
            return 'encode_string(&{}).as_ptr()'.format(name)

        if type_ in self.define.classes:
            if is_property:
                if type_.cache_mode == CacheMode.ThreadSafeCache:
                    return '{}.lock().expect("Failed to get lock of {}").{}()'.format(name, type_.name, self.self_ptr_name)
                elif type_.cache_mode == CacheMode.Cache:
                    return '{}.borrow_mut().{}()'.format(name, self.self_ptr_name)
            
            return '{}.{}()'.format(name, self.self_ptr_name)

        if type_ in self.define.structs:
            if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref:
                return  '{}.clone() as {}'.format(name, self.__get_rsc_type__(type_, called_by=called_by))
            else:
                return '{}.clone()'.format(name)

        if type_ in self.define.enums:
            if type_ in self.bitFlags:
                return '{}.bits as i32'.format(name)
            else:
                return '{} as i32'.format(name)

        if type_ is None:
            return '()'

        print('Type: {}'.format(type_))
        assert(False)

    def __convert_ret__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_byte or type_ == ctypes.c_void_p:
            return name

        if type_ == ctypes.c_wchar_p:
            return 'decode_string({})'.format(name)

        if type_ in self.define.classes:
            if is_cached(type_):
                return '{{ let ret = {}::try_get_from_cache({})?; Some(ret) }}'.format(type_.name, name)
            else:
                return '{}::cbg_create_raw({})'.format(type_.name, name)

        if type_ in self.define.structs:
            return name

        if type_ in self.define.enums:
            if type_ in self.bitFlags:
                return '{}::from_bits_truncate({})'.format(type_.name, name)
            else:
                return 'unsafe {{ std::mem::transmute({}) }}'.format(name)

        print('Type: {}'.format(type_))
        assert(False)

    def __generate__unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [replaceKeyword(arg.name) + ': ' + self.__get_rsc_type__(arg.type_, called_by=arg.called_by)
            for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = ['{}: *mut {}'.format(self.self_ptr_name, self.PtrEnumName)] + args
            
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
            args = ["self." + self.self_ptr_name] + args

        if func_.is_constructor:
            code('Self::cbg_create_raw(unsafe{{ {}({}) }})'.format(fname, ', '.join(args)))
        else:
            func_code = 'unsafe {{ {}({}) }}'.format(fname, ', '.join(args))
            if func_.return_value.type_ is None:
                code(func_code)
            else:
                code( 'let ret = {};'.format(func_code) )
                code(self.__convert_ret__(func_.return_value.type_, 'ret'))

    def __generate_func_brief__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        # Markdown comment
        if func_.brief != None:
            code('/// {}'.format(func_.brief.descs[self.lang]))

            # not empty
            # if func_.args:
            if any(map(lambda x: x.brief != None, func_.args)):
                code('/// # Arguments')

            for arg in func_.args:
                if arg.brief != None:
                    code('/// * `{}` - {}'.format(camelcase_to_underscore(replaceKeyword(arg.name)), arg.brief.descs[self.lang]))
        return code

    def __managed_func_declare__(self, class_: Class, func_: Function) -> str:
        args = []
        index_ = 0
        generic_ = []
        for arg in func_.args:
            if arg.type_ in self.baseClasses:
                args.append('{}: &mut T{}'.format(camelcase_to_underscore(replaceKeyword(arg.name)), index_))
                generic_.append('T{}: {}'.format(index_, get_base_trait_name(arg.type_)))
                index_ += 1
            else:
                args.append(('mut ' if arg.type_ in self.define.structs else '') + camelcase_to_underscore(replaceKeyword(arg.name)) + ' : ' + self.__get_rs_type__(arg.type_, is_return=False, is_property=False, called_by=arg.called_by))

        if not func_.is_static and not func_.is_constructor:
            args = [ "&mut self" ] + args

        if func_.is_constructor:
            return 'fn new<{}>({}) -> {}'.format(', '.join(generic_), ', '.join(args), self.__get_rs_type__(class_, is_return=True))
        else:
            return 'fn {}<{}>({}) -> {}'.format(
                camelcase_to_underscore(func_.name),
                ', '.join(generic_),
                ', '.join(args),
                self.__get_rs_type__(func_.return_value.type_, is_return=True))


    def __generate__managed_func__(self, class_: Class, func_: Function, add_accessor=True) -> Code:
        code = Code()

        code(self.__generate_func_brief__(class_, func_))

        # access signature
        access = ''
        if add_accessor:
            if func_.is_public:
                access = 'pub '
            else:
                access = 'pub(crate) '

        func_title = access + self.__managed_func_declare__(class_, func_)
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
        if not is_trait:
            access = 'pub '

        # Markdown comment
        if prop_.brief != None:
            code('/// {}'.format(prop_.brief.descs[self.lang]))
        with CodeBlock(code, '{}fn get_{}(&mut self) -> {}'.format(access, field_name, type_name_return)):
            if prop_.has_setter:
                if prop_.type_ in self.define.classes:
                    code('if let Some(value) = &self.{0} {{ return Some(value.clone()) }}'.format(field_name))
                else:
                    code('if let Some(value) = &self.{0} {{ return value.clone(); }}'.format(field_name))
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
        if not is_trait:
            access = 'pub '
        # if prop_.is_public:
        #     access = 'pub'
        # else:
        #     access = 'pub(crate)'

        if prop_.has_setter:
            # Markdown comment
            if prop_.brief != None:
                code('/// {}'.format(prop_.brief.descs[self.lang]))

            mut_ = 'mut ' if prop_.type_ in self.define.structs else ''

            generic_ = ''
            if prop_.type_ in self.baseClasses:
                type_name = 'T'
                if prop_.type_.cache_mode == CacheMode.Cache:
                    type_name = 'Rc<RefCell<T>>'
                elif prop_.type_.cache_mode == CacheMode.ThreadSafeCache:
                    type_name = 'Arc<Mutex<T>>'
                generic_ = 'T: {} + \'static'.format(get_base_trait_name(prop_.type_))

            head = '{}fn set_{}<{}>(&mut self, {}value : {}) -> &mut Self'.format(access, field_name, generic_, mut_, type_name)

            if is_trait:
                head = '{}fn base_set_{}<{}>(&mut self, {}value : {})'.format(access, field_name, generic_, mut_, type_name)

            with CodeBlock(code, head):
                self.__write_managed_function_body__(code, class_, prop_.setter_as_func(), is_property=True)
                if prop_.has_getter:
                    code('self.{} = Some(value.clone());'.format(field_name))
                if not is_trait:
                    code('self')

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

        if enum_ in self.bitFlags:

            with CodeBlock(code, "bitflags!"):
                # Markdown comment
                if enum_.brief != None:
                    code('/// {}'.format(enum_.brief.descs[self.lang]))

                with CodeBlock(code, "{} struct {}: i32".format(access, enum_.name)):
                    int_value = 0
                    for val in enum_.values:
                        if val.brief != None:
                            code('/// {}'.format(val.brief.descs[self.lang]))

                        val_name = camelcase_to_underscore(val.name).upper()
                        if val.value != None:
                            code('const {} = {};'.format(val_name, val.value))
                            int_value = val.value + 1
                        else:
                            code('const {} = {};'.format(val_name, int_value))
                            int_value += 1
        else:
            # Markdown comment
            if enum_.brief != None:
                code('/// {}'.format(enum_.brief.descs[self.lang]))
            
            code('#[repr(C)]')
            code('#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]')
            with CodeBlock(code, "{} enum {}".format(access, enum_.name)):
                int_value = 0
                for val in enum_.values:
                    if val.brief != None:
                        code('/// {}'.format(val.brief.descs[self.lang]))
                    if val.value != None:
                        code('{} = {},'.format(val.name, val.value))
                    else:
                        code('{},'.format(val.name))

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
                if not f.name in base_funcs:
                    base_funcs[f.name] = f
            for p in current.base_class.properties:
                if not p.name in distincted_props:
                    distincted_props[p.name] = (current.base_class, p)
                if not p.name in base_props:
                    base_props[p.name] = (current.base_class, p)
            current = current.base_class

        # Markdown comment
        if class_.brief != None:
            code('/// {}'.format(class_.brief.descs[self.lang]))
        
        access = ''
        if class_.is_public:
            access = 'pub'
        else:
            access = 'pub(crate)'

        code('#[derive(Debug)]')
        with CodeBlock(code, '{} struct {}'.format(access, class_.name)):
            # unmanaged pointer
            code('{} : *mut {},'.format(self.self_ptr_name, self.PtrEnumName))
            for pair in distincted_props.values():
                prop_ = pair[1]
                if prop_.has_getter and prop_.has_setter:
                    code('{}: Option<{}>,'.format(camelcase_to_underscore(prop_.name), self.__get_rs_type__(prop_.type_, is_property=True)))
        
        if class_.cache_mode == CacheMode.ThreadSafeCache:
            code('''
unsafe impl Send for {0} {{ }}
unsafe impl Sync for {0} {{ }}
    '''.format(class_.name))

        code('''
impl Has{1} for {0} {{
    fn {2}(&mut self) -> *mut {1} {{
        self.{2}.clone()
    }}
}}
'''.format(class_.name, self.PtrEnumName, self.self_ptr_name))

        if class_ in self.baseClasses:
            inherits = ': std::fmt::Debug + Has{}'.format(self.PtrEnumName)
            # not empty
            if base_classes:
                inherits = inherits + ' + ' + ' + '.join(map(lambda x: x.name + 'Trait', base_classes))

            with CodeBlock(code, 'pub trait {} {}'.format(get_base_trait_name(class_), inherits)):
                for func_ in [pair[1] for pair in distincted_funcs.values() if (len(pair[1].targets) == 0) or ('rust' in pair[1].targets) and (not pair[1] in base_funcs)]:
                    if not func_.is_static:
                        code(self.__generate_func_brief__(class_, func_))
                        code(self.__managed_func_declare__(class_, func_) + ';')

                for prop_ in [pair[1] for pair in distincted_props.values() if (not pair[1] in base_props)]:
                    type_name = self.__get_rs_type__(prop_.type_, is_property=True)
                    type_name_return = self.__get_rs_type__(prop_.type_, is_return=True)
                    field_name = camelcase_to_underscore(prop_.name)

                    if prop_.has_getter:
                        # Markdown comment
                        if prop_.brief != None:
                            code('/// {}'.format(prop_.brief.descs[self.lang]))
                        code('fn get_{}(&mut self) -> {};'.format(field_name, type_name_return))

                    if prop_.has_setter:
                        # Markdown comment
                        if prop_.brief != None:
                            code('/// {}'.format(prop_.brief.descs[self.lang]))
                        code('fn base_set_{}(&mut self, value : {});'.format(field_name, type_name))

            base_classes.append(class_)

        for base_class in base_classes:
            with CodeBlock(code, 'impl {} for {}'.format(get_base_trait_name(base_class), class_.name)):
                for func_ in [f for f in base_class.funcs if len(f.targets) == 0 or 'rust' in f.targets]:
                    if not func_.is_static:
                        code(self.__generate__managed_func__(base_class, func_, add_accessor=False))

                for prop_ in base_class.properties:
                    code(self.__generate__managed_property_(base_class, prop_, is_trait=True))

        with CodeBlock(code, 'impl {}'.format(class_.name)):
            # unmanaged constructor
            ret_type = 'Self'
            if class_.cache_mode == CacheMode.Cache:
                ret_type = 'Rc<RefCell<Self>>'
            elif class_.cache_mode == CacheMode.ThreadSafeCache:
                ret_type = 'Arc<Mutex<Self>>'
            
            with CodeBlock(code, 'fn cbg_create_raw({} : *mut {}) -> Option<{}>'.format(self.self_ptr_name, self.PtrEnumName, ret_type), True):
                code('if {} == NULLPTR {{ return None; }}'.format(self.self_ptr_name))

                code('Some(')
                if class_.cache_mode == CacheMode.Cache:
                    code('Rc::new(RefCell::new(')
                elif class_.cache_mode == CacheMode.ThreadSafeCache:
                    code('Arc::new(Mutex::new(')
                
                with CodeBlock(code, class_.name):
                    code('{},'.format(self.self_ptr_name))
                    for pair in distincted_props.values():
                        prop_ = pair[1]
                        if prop_.has_getter and prop_.has_setter:
                            code('{} : None,'.format(camelcase_to_underscore(prop_.name)))
                
                if is_cached(class_):
                    code('))')
                code(')')

            body = ''
            if class_.cache_mode == CacheMode.Cache:
                body = '''
fn try_get_from_cache({0} : *mut {1}) -> Option<Rc<RefCell<Self>>> {{
    thread_local! {{
        static {2}_CACHE: RefCell<HashMap<{1}Storage, rc::Weak<RefCell<{3}>>>> = RefCell::new(HashMap::new());
    }}
    {2}_CACHE.with(|hash_map| {{
        let mut hash_map = hash_map.borrow_mut();
        let storage = {1}Storage({0});
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
'''.format(self.self_ptr_name, self.PtrEnumName, class_.name.upper(), class_.name)

            elif class_.cache_mode == CacheMode.ThreadSafeCache:
                body = '''
fn try_get_from_cache({0} : *mut {1}) -> Option<Arc<Mutex<Self>>> {{
    lazy_static! {{
        static ref {2}_CACHE: RwLock<HashMap<{1}Storage, sync::Weak<Mutex<{3}>>>> = RwLock::new(HashMap::new());
    }}
    let mut hash_map = {2}_CACHE.write().unwrap();
    let storage = {1}Storage({0});
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
'''.format(self.self_ptr_name, self.PtrEnumName, class_.name.upper(), class_.name)

            lines = body.split('\n')
            for line in lines:
                code(line)

            if class_ in self.baseClasses:
                for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'rust' in f.targets]:
                    if func_.is_static:
                        code(self.__generate__managed_func__(class_, func_))

                # setter
                for pair in distincted_props.values():
                    code(self.__generate__manaded_property_setter__(pair[0], pair[1]))

            else:
                for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'rust' in f.targets]:
                    if not (func_.name in base_funcs):
                        code(self.__generate__managed_func__(class_, func_))

                for pair in base_props.values():
                    code(self.__generate__manaded_property_setter__(pair[0], pair[1]))

                for prop_ in class_.properties:
                    if not (prop_.name in base_props):
                        code(self.__generate__manaded_property_getter__(class_, prop_))
                        code(self.__generate__manaded_property_setter__(class_, prop_))



        code('')

        # destructor
        with CodeBlock(code, 'impl Drop for {}'.format(class_.name)):
            with CodeBlock(code, 'fn drop(&mut self)'):
                # with CodeBlock(code, 'if !self.{}.is_null()'.format(self.self_ptr_name)):
                code('unsafe {{ {}(self.{}) }};'.format(__get_c_release_func_name__(class_), self.self_ptr_name))
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

        # declare use
        code('#![allow(dead_code)]')
        code('#[allow(unused_imports)]')
        code('use std::ffi::c_void;')
        code('use std::os::raw::*;')
        code('')
        code('const NULLPTR: *mut RawPtr = 0 as *mut RawPtr;')

        code('''
fn decode_string(source: *const u16) -> String {
    unsafe {
        let len = (0..).take_while(|&i| *source.offset(i) != 0).count();
        let slice = std::slice::from_raw_parts(source, len);
        String::from_utf16_lossy(slice)
    }
}

fn encode_string(s: &str) -> Vec<u16> {
    let mut v: Vec<u16> = s.encode_utf16().collect();
    v.push(0);
    v
}
''')

        # for cache
        code('''
use std::rc::{{self, Rc}};
use std::cell::RefCell;
use std::sync::{{self, Arc, RwLock, Mutex}};
use std::collections::HashMap;

pub enum {0} {{ }}

pub trait Has{0} {{
    fn {1}(&mut self) -> *mut {0};
}}

#[derive(Debug, PartialEq, Eq, Hash)]
struct {0}Storage(*mut {0});

unsafe impl Send for {0}Storage {{ }}
unsafe impl Sync for {0}Storage {{ }}
'''.format(self.PtrEnumName, self.self_ptr_name))

        # enum group
        for enum_ in self.define.enums:
            if len(enum_.values) > 0:
                code(self.__generate_enum__(enum_))

        code(self.__generate_extern__(self.define.classes))

        for class_ in self.define.classes:
            if class_.base_class != None:
                self.baseClasses.add(class_.base_class)
        
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
            with open(self.output_path, mode='w') as f:
                f.write(str(code))