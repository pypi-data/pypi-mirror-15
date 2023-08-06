# author: Manuel Gunther <siebenkopf@googlemail.com>
# date:  Wed May 25 10:55:42 MDT 2016
# license: BSD-3, see LICENSE file

cmake_minimum_required(VERSION 2.8)
project(test)

# Set the module path so that "FindBob.cmake" is found
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR})

# Add the -pthread option
set(CMAKE_CXX_FLAGS "-pthread" CACHE STRING "Flags used by the compiler during release builds" FORCE)

# Find all Bob packages recursively
find_package(Bob COMPONENTS bob.io.image REQUIRED)

# Add Bob's include directories
include_directories(${Bob_INCLUDE_DIRS})
# Add Bob's library directories
link_directories(${Bob_LIBRARY_DIRS})
# Add Bob's libraries
link_libraries(${Bob_LIBRARIES} boost_system)
# Add Bob's definitions
add_definitions(${Bob_DEFINITIONS})

# create an "my_test" executable from file "test.cpp"
add_executable(my_test test.cpp)
