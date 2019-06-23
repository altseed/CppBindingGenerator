cmake_minimum_required(VERSION 3.8)

enable_language(CSharp)

file(GLOB files *.cs) 

add_library(CSharpLib
  SHARED
  ${files}
)

target_link_libraries(CSharpLib Common)
target_compile_options(CSharpLib PRIVATE "/langversion:6")
