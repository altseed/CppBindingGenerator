#[macro_use]
extern crate lazy_static;

pub mod rust;

pub struct ReplaceStruct<T> {
    x : T,
    y : T,
}

use rust::structs;

impl From<structs::ReplaceStructA> for ReplaceStruct<f32> {
    fn from(item: structs::ReplaceStructA) -> Self {
        Self {
            x : item.x,
            y : item.y,
        }
    }
}
impl Into<structs::ReplaceStructA> for ReplaceStruct<f32> {
    fn into(self) -> structs::ReplaceStructA {
        structs::ReplaceStructA {
            x : self.x,
            y : self.y,
        }
    }
}
