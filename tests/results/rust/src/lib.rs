#[macro_use]
extern crate lazy_static;

pub mod auto_generated_core_bindings;

#[repr(C)]
#[derive(Debug, Clone)]
pub struct ReplaceStruct<T> {
    pub x : T,
    pub y : T,
}

pub mod structs {
    #[repr(C)]
    #[derive(Debug, Clone)]
    pub struct StructA {
        pub x : f32,
        pub y : f32,
        pub z : f32,
    }
}

pub mod prelude {
    pub use super::auto_generated_core_bindings::*;
}