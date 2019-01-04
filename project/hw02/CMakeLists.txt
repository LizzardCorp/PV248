cmake_minimum_required(VERSION 3.6)
project(karel)

# Configuration

#   C++ standard version
set(CMAKE_CXX_STANDARD 14)
#   disable C++ non-standard extensions
set(CMAKE_CXX_EXTENSIONS OFF)

#   compilation flags
if (CMAKE_CXX_COMPILER_ID MATCHES Clang OR ${CMAKE_CXX_COMPILER_ID} STREQUAL GNU)
  # using regular Clang or AppleClang or GCC
  set(CMAKE_CXX_FLAGS "-pedantic -Wall -Wextra -g -Og -Wold-style-cast")
elseif (${CMAKE_CXX_COMPILER_ID} STREQUAL MSVC)
  # using Visual Studio C++
  set(CMAKE_CXX_FLAGS "/permissive- /W4 /EHsc")
  add_definitions("-D_CRT_SECURE_NO_WARNINGS")
endif()

#--------------------------------------------------------------------

# Search for library files
file(GLOB LIBHEADERS "*.hpp")
file(GLOB LIBSOURCES "*.cpp")

# Exclude test and CLI filenames
list(FILTER LIBHEADERS EXCLUDE REGEX "^(.*/)?(catch[.]hpp|test-.+[.]hpp)$")
list(FILTER LIBSOURCES EXCLUDE REGEX "^(.*/)?(main[.]cpp|errors[.]cpp|test-.+[.]cpp)$")

# Search for test files
file(GLOB TESTHEADERS test-*.hpp)
file(GLOB TESTSOURCES test-*.cpp)

# CLI should be implemented in main.cpp
set(CLIHEADERS)
set(CLISOURCES main.cpp)

# Complain implementation
set(ERRHEADERS errors.hpp)
set(ERRSOURCES errors.cpp)

# Some IDEs require the following variables
set(HEADERS ${LIBHEADERS} ${TESTHEADERS} ${CLIHEADERS} ${ERRHEADERS})
set(SOURCES ${LIBSOURCES} ${TESTSOURCES} ${CLISOURCES} ${ERRSOURCES})

#==  Targets  =================================================================

#--  Robot library  -----------------------------------------------------------

if(NOT LIBSOURCES)
    message(FATAL_ERROR "There are no source files to build Robot Library!")
endif()

add_library(robot STATIC ${LIBSOURCES})

#--  Playground executable  ---------------------------------------------------

add_executable(robot-cli ${CLISOURCES} ${ERRSOURCES})
target_link_libraries(robot-cli robot)

#--  Tests  -------------------------------------------------------------------

add_executable(robot-test ${TESTSOURCES} ${ERRSOURCES})
target_link_libraries(robot-test robot)

# Turn on exceptions in Complain
target_compile_definitions(robot-test PRIVATE -DCOMPLAIN_EXCEPTIONS=1)
