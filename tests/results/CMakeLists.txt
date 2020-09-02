cmake_minimum_required(VERSION 3.15)

# make ZERO_CHECK disabled
set(CMAKE_SUPPRESS_REGENERATION true)

# solution name
project(CoreLib)

# specify project type
set(CMAKE_CONFIGURATION_TYPES Debug Release)

# specify destionation directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_BINARY_DIR}/DEBUG")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG "${CMAKE_BINARY_DIR}/DEBUG")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}/RELEASE")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}/RELEASE")

# add directories
add_subdirectory(so)
add_subdirectory(cplusplus)