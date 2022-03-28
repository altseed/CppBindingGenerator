// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
//
//   このファイルは自動生成されました。
//   このファイルへの変更は消失することがあります。
//
//   THIS FILE IS AUTO GENERATED.
//   YOUR COMMITMENT ON THIS FILE WILL BE WIPED. 
//
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

#![allow(dead_code)]
#![allow(unused_imports)]
use std::ffi::c_void;
use std::os::raw::*;

use std::rc::{self, Rc};
use std::cell::RefCell;
use std::sync::{self, Arc, RwLock, Mutex};
use std::collections::HashMap;

const NULLPTR: *mut () = 0 as *mut ();

pub trait HasRawPtr {
    fn self_ptr(&mut self) -> *mut ();
}

#[derive(Debug, PartialEq, Eq, Hash)]
struct RawPtrStorage(*mut ());

unsafe impl Send for RawPtrStorage { }
unsafe impl Sync for RawPtrStorage { }

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

#[repr(C)]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Animal {
    Mosue,
    Cow,
    Tiger = 3,
}

#[link(name = "CoreLib")]
extern {
    fn cbg_ClassAlias_Cpp_Constructor_0() -> *mut ();
    
    fn cbg_ClassAlias_Cpp_FuncSimple(self_ptr: *mut ()) -> *mut ();
    
    fn cbg_ClassAlias_Cpp_Release(self_ptr: *mut ()) -> ();
    
    fn cbg_ClassA_Constructor_0() -> *mut ();
    
    fn cbg_ClassA_FuncSimple(self_ptr: *mut ()) -> ();
    
    fn cbg_ClassA_FuncArgInt(self_ptr: *mut (), value: c_int) -> ();
    
    fn cbg_ClassA_FuncArgFloatBoolStr(self_ptr: *mut (), value1: c_float, value2: bool, value3: *const u16) -> ();
    
    fn cbg_ClassA_FuncArgStruct(self_ptr: *mut (), value1: *const crate::structs::StructA) -> ();
    
    fn cbg_ClassA_FuncArgClass(self_ptr: *mut (), value1: *mut ()) -> ();
    
    fn cbg_ClassA_FuncReturnInt(self_ptr: *mut ()) -> c_int;
    
    fn cbg_ClassA_FuncReturnBool(self_ptr: *mut ()) -> bool;
    
    fn cbg_ClassA_FuncReturnFloat(self_ptr: *mut ()) -> c_float;
    
    fn cbg_ClassA_FuncReturnStruct(self_ptr: *mut ()) -> crate::structs::StructA;
    
    fn cbg_ClassA_FuncReturnClass(self_ptr: *mut ()) -> *mut ();
    
    fn cbg_ClassA_FuncReturnString(self_ptr: *mut ()) -> *const u16;
    
    fn cbg_ClassA_FuncReturnStatic() -> c_int;
    
    fn cbg_ClassA_GetBReference(self_ptr: *mut ()) -> *mut ();
    
    
    fn cbg_ClassA_GetEnumA(self_ptr: *mut ()) -> c_int;
    fn cbg_ClassA_SetEnumA(self_ptr: *mut (), value: c_int) -> ();
    
    
    fn cbg_ClassA_Release(self_ptr: *mut ()) -> ();
    
    fn cbg_ClassB_Constructor_0() -> *mut ();
    
    fn cbg_ClassB_SetValue(self_ptr: *mut (), value: c_float) -> ();
    
    fn cbg_ClassB_SetEnum(self_ptr: *mut (), enumValue: c_int) -> ();
    
    fn cbg_ClassB_GetEnum(self_ptr: *mut (), id: c_int) -> c_int;
    
    fn cbg_ClassB_GetMyProperty(self_ptr: *mut ()) -> c_int;
    fn cbg_ClassB_SetMyProperty(self_ptr: *mut (), value: c_int) -> ();
    
    
    fn cbg_ClassB_GetClassProperty(self_ptr: *mut ()) -> *mut ();
    fn cbg_ClassB_SetClassProperty(self_ptr: *mut (), value: *mut ()) -> ();
    
    
    
    
    fn cbg_ClassB_SetMyBool(self_ptr: *mut (), value: bool) -> ();
    
    
    fn cbg_ClassB_Release(self_ptr: *mut ()) -> ();
    
    fn cbg_ClassC_Constructor_0() -> *mut ();
    
    fn cbg_ClassC_SetValue(self_ptr: *mut (), value: c_float) -> ();
    
    fn cbg_ClassC_SetEnum(self_ptr: *mut (), enumValue: c_int) -> ();
    
    fn cbg_ClassC_GetEnum(self_ptr: *mut (), id: c_int) -> c_int;
    
    fn cbg_ClassC_FuncHasRefArg(self_ptr: *mut (), intRef: *const c_int) -> ();
    
    fn cbg_ClassC_GetMyProperty(self_ptr: *mut ()) -> c_int;
    fn cbg_ClassC_SetMyProperty(self_ptr: *mut (), value: c_int) -> ();
    
    
    fn cbg_ClassC_GetStringProperty(self_ptr: *mut ()) -> *const u16;
    fn cbg_ClassC_SetStringProperty(self_ptr: *mut (), value: *const u16) -> ();
    
    
    
    
    fn cbg_ClassC_SetMyBool(self_ptr: *mut (), value: bool) -> ();
    
    
    fn cbg_ClassC_Release(self_ptr: *mut ()) -> ();
    
    fn cbg_BaseClass_Constructor_0() -> *mut ();
    
    fn cbg_BaseClass_GetBaseClassField(self_ptr: *mut ()) -> c_int;
    
    fn cbg_BaseClass_SetBaseClassField(self_ptr: *mut (), value: c_int) -> ();
    
    fn cbg_BaseClass_Release(self_ptr: *mut ()) -> ();
    
    fn cbg_DerivedClass_Constructor_0() -> *mut ();
    
    fn cbg_DerivedClass_GetBaseClassFieldFromDerivedClass(self_ptr: *mut ()) -> c_int;
    
    fn cbg_DerivedClass_Release(self_ptr: *mut ()) -> ();
    
}

#[derive(Debug)]
pub struct ClassAlias_CS {
    self_ptr : *mut (),
}

impl HasRawPtr for ClassAlias_CS {
    fn self_ptr(&mut self) -> *mut () {
        self.self_ptr.clone()
    }
}

impl ClassAlias_CS {
    fn cbg_create_raw(self_ptr : *mut ()) -> Option<Self> {
        if self_ptr == NULLPTR { return None; }
        Some(
            ClassAlias_CS {
                self_ptr,
            }
        )
    }
    
    
    
    pub fn new<>() -> Option<ClassAlias_CS> {
        Self::cbg_create_raw(unsafe{ cbg_ClassAlias_Cpp_Constructor_0() })
    }
    
    
    pub fn func_simple<>(&mut self) -> Option<ClassAlias_CS> {
        let ret = unsafe { cbg_ClassAlias_Cpp_FuncSimple(self.self_ptr) };
        ClassAlias_CS::cbg_create_raw(ret)
    }
    
}

impl Drop for ClassAlias_CS {
    fn drop(&mut self) {
        unsafe { cbg_ClassAlias_Cpp_Release(self.self_ptr) };
    }
}

#[derive(Debug)]
pub struct ClassA {
    self_ptr : *mut (),
}

impl HasRawPtr for ClassA {
    fn self_ptr(&mut self) -> *mut () {
        self.self_ptr.clone()
    }
}

impl ClassA {
    fn cbg_create_raw(self_ptr : *mut ()) -> Option<Self> {
        if self_ptr == NULLPTR { return None; }
        Some(
            ClassA {
                self_ptr,
            }
        )
    }
    
    
    
    pub fn new<>() -> Option<ClassA> {
        Self::cbg_create_raw(unsafe{ cbg_ClassA_Constructor_0() })
    }
    
    
    pub fn func_simple<>(&mut self) -> () {
        unsafe { cbg_ClassA_FuncSimple(self.self_ptr) }
    }
    
    
    pub fn func_arg_int<>(&mut self, value : i32) -> () {
        unsafe { cbg_ClassA_FuncArgInt(self.self_ptr, value) }
    }
    
    
    pub fn func_arg_float_bool_str<>(&mut self, value1 : f32, value2 : bool, value3 : &str) -> () {
        unsafe { cbg_ClassA_FuncArgFloatBoolStr(self.self_ptr, value1, value2, encode_string(&value3).as_ptr()) }
    }
    
    /// Processes a structA.
    
    pub fn func_arg_struct<>(&mut self, value1 : &crate::structs::StructA) -> () {
        unsafe { cbg_ClassA_FuncArgStruct(self.self_ptr, value1 as *const crate::structs::StructA) }
    }
    
    
    pub fn func_arg_class<>(&mut self, value1 : &mut ClassB) -> () {
        unsafe { cbg_ClassA_FuncArgClass(self.self_ptr, value1.self_ptr) }
    }
    
    /// Returns some integer.
    
    pub fn func_return_int<>(&mut self) -> i32 {
        let ret = unsafe { cbg_ClassA_FuncReturnInt(self.self_ptr) };
        ret
    }
    
    
    pub fn func_return_bool<>(&mut self) -> bool {
        let ret = unsafe { cbg_ClassA_FuncReturnBool(self.self_ptr) };
        ret
    }
    
    
    pub fn func_return_float<>(&mut self) -> f32 {
        let ret = unsafe { cbg_ClassA_FuncReturnFloat(self.self_ptr) };
        ret
    }
    
    
    pub fn func_return_struct<>(&mut self) -> crate::structs::StructA {
        let ret = unsafe { cbg_ClassA_FuncReturnStruct(self.self_ptr) };
        ret
    }
    
    
    pub fn func_return_class<>(&mut self) -> Option<Rc<RefCell<ClassB>>> {
        let ret = unsafe { cbg_ClassA_FuncReturnClass(self.self_ptr) };
        { let ret = ClassB::__try_get_from_cache(ret)?; Some(ret) }
    }
    
    
    pub fn func_return_string<>(&mut self) -> String {
        let ret = unsafe { cbg_ClassA_FuncReturnString(self.self_ptr) };
        decode_string(ret)
    }
    
    
    pub fn func_return_static<>() -> i32 {
        let ret = unsafe { cbg_ClassA_FuncReturnStatic() };
        ret
    }
    
    pub fn get_breference(&mut self) -> Option<Rc<RefCell<ClassB>>> {
        let ret = unsafe { cbg_ClassA_GetBReference(self.self_ptr) };
        { let ret = ClassB::__try_get_from_cache(ret)?; Some(ret) }
    }
    
    
    pub fn get_enum_a(&mut self) -> Animal {
        let ret = unsafe { cbg_ClassA_GetEnumA(self.self_ptr) };
        unsafe { std::mem::transmute(ret) }
    }
    
    pub fn set_enum_a<>(&mut self, value : Animal) {
        unsafe { cbg_ClassA_SetEnumA(self.self_ptr, value as i32) }
    }
    
}

impl Drop for ClassA {
    fn drop(&mut self) {
        unsafe { cbg_ClassA_Release(self.self_ptr) };
    }
}

#[derive(Debug)]
pub struct ClassB {
    self_ptr : *mut (),
}

impl HasRawPtr for ClassB {
    fn self_ptr(&mut self) -> *mut () {
        self.self_ptr.clone()
    }
}

impl ClassB {
    fn cbg_create_raw(self_ptr : *mut ()) -> Option<Rc<RefCell<Self>>> {
        if self_ptr == NULLPTR { return None; }
        Some(
            Rc::new(RefCell::new(
                ClassB {
                    self_ptr,
                }
            ))
        )
    }
    
    
    pub fn __try_get_from_cache(self_ptr : *mut ()) -> Option<Rc<RefCell<Self>>> {
        thread_local! {
            static CLASSB_CACHE: RefCell<HashMap<RawPtrStorage, rc::Weak<RefCell<ClassB>>>> = RefCell::new(HashMap::new());
        }
        CLASSB_CACHE.with(|hash_map| {
            let mut hash_map = hash_map.borrow_mut();
            let storage = RawPtrStorage(self_ptr);
            if let Some(x) = hash_map.get(&storage) {
                match x.upgrade() {
                    Some(o) => { return Some(o); },
                    None => { hash_map.remove(&storage); },
                }
            }
            let o = Self::cbg_create_raw(self_ptr)?;
            hash_map.insert(storage, Rc::downgrade(&o));
            Some(o)
        })
    }
    
    
    pub fn new<>() -> Option<Rc<RefCell<ClassB>>> {
        Self::cbg_create_raw(unsafe{ cbg_ClassB_Constructor_0() })
    }
    
    
    pub fn set_value<>(&mut self, value : f32) -> () {
        unsafe { cbg_ClassB_SetValue(self.self_ptr, value) }
    }
    
    
    pub fn set_enum<>(&mut self, enum_value : Animal) -> () {
        unsafe { cbg_ClassB_SetEnum(self.self_ptr, enum_value as i32) }
    }
    
    
    pub fn get_enum<>(&mut self, id : i32) -> Animal {
        let ret = unsafe { cbg_ClassB_GetEnum(self.self_ptr, id) };
        unsafe { std::mem::transmute(ret) }
    }
    
    /// 
    pub fn get_my_property(&mut self) -> i32 {
        let ret = unsafe { cbg_ClassB_GetMyProperty(self.self_ptr) };
        ret
    }
    
    /// 
    pub fn set_my_property<>(&mut self, value : i32) {
        unsafe { cbg_ClassB_SetMyProperty(self.self_ptr, value) }
    }
    
    /// 
    pub fn get_class_property(&mut self) -> Option<ClassA> {
        let ret = unsafe { cbg_ClassB_GetClassProperty(self.self_ptr) };
        ClassA::cbg_create_raw(ret)
    }
    
    /// 
    pub fn set_class_property<>(&mut self, value : ClassA) {
        unsafe { cbg_ClassB_SetClassProperty(self.self_ptr, value.self_ptr) }
    }
    
    
    
    
    pub fn set_my_bool<>(&mut self, value : bool) {
        unsafe { cbg_ClassB_SetMyBool(self.self_ptr, value) }
    }
    
}

impl Drop for ClassB {
    fn drop(&mut self) {
        unsafe { cbg_ClassB_Release(self.self_ptr) };
    }
}

#[derive(Debug)]
pub struct ClassC {
    self_ptr : *mut (),
}

unsafe impl Send for ClassC { }
unsafe impl Sync for ClassC { }

impl HasRawPtr for ClassC {
    fn self_ptr(&mut self) -> *mut () {
        self.self_ptr.clone()
    }
}

impl ClassC {
    fn cbg_create_raw(self_ptr : *mut ()) -> Option<Arc<Mutex<Self>>> {
        if self_ptr == NULLPTR { return None; }
        Some(
            Arc::new(Mutex::new(
                ClassC {
                    self_ptr,
                }
            ))
        )
    }
    
    
    pub fn __try_get_from_cache(self_ptr : *mut ()) -> Option<Arc<Mutex<Self>>> {
        lazy_static! {
            static ref CLASSC_CACHE: RwLock<HashMap<RawPtrStorage, sync::Weak<Mutex<ClassC>>>> = RwLock::new(HashMap::new());
        }
        let mut hash_map = CLASSC_CACHE.write().unwrap();
        let storage = RawPtrStorage(self_ptr);
        if let Some(x) = hash_map.get(&storage) {
            match x.upgrade() {
                Some(o) => { return Some(o); },
                None => { hash_map.remove(&storage); },
            }
        }
        let o = Self::cbg_create_raw(self_ptr)?;
        hash_map.insert(storage, Arc::downgrade(&o));
        Some(o)
    }
    
    
    pub fn new<>() -> Option<Arc<Mutex<ClassC>>> {
        Self::cbg_create_raw(unsafe{ cbg_ClassC_Constructor_0() })
    }
    
    
    pub fn set_value<>(&mut self, value : f32) -> () {
        unsafe { cbg_ClassC_SetValue(self.self_ptr, value) }
    }
    
    
    pub fn set_enum<>(&mut self, enum_value : Animal) -> () {
        unsafe { cbg_ClassC_SetEnum(self.self_ptr, enum_value as i32) }
    }
    
    
    pub fn get_enum<>(&mut self, id : i32) -> Animal {
        let ret = unsafe { cbg_ClassC_GetEnum(self.self_ptr, id) };
        unsafe { std::mem::transmute(ret) }
    }
    
    
    pub fn func_has_ref_arg<>(&mut self, int_ref : &i32) -> () {
        unsafe { cbg_ClassC_FuncHasRefArg(self.self_ptr, int_ref as *const c_int) }
    }
    
    /// 
    pub fn get_my_property(&mut self) -> i32 {
        let ret = unsafe { cbg_ClassC_GetMyProperty(self.self_ptr) };
        ret
    }
    
    /// 
    pub fn set_my_property<>(&mut self, value : i32) {
        unsafe { cbg_ClassC_SetMyProperty(self.self_ptr, value) }
    }
    
    /// 
    pub fn get_string_property(&mut self) -> String {
        let ret = unsafe { cbg_ClassC_GetStringProperty(self.self_ptr) };
        decode_string(ret)
    }
    
    /// 
    pub fn set_string_property<>(&mut self, value : String) {
        unsafe { cbg_ClassC_SetStringProperty(self.self_ptr, encode_string(&value).as_ptr()) }
    }
    
    
    
    
    pub fn set_my_bool<>(&mut self, value : bool) {
        unsafe { cbg_ClassC_SetMyBool(self.self_ptr, value) }
    }
    
}

impl Drop for ClassC {
    fn drop(&mut self) {
        unsafe { cbg_ClassC_Release(self.self_ptr) };
    }
}

#[derive(Debug)]
pub struct BaseClass {
    self_ptr : *mut (),
}

impl HasRawPtr for BaseClass {
    fn self_ptr(&mut self) -> *mut () {
        self.self_ptr.clone()
    }
}

pub trait AsBaseClass : std::fmt::Debug + HasRawPtr {
    
    fn get_base_class_field<>(&mut self) -> i32;
    
    fn set_base_class_field<>(&mut self, value : i32) -> ();
}

impl AsBaseClass for BaseClass {
    
    fn get_base_class_field<>(&mut self) -> i32 {
        let ret = unsafe { cbg_BaseClass_GetBaseClassField(self.self_ptr) };
        ret
    }
    
    
    fn set_base_class_field<>(&mut self, value : i32) -> () {
        unsafe { cbg_BaseClass_SetBaseClassField(self.self_ptr, value) }
    }
    
}

impl BaseClass {
    fn cbg_create_raw(self_ptr : *mut ()) -> Option<Self> {
        if self_ptr == NULLPTR { return None; }
        Some(
            BaseClass {
                self_ptr,
            }
        )
    }
    
    
    
    pub fn new<>() -> Option<BaseClass> {
        Self::cbg_create_raw(unsafe{ cbg_BaseClass_Constructor_0() })
    }
    
}

impl Drop for BaseClass {
    fn drop(&mut self) {
        unsafe { cbg_BaseClass_Release(self.self_ptr) };
    }
}

#[derive(Debug)]
pub struct DerivedClass {
    self_ptr : *mut (),
}

impl HasRawPtr for DerivedClass {
    fn self_ptr(&mut self) -> *mut () {
        self.self_ptr.clone()
    }
}

impl AsBaseClass for DerivedClass {
    
    fn get_base_class_field<>(&mut self) -> i32 {
        let ret = unsafe { cbg_BaseClass_GetBaseClassField(self.self_ptr) };
        ret
    }
    
    
    fn set_base_class_field<>(&mut self, value : i32) -> () {
        unsafe { cbg_BaseClass_SetBaseClassField(self.self_ptr, value) }
    }
    
}

impl DerivedClass {
    fn cbg_create_raw(self_ptr : *mut ()) -> Option<Self> {
        if self_ptr == NULLPTR { return None; }
        Some(
            DerivedClass {
                self_ptr,
            }
        )
    }
    
    
    
    pub fn new<>() -> Option<DerivedClass> {
        Self::cbg_create_raw(unsafe{ cbg_DerivedClass_Constructor_0() })
    }
    
    
    pub fn get_base_class_field_from_derived_class<>(&mut self) -> i32 {
        let ret = unsafe { cbg_DerivedClass_GetBaseClassFieldFromDerivedClass(self.self_ptr) };
        ret
    }
    
}

impl Drop for DerivedClass {
    fn drop(&mut self) {
        unsafe { cbg_DerivedClass_Release(self.self_ptr) };
    }
}

