cmake_minimum_required(VERSION 3.8)

enable_language(CXX)

file(GLOB files *.h *.cpp)

add_library(CoreLib_Shared SHARED ${files})
add_library(CoreLib_Static STATIC ${files})

target_compile_features(CoreLib_Shared PUBLIC cxx_std_17)
target_compile_features(CoreLib_Static PUBLIC cxx_std_17)

set_target_properties(CoreLib_Shared CoreLib_Static PROPERTIES OUTPUT_NAME CoreLib)

if(UNIX)
    set (CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -fsanitize=address")
    set (CMAKE_ARCHIVE_LINKER_FLAGS "${CMAKE_ARCHIVE_LINKER_FLAGS} -fsanitize=address")
endif()
