cmake_minimum_required(VERSION 3.8)

# make ZERO_CHECK disabled
set(CMAKE_SUPPRESS_REGENERATION true)

# solution name
project(Generator)

# specify project type
set(CMAKE_CONFIGURATION_TYPES Debug Release)

# specify destionation directories
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_BINARY_DIR}/DEBUG")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_DEBUG "${CMAKE_BINARY_DIR}/DEBUG")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}/RELEASE")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE "${CMAKE_BINARY_DIR}/RELEASE")

# specify C# framework
set(CMAKE_DOTNET_TARGET_FRAMEWORK_VERSION v4.6.1)
# set(CMAKE_CSharp_FLAGS "/langversion:6")

# add directories
add_subdirectory(so)
add_subdirectory(csharp)
add_subdirectory(csharp_caller)

# specify a startup project
set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT CSharpCaller)