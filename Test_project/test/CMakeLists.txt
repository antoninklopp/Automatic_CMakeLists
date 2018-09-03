#This CMake was automatically generated
#You can find this project on git : 

#Minimum version of CMake
cmake_minimum_required(VERSION 3.9) 

include_directories(${PROJECT_SOURCE_DIR}/src)

#EXECUTABLES

add_executable(test_exec test_exec.cpp)

# LINKING LIBRARIES 

target_link_libraries(test_exec lib2 lib1)
