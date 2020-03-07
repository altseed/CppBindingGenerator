extern crate cbg_rust_debug;
use cbg_rust_debug::rust::*;

// use std::sync::{Arc, Mutex};

fn main() {
    let mut a = ClassA::new();
    a.func_simple();
    a.func_arg_int(2);
    a.func_arg_float_bool_str(2.2, true, "hello");


    if ClassA::func_return_static() != 1 {
        eprintln!("ClassA::func_return_static() != 1");
    }
    a.set_enum_a(EnumA::Tiger);

    if a.get_enum_a() != EnumA::Tiger {
        eprintln!("a.get_enum_a() != EnumA::Tiger");
    }

    a.func_arg_struct(StructA { x : 1.0, y : 2.0, z : 3.0 });

    let cb = ClassB::new();
    {
        let mut cb = cb.lock().unwrap();
        cb.set_value(100.0);
        a.func_arg_class(&mut cb);
        let cc = cb.get_class_property();
        let mut cc = cc.lock().unwrap();
        let mut x = 0;
        cc.func_has_ref_arg(&mut x);
        println!("func_has_ref_arg: {:?}", &x);
    }

    let ret_bool = a.func_return_bool();
    println!("{:?}", &ret_bool);

    let ret_struct = a.func_return_struct();
    println!("{:?}", &ret_struct);

    let ret_class = a.func_return_class();
    {
        let mut ret_class = ret_class.lock().unwrap();
        ret_class.set_value(101.0);
        a.func_arg_class(&mut ret_class);
    }
    
}