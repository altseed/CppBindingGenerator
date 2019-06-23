cmake_minimum_required(VERSION 3.8)

enable_language(CSharp)

file(GLOB files *.cs) 

add_executable(CSharpCaller
  ${files}
)

target_link_libraries(CSharpCaller CSharpLib)
target_compile_options(CSharpCaller PRIVATE "/langversion:6")

