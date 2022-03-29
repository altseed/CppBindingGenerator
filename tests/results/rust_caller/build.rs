use std::{env, error, fs, path::Path};

fn copy(path: &str, output: &str) -> Result<(), Box<dyn error::Error>> {
    if Path::new(path).exists() {
        fs::copy(path, output)?;
    }

    Ok(())
}

fn main() -> Result<(), Box<dyn error::Error>> {
    let flag = env::var("PROFILE")?;

    let dll_name = match env::consts::OS {
        "windows" => "CoreLib.dll",
        "macos" => "libCoreLib.dylib",
        _ => "libCoreLib.so",
    };

    copy(
        &format!("../build/{}/{}", flag, dll_name),
        &format!("../../../target/{}/{}", flag, dll_name),
    )?;
    println!("cargo:rustc-link-search=native=.");

    Ok(())
}