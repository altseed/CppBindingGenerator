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

#[link(name = "cplusplus")]
extern "C" {
    fn cbg_ClassCppD_Constructor_0() -> *mut ();
    
    fn cbg_ClassCppD_FuncReturnClass(self_ptr: *mut ()) -> *mut ();
    
    fn cbg_ClassCppD_Release(self_ptr: *mut ()) -> ();
    
}

#[derive(Debug)]
pub struct ClassCppD {
    self_ptr : *mut (),
}

impl HasRawPtr for ClassCppD {
    fn self_ptr(&mut self) -> *mut () {
        self.self_ptr.clone()
    }
}

impl ClassCppD {
    fn cbg_create_raw(self_ptr : *mut ()) -> Option<Self> {
        if self_ptr == NULLPTR { return None; }
        Some(
            ClassCppD {
                self_ptr,
            }
        )
    }
    
    
    
    pub fn new<>() -> Option<ClassCppD> {
        Self::cbg_create_raw(unsafe{ cbg_ClassCppD_Constructor_0() })
    }
    
    
    pub fn func_return_class<>(&mut self) -> Option<Rc<RefCell<cbg_rust_debug::prelude::ClassB>>> {
        let ret = unsafe { cbg_ClassCppD_FuncReturnClass(self.self_ptr) };
        { let ret = cbg_rust_debug::prelude::ClassB::__try_get_from_cache(ret)?; Some(ret) }
    }
    
}

impl Drop for ClassCppD {
    fn drop(&mut self) {
        unsafe { cbg_ClassCppD_Release(self.self_ptr) };
    }
}

