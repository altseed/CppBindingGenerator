use std::{error};

fn main() -> Result<(), Box<dyn error::Error>> {
    if cfg!(all(windows, target_env = "msvc")) {
        println!("cargo:rustc-link-arg=/NODEFAULTLIB:msvcrtd.lib");
    }

    Ok(())
}
