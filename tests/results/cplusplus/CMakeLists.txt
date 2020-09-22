cmake_minimum_required(VERSION 3.8)

enable_language(CXX)

file(GLOB files *.h *.cpp) 

add_executable(CBGTest ${files})

add_dependencies(CBGTest CoreLib)

target_compile_features(CBGTest PUBLIC cxx_std_17)

if(UNIX AND NOT APPLE)
    target_link_libraries(CBGTest PRIVATE dl)
endif()

if(UNIX)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address")
endif()