# Set the CMake minimum version
cmake_minimum_required(VERSION 3.5)

# Declare the Project version and the Language that the project is written in
project(module2 VERSION 1.0.0 LANGUAGES C CXX)

# Set the Build Type to Release
# Ideally there should be more Build Types, but for now there is only one
set(CMAKE_BUILD_TYPE "Release")

# Include the Header files  
include_directories("include/")

# Add rules to create the binary files
add_executable(problem1 src/problem1_app.cpp src/problem1.cpp)
target_link_libraries(problem1 PUBLIC  -lm )

# Add rules to create the binary file for the test
add_executable(problem1_test tests/problem1_test.cpp src/problem1.cpp)
target_link_libraries(problem1_test PUBLIC  -lm -lgtest -lpthread)

