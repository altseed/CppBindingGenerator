extern crate cbg_rust_debug;
use cbg_rust_debug::{structs::*, prelude::*};

// use std::sync::{Arc, Mutex};

fn main() {
    let mut a = ClassA::new().unwrap();
    a.func_simple();
    a.func_arg_int(2);
    a.func_arg_float_bool_str(2.2, true, "hello");


    if ClassA::func_return_static() != 1 {
        eprintln!("ClassA::func_return_static() != 1");
    }
    a.set_enum_a(Animal::Tiger);

    if a.get_enum_a() != Animal::Tiger {
        eprintln!("a.get_enum_a() != Animal::Tiger");
    }

    a.func_arg_struct(&StructA { x : 1.0, y : 2.0, z : 3.0 });

    let cb = ClassB::new().unwrap();
    {
        cb.borrow_mut().set_value(100.0);
        a.func_arg_class(&mut cb.borrow_mut());
    }

    let ret_bool = a.func_return_bool();
    println!("{:?}", &ret_bool);

    let ret_struct = a.func_return_struct();
    println!("{:?}", &ret_struct);

    let cc = ClassC::new().unwrap();
    {
        let mut cc = cc.lock().unwrap();
        cc.set_enum(Animal::Cow);
    }
    
}