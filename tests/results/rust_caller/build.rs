fn main() {
    println!("cargo:rustc-link-search=native=../../build/DEBUG/.");
    println!("cargo:rustc-link-lib=dylib=Common");
}