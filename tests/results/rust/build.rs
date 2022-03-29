use std::{env, error, fs, path::Path};

fn copy(path: &str, output: &str) -> Result<(), Box<dyn error::Error>> {
    if Path::new(path).exists() {
        fs::copy(path, output)?;
    }

    Ok(())
}

fn main() -> Result<(), Box<dyn error::Error>> {
    let profile = env::var("PROFILE")?.to_uppercase();

    let filename = if cfg!(windows) { "CoreLib.lib" } else { "libCoreLib.a" };

    copy(&format!("../Build/{}/{}", profile, filename), &format!("../../../{}", filename))?;


    println!("cargo:rustc-link-search=.");
    println!("cargo:rustc-link-lib=static=CoreLib");

    Ok(())
}
