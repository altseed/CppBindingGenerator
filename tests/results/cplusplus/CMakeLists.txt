cmake_minimum_required(VERSION 3.8)

enable_language(CXX)

file(GLOB files *.h *.cpp)

add_library(cplusplus_Shared SHARED ${files})
add_library(cplusplus_Static STATIC ${files})

target_compile_features(cplusplus_Shared PUBLIC cxx_std_17)
target_compile_features(cplusplus_Static PUBLIC cxx_std_17)

add_dependencies(cplusplus_Shared CoreLib_Shared)
add_dependencies(cplusplus_Static CoreLib_Static)

set_target_properties(cplusplus_Shared cplusplus_Static PROPERTIES OUTPUT_NAME cplusplus)

if(UNIX AND NOT APPLE)
    target_link_libraries(cplusplus_Shared PRIVATE dl)
    target_link_libraries(cplusplus_Static PRIVATE dl)
endif()

if(UNIX)
    set (CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -fsanitize=address")
    set (CMAKE_ARCHIVE_LINKER_FLAGS "${CMAKE_ARCHIVE_LINKER_FLAGS} -fsanitize=address")
endif()
