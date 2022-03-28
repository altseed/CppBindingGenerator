#[macro_use]
extern crate lazy_static;

extern crate cbg_rust_debug;

pub mod auto_generated_core_bindings;

pub mod prelude {
    pub use super::auto_generated_core_bindings::*;
}