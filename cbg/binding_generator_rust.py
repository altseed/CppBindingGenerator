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
            return ptr + 'c_void'

        if type_ == ctypes.c_wchar_p:
            if is_return or is_property:
                return 'String'
            return '&str'

        if type_ in self.define.classes:
            if is_return:
                if type_.cache_mode == CacheMode.Cache:
                    return 'Option<Rc<RefCell<{}>>>'.format(type_.name)
                elif type_.cache_mode == CacheMode.ThreadSafeCache:
                    return 'Option<Arc<Mutex<{}>>>'.format(type_.name)
                else:
                    return type_.name
            elif is_property:
                if type_.cache_mode == CacheMode.Cache:
                    return 'Rc<RefCell<{}>>'.format(type_.name)
                elif type_.cache_mode == CacheMode.ThreadSafeCache:
                    return 'Arc<Mutex<{}>>'.format(type_.name)
                else:
                    return type_.name
            else:
                return '&mut ' + type_.name

        if type_ in self.define.structs:
            return self.structsReplaceMap.get(type_, type_.alias)

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
            return ptr + 'c_void'

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
            return self.PtrEnumName

        if type_ in self.define.classes:
            return '*mut {}'.format(self.PtrEnumName)

        if type_ in self.define.structs:
            return '{}::{}'.format(self.structModName, type_.alias)

        if type_ in self.define.enums:
            return 'c_int'

        if type_ is None:
            if is_return:
                return '()'
            
            return ''

        print('Type: {}'.format(type_))
        assert(False)

    def __convert_rsc_to_rs__(self, type_, name: str, is_property = False, called_by: ArgCalledBy = None) -> str:
        if type_ == int or type_ == float or type_ == bool or type_ == ctypes.c_byte or type_ == ctypes.c_void_p:
            if called_by == ArgCalledBy.Out or called_by == ArgCalledBy.Ref:
                return  '{} as {}'.format(name, self.__get_rsc_type__(type_, called_by=called_by))
            else:
                return name

        if type_ == ctypes.c_wchar_p:
            return 'encode_string(&{}).as_ptr()'.format(name)

        if type_ in self.define.classes:
            if is_property:
                if type_.cache_mode == CacheMode.Cache:
                    return '{}.borrow_mut().{}'.format(name, self.self_ptr_name)
                elif type_.cache_mode == CacheMode.ThreadSafeCache:
                    return '{}.lock().expect("Failed to get lock of {}").{}'.format(name, type_.name, self.self_ptr_name)
            
            return '{}.{}'.format(name, self.self_ptr_name)

        if type_ in self.define.structs:
            return '{}.into()'.format(name)

        if type_ in self.define.enums:
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
                return '{}::try_get_from_cache({})'.format(type_.name, name)
            else:
                return '{}::cbg_create_raw({})'.format(type_.name, name)

        if type_ in self.define.structs:
            return '{}.into()'.format(name)

        if type_ in self.define.enums:
            return 'unsafe {{ std::mem::transmute({}) }}'.format(name)

        print('Type: {}'.format(type_))
        assert(False)

    def __generate__unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [replaceKeyword(arg.name) + ' : ' + self.__get_rsc_type__(arg.type_, called_by=arg.called_by)
            for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = ['{} : *mut {}'.format(self.self_ptr_name, self.PtrEnumName)] + args
            
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

        code('#[allow(dead_code)]')
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



    def __generate__managed_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()

        args = [camelcase_to_underscore(replaceKeyword(arg.name)) + ' : ' + self.__get_rs_type__(arg.type_, is_return=False, is_property=False, called_by=arg.called_by)
            for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = [ "&mut self" ] + args

        # Markdown comment
        if func_.brief != None:
            code('/// {}'.format(func_.brief.descs[self.lang]))

            # not empty
            if func_.args:
                code('/// # Arguments')

            for arg in func_.args:
                if arg.brief != None:
                    code('/// * `{}` - {}'.format(camelcase_to_underscore(replaceKeyword(arg.name)), arg.brief.descs[self.lang]))

        # access signature
        access = ''

        if func_.is_public:
            access = 'pub'
        else:
            access = 'pub(crate)'

        if func_.is_constructor:
            func_title = '{} fn new({}) -> {}'.format(access, ', '.join(args), self.__get_rs_type__(class_, is_return=True))
        else:
            func_title = '{} fn {}({}) -> {}'.format(
                access,
                camelcase_to_underscore(func_.name),
                ', '.join(args),
                self.__get_rs_type__(func_.return_value.type_, is_return=True))

        # function body
        with CodeBlock(code, func_title):
            self.__write_managed_function_body__(code, class_, func_)

        return code

    def __generate__managed_property_(self, class_: Class, prop_:Property) -> Code:
        code = Code()

        # cannot generate property with no getter and no setter
        if not prop_.has_getter and not prop_.has_setter:
            return code
        
        # Markdown comment
        if prop_.brief != None:
            code('/// {}'.format(prop_.brief.descs[self.lang]))
        
        type_name = self.__get_rs_type__(prop_.type_, is_property=True)
        type_name_return = self.__get_rs_type__(prop_.type_, is_return=True)

        field_name = camelcase_to_underscore(prop_.name)

        access = 'pub'
        # if prop_.is_public:
        #     access = 'pub'
        # else:
        #     access = 'pub(crate)'
        
        if prop_.has_getter:
            with CodeBlock(code, '{} fn get_{}(&mut self) -> {}'.format(access, field_name, type_name_return)):
                if prop_.has_setter:
                    if prop_.type_ in self.define.classes:
                        code('if let Some(value) = self.{0}.clone() {{ return Some(value) }}'.format(field_name))
                    else:
                        code('if let Some(value) = self.{0}.clone() {{ return value; }}'.format(field_name))
                self.__write_managed_function_body__(code, class_, prop_.getter_as_func())
        if prop_.has_setter:
            with CodeBlock(code, '{} fn set_{}(&mut self, value : {})'.format(access, field_name, type_name)):
                if prop_.has_getter:
                    code('self.{} = Some(value.clone());'.format(field_name))
                self.__write_managed_function_body__(code, class_, prop_.setter_as_func(), is_property=True)

        return code


    def __generate_enum__(self, enum_ : Enum) -> Code:
        code = Code()

        access = 'pub'

        code('#[repr(C)]')
        code('#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]')
        with CodeBlock(code, "{} enum {}".format(access, enum_.name)):
            for val in enum_.values:
                line = val.name
                if val.value != None:
                    line = '{} = {}'.format(line, val.value)
                code(line + ',')

        return code


    # def __generate_unmanaged_struct__(self, struct_ : Struct) -> Code:
    #     code = Code()

    #     code('#[repr(C)]')
    #     with CodeBlock(code, 'pub struct {}'.format(struct_.alias)):
    #         for field_ in struct_.fields:
    #             code('pub(crate) {} : {},'.format(camelcase_to_underscore(field_.name), self.__get_rsc_type__(field_.type_)))
    #     return code

    # def __generate_managed_struct__(self, struct_ : Struct) -> Code:
    #     code = Code()
    #     code('#[derive(Debug, Clone, Copy, PartialEq, Default)]')
    #     with CodeBlock(code, 'pub struct {}'.format(struct_.alias)):
    #         for field_ in struct_.fields:
    #             code('pub {} : {},'.format(camelcase_to_underscore(field_.name), self.__get_rs_type__(field_.type_, is_return=True, is_property=True)))
        
    #     unmanagedStructName = '{}::{}'.format(self.structModName, struct_.alias)

    #     with CodeBlock(code, 'impl From<{0}> for {1}'.format(unmanagedStructName, struct_.alias)):
    #         with CodeBlock(code, 'fn from(item: {}) -> Self'.format(unmanagedStructName)):
    #             with CodeBlock(code, 'Self'):
    #                 for field_ in struct_.fields:
    #                     name = camelcase_to_underscore(field_.name)
    #                     code('{} : {},'.format(name, self.__convert_rsc_to_rs__(field_.type_, 'item.' + name)))

    #     with CodeBlock(code, 'impl Into<{}> for {}'.format(unmanagedStructName, struct_.alias)):
    #         with CodeBlock(code, 'fn into(self) -> {}'.format(unmanagedStructName)):
    #             with CodeBlock(code, unmanagedStructName):
    #                 for field_ in struct_.fields:
    #                     name = camelcase_to_underscore(field_.name)
    #                     code('{} : {},'.format(name, self.__convert_ret__(field_.type_, 'self.' + name)))

    #     return code


    def __generate_cache__(self, classes: List[Class]) -> Code:
        code = Code()

        ptr_storage_name = self.PtrEnumName + "Storage"
        code('''
use std::rc::{{self, Rc}};
use std::cell::RefCell;
use std::sync::{{self, Arc, RwLock, Mutex}};
use std::collections::HashMap;

#[derive(Debug, PartialEq, Eq, Hash)]
struct {0}(*mut {1});

unsafe impl Send for {0} {{ }}
unsafe impl Sync for {0} {{ }}
'''.format(ptr_storage_name, self.PtrEnumName))

        return code


    def __generate_class__(self, class_: Class) -> Code:
        code = Code()

        access = ''
        if class_.is_public:
            access = 'pub'
        else:
            access = 'pub(crate)'

        code('#[derive(Debug)]')
        with CodeBlock(code, '{} struct {}'.format(access, class_.name)):
            # unmanaged pointer
            code('{} : *mut {},'.format(self.self_ptr_name, self.PtrEnumName))
            for prop_ in class_.properties:
                if prop_.has_getter and prop_.has_setter:
                    code('{} : Option<{}>,'.format(camelcase_to_underscore(prop_.name), self.__get_rs_type__(prop_.type_, is_property=True)))
        
        if class_.cache_mode == CacheMode.ThreadSafeCache:
            code('''
unsafe impl Send for {0} {{ }}
unsafe impl Sync for {0} {{ }}
    '''.format(class_.name))

        # with CodeBlock(code, 'impl Clone for {}'.format(class_.name)):
        #     with CodeBlock(code, 'fn clone(&self) -> Self'):
        #         with CodeBlock(code, class_.name):
        #             code('{0} : self.{0},'.format(self.self_ptr_name))
        #             for prop_ in class_.properties:
        #                 if prop_.has_getter and prop_.has_setter:
        #                     name = camelcase_to_underscore(prop_.name)
                            
        #                     code('{} : self.{},'.format(name, name))
        code('')

        with CodeBlock(code, 'impl {}'.format(class_.name)):
            # unmanaged constructor
            ret_type = self.__get_rs_type__(class_, is_return=True)
            
            code('#[allow(dead_code)]')
            with CodeBlock(code, 'fn cbg_create_raw({} : *mut {}) -> {}'.format(self.self_ptr_name, self.PtrEnumName, ret_type), True):
                code('if {} == NULLPTR {{ return None; }}'.format(self.self_ptr_name))

                if class_.cache_mode == CacheMode.Cache:
                    code('Some(Rc::new(RefCell::new(')
                elif class_.cache_mode == CacheMode.ThreadSafeCache:
                    code('Some(Arc::new(Mutex::new(')
                
                with CodeBlock(code, class_.name):
                    code('{},'.format(self.self_ptr_name))
                    for prop_ in class_.properties:
                        if prop_.has_getter and prop_.has_setter:
                            code('{} : None,'.format(camelcase_to_underscore(prop_.name)))
                
                if is_cached(class_):
                    code(')))')

            body = ''
            if class_.cache_mode == CacheMode.Cache:
                body = '''
#[allow(dead_code)]
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
#[allow(dead_code)]
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

            # managed functions
            for func_ in [f for f in class_.funcs if len(f.targets) == 0 or 'rust' in f.targets]:
                code(self.__generate__managed_func__(class_, func_))

            for prop_ in class_.properties:
                code(self.__generate__managed_property_(class_, prop_))

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

        # declare use
        code('#[allow(unused_imports)]')
        code('use std::os::raw::*;')
        code('use std::ffi::{ c_void };')
        code('')
        code('const NULLPTR : *mut RawPtr = 0 as *mut RawPtr;')

        body = '''
#[allow(dead_code)]
fn decode_string(source: *const u16) -> String {
    unsafe {
        let len = (0..).take_while(|&i| *source.offset(i) != 0).count();
        let slice = std::slice::from_raw_parts(source, len);
        String::from_utf16_lossy(slice)
    }
}

#[allow(dead_code)]
fn encode_string(s: &str) -> Vec<u16> {
    let mut v: Vec<u16> = s.encode_utf16().collect();
    v.push(0);
    v
}
'''

        for line in body.split('\n'):
            code(line)


        # declare module
        if self.module != '':
            code('mod {} {{'.format(self.module))
            code.inc_indent()

        code('enum {} {{ }}'.format(self.PtrEnumName))
        code('')

        # enum group
        for enum_ in self.define.enums:
            if len(enum_.values) > 0:
                code(self.__generate_enum__(enum_))
        
        # for struct_ in self.define.structs:
        #     if struct_ not in self.structsReplaceMap:
        #         code(self.__generate_managed_struct__(struct_))

        # # if list is not empty
        # if self.define.structs:
        #     with CodeBlock(code, 'pub mod {}'.format(self.structModName)):
        #         code('#[allow(unused_imports)]')
        #         code('use super::*;')
        #         for struct_ in self.define.structs:
        #             code(self.__generate_unmanaged_struct__(struct_))


        code(self.__generate_extern__(self.define.classes))

        chached_classed = list(filter(is_cached, self.define.classes))

        # Not Empty
        if chached_classed:
            code(self.__generate_cache__(chached_classed))
        
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