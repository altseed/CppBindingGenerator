cmake_minimum_required(VERSION 3.8)

enable_language(CXX)

file(GLOB files *.cpp) 

add_library(Common
  SHARED
  ${files}
)
