cmake_minimum_required(VERSION 3.8)

enable_language(CXX)

file(GLOB files *.h *.cpp) 

add_library(CoreLib SHARED ${files})

target_compile_features(CoreLib PUBLIC cxx_std_17)

# if(UNIX)
#     set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address") 
# endif()