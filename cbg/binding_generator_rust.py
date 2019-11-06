from typing import List
import ctypes

from .cpp_binding_generator import BindingGenerator, Define, Class, Struct, Enum, Code, Property, Function, EnumValue, __get_c_func_name__
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

    c = ''
    for x in list(value):
        if x.isalnum() and x.isupper() and (beforeCharacter != '_'):
            if result:
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
        self.structModName = 'structs'
        self.structsReplaceMap = {}

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
            if is_return:
                if type_.do_cache:
                    return 'Arc<Mutex<{}>>'.format(type_.name)
                return type_.name
            else:
                return '&mut ' + type_.name

        if type_ in self.define.structs:
            return self.structsReplaceMap.get(type_, type_.name)

        if type_ in self.define.enums:
            return type_.name

        if type_ is None:
            return '()'

        print('Type: {}'.format(type_.name))
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
            return '{}::{}'.format(self.structModName, type_.name)

        if type_ in self.define.enums:
            return 'c_int'

        if type_ is None:
            if is_return:
                return '()'
            
            return ''

        print('Type: {}'.format(type_.name))
        assert(False)

    def __convert_rsc_to_rs__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool:
            return name

        if type_ == ctypes.c_wchar_p:
            return 'CString::new({0}).expect("CString::new({0}) failed").as_ptr()'.format(name)

        if type_ in self.define.classes:
            return '{}.{}'.format(name, self.self_ptr_name)

        if type_ in self.define.structs:
            return '{}.into()'.format(name)

        if type_ in self.define.enums:
            return '{} as i32'.format(name)

        if type_ is None:
            return '()'

        assert(False)

    def __convert_ret__(self, type_, name: str) -> str:
        if type_ == int or type_ == float or type_ == bool:
            return name

        if type_ == ctypes.c_wchar_p:
            x = 'unsafe{{ CString::from_raw({} as *mut i8) }}'.format(name)
            return '{0}.into_string().expect("{0} failed")'.format(x)

        if type_ in self.define.classes:
            if type_.do_cache:
                return '{}::try_get_from_cache({})'.format(type_.name, name)
            else:
                return '{}::create({})'.format(type_.name, name)

        if type_ in self.define.structs:
            return 'From::from({})'.format(name)

        if type_ in self.define.enums:
            return 'unsafe {{ std::mem::transmute({}) }}'.format(name)

        assert(False)

    def __generate__unmanaged_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()
        fname = __get_c_func_name__(class_, func_)

        args = [replaceKeyword(arg.name) + ' : ' + self.__get_rsc_type__(arg.type_)
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


    def __write_managed_function_body__(self, code: Code, class_: Class, func_: Function):
        fname = __get_c_func_name__(class_, func_)
        # call a function
        args = [self.__convert_rsc_to_rs__(
                arg.type_, camelcase_to_underscore(replaceKeyword(arg.name))) for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = ["self." + self.self_ptr_name] + args

        if func_.is_constructor:
            code('Self::create(unsafe{{ {}({}) }})'.format(fname, ', '.join(args)))
        else:
            func_code = 'unsafe {{ {}({}) }}'.format(fname, ', '.join(args))
            if func_.return_value.type_ is None:
                code(func_code)
            else:
                code( 'let ret = {};'.format(func_code) )
                code(self.__convert_ret__(func_.return_value.type_, 'ret'))



    def __generate__managed_func__(self, class_: Class, func_: Function) -> Code:
        code = Code()

        args = [camelcase_to_underscore(replaceKeyword(arg.name)) + ' : ' + self.__get_rs_type__(arg.type_)
            for arg in func_.args]

        if not func_.is_static and not func_.is_constructor:
            args = [ "&mut self" ] + args

        # Markdown comment
        if func_.brief != None:
            code('/// {}'.format(func_.brief.descs[self.lang]))

            # not empty
            if func_.args:
                code('///')
                code('/// # Arguments')

            for arg in func_.args:
                code('///')
                code('/// * `{}` - {}'.format(camelcase_to_underscore(replaceKeyword(arg.name)), arg.desc.descs[self.lang]))

        # determine signature
        if func_.is_constructor:
            ret_type = "Self"
            if class_.do_cache:
                ret_type = "Arc<Mutex<Self>>"
            func_title = 'pub fn new({}) -> {}'.format(', '.join(args), ret_type)
        else:
            func_title = 'pub fn {}({}) -> {}'.format(
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
        
        type_name = self.__get_rs_type__(prop_.type_)
        type_name_return = self.__get_rs_type__(prop_.type_, is_return=True)

        field_name = camelcase_to_underscore(prop_.name)
        # with CodeBlock(code, 'public {} {}'.format(type_name, prop_.name)):
        if prop_.has_getter:
            with CodeBlock(code, 'pub fn get_{}(&mut self) -> {}'.format(field_name, type_name_return)):
                if prop_.has_setter:
                    with CodeBlock(code, 'if let Some(value) = self.{}'.format(field_name)):
                        code('return value;')
                self.__write_managed_function_body__(code, class_, prop_.getter_as_func())
        if prop_.has_setter:
            with CodeBlock(code, 'pub fn set_{}(&mut self, value : {})'.format(field_name, type_name)):
                if prop_.has_getter:
                    code('self.{} = Some(value);'.format(field_name))
                self.__write_managed_function_body__(code, class_, prop_.setter_as_func())

        return code


    def __generate_enum__(self, enum_ : Enum) -> Code:
        code = Code()

        code('#[repr(C)]')
        code('#[derive(Debug, Clone, Copy, PartialEq)]')
        with CodeBlock(code, "pub enum {}".format(enum_.name)):
            for val in enum_.values:
                line = val.name
                if val.value != None:
                    line = '{} = {}'.format(line, val.value)
                code(line + ',')

        return code


    def __generate_unmanaged_struct__(self, struct_ : Struct) -> Code:
        code = Code()

        code('#[repr(C)]')
        with CodeBlock(code, 'pub(crate) struct {}'.format(struct_.name)):
            for field_ in struct_.fields:
                code('pub(crate) {} : {},'.format(camelcase_to_underscore(field_.name), self.__get_rsc_type__(field_.type_)))
        return code

    def __generate_managed_struct__(self, struct_ : Struct) -> Code:
        code = Code()
        code('#[derive(Debug, Clone, Copy, PartialEq)]')
        with CodeBlock(code, 'pub struct {}'.format(struct_.name)):
            for field_ in struct_.fields:
                code('{} : {},'.format(camelcase_to_underscore(field_.name), self.__get_rs_type__(field_.type_, is_return=True)))
        
        unmanagedStructName = '{}::{}'.format(self.structModName, struct_.name)

        with CodeBlock(code, 'impl From<{0}> for {1}'.format(unmanagedStructName, struct_.name)):
            with CodeBlock(code, 'fn from(item: {}) -> Self'.format(unmanagedStructName)):
                with CodeBlock(code, 'Self'):
                    for field_ in struct_.fields:
                        name = camelcase_to_underscore(field_.name)
                        code('{} : {},'.format(name, self.__convert_rsc_to_rs__(field_.type_, 'item.' + name)))

        with CodeBlock(code, 'impl Into<{}> for {}'.format(unmanagedStructName, struct_.name)):
            with CodeBlock(code, 'fn into(self) -> {}'.format(unmanagedStructName)):
                with CodeBlock(code, unmanagedStructName):
                    for field_ in struct_.fields:
                        name = camelcase_to_underscore(field_.name)
                        code('{} : {},'.format(name, self.__convert_ret__(field_.type_, 'self.' + name)))

        return code


    def __generate_cache__(self, classes: List[Class]) -> Code:
        code = Code()

        ptr_storage_name = self.PtrEnumName + "Storage"
        code('''
use std::sync::{{Arc, Weak, RwLock, Mutex}};
use std::collections::HashMap;

#[derive(Debug, PartialEq, Eq, Hash)]
struct {0}(*mut {1});

unsafe impl Send for {0} {{ }}
unsafe impl Sync for {0} {{ }}
'''.format(ptr_storage_name, self.PtrEnumName))

        with CodeBlock(code, 'lazy_static!'):
            for class_ in classes:
                code('''static ref {}_CACHE: RwLock<HashMap<{}, Weak<Mutex<{}>>>> = RwLock::new(HashMap::new());'''.format(
                    class_.name.upper(), ptr_storage_name, class_.name))

        return code


    def __generate_class__(self, class_: Class) -> Code:
        code = Code()

        code('#[derive(Debug, PartialEq, Eq, Hash)]')
        with CodeBlock(code, 'pub struct {}'.format(class_.name)):
            # unmanaged pointer
            code('{} : *mut {},'.format(self.self_ptr_name, self.PtrEnumName))
            for prop_ in class_.properties:
                if prop_.has_getter and prop_.has_setter:
                    code('{} : Option<{}>,'.format(camelcase_to_underscore(prop_.name), self.__get_rs_type__(prop_.type_)))

        code('''
unsafe impl Send for {0} {{ }}
unsafe impl Sync for {0} {{ }}
'''.format(class_.name))

        with CodeBlock(code, 'impl Clone for {}'.format(class_.name)):
            with CodeBlock(code, 'fn clone(&self) -> Self'):
                with CodeBlock(code, class_.name):
                    code('{0} : self.{0},'.format(self.self_ptr_name))
                    for prop_ in class_.properties:
                        if prop_.has_getter and prop_.has_setter:
                            name = camelcase_to_underscore(prop_.name)
                            code('{} : self.{},'.format(name, name))
        code('')

        with CodeBlock(code, 'impl {}'.format(class_.name)):
            # unmanaged constructor
            ret_type = "Self"
            if class_.do_cache:
                ret_type = "Arc<Mutex<Self>>"
            
            code('#[allow(dead_code)]')
            with CodeBlock(code, 'fn create({} : *mut {}) -> {}'.format(self.self_ptr_name, self.PtrEnumName, ret_type), True):
                if class_.do_cache:
                    code('Arc::new(Mutex::new(')
                
                with CodeBlock(code, class_.name):
                    code('{},'.format(self.self_ptr_name))
                    for prop_ in class_.properties:
                        if prop_.has_getter and prop_.has_setter:
                            code('{} : None,'.format(camelcase_to_underscore(prop_.name)))
                
                if class_.do_cache:
                    code('))')

            if class_.do_cache:
                body ='''
#[allow(dead_code)]
fn try_get_from_cache({0} : *mut RawPtr) -> Arc<Mutex<Self>> {{
    let mut hash_map = {1}_CACHE.write().unwrap();
    let storage = RawPtrStorage({0});
    if let Some(x) = hash_map.get(&storage) {{
        match x.upgrade() {{
            Some(o) => {{ return o; }},
            None => {{ hash_map.remove(&storage); }},
        }}
    }}
    let o = Self::create({0});
    hash_map.insert(storage, Arc::downgrade(&o));
    o
}}
'''.format(self.self_ptr_name, class_.name.upper())

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

        # declare use
        code('#[allow(unused_imports)]')
        code('use std::os::raw::*;')
        code('#[allow(unused_imports)]')
        code('use std::ffi::CString;')
        code('')
        code('')

        # declare module
        if self.module != '':
            code('mod {} {{'.format(self.module))
            code.inc_indent()

        code('enum {} {{ }}'.format(self.PtrEnumName))
        code('')

        # enum group
        for enum_ in self.define.enums:
            code(self.__generate_enum__(enum_))
        
        for struct_ in self.define.structs:
            if struct_ not in self.structsReplaceMap:
                code(self.__generate_managed_struct__(struct_))

        # if list is not empty
        if self.define.structs:
            with CodeBlock(code, 'pub(crate) mod {}'.format(self.structModName)):
                code('#[allow(unused_imports)]')
                code('use super::*;')
                for struct_ in self.define.structs:
                    code(self.__generate_unmanaged_struct__(struct_))


        code(self.__generate_extern__(self.define.classes))

        chached_classed = list(filter(lambda x: x.do_cache, self.define.classes))

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