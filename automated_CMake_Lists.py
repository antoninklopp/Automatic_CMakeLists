#!/usr/bin/env python3

import glob
import os

"""
This program aims to write automatically CMakes for very simple projects.
"""

WRITE_GIT = True
# If write backup is true then we will write the backup of the CMakeLists
# as CMakeLists_backup.txt
WRITE_BACKUP = False

def write_header_CMake(file_to_write):
    if WRITE_GIT:
        file_to_write.write("#This CMake was automatically generated\n")
        file_to_write.write("#You can find this project on git https://github.com/antoninklopp/Automatic_CMakeLists: \n\n")
    file_to_write.write("#Minimum version of CMake\n")
    file_to_write.write("cmake_minimum_required(VERSION 3.9) \n\n")


def write_CMakeList():
    """
    The user can put a requirement.txt in the folder, and it will be concatenated to
    the first CMakeLists, in case he want special packages like openmp or other packages
    """
    with open("CMakeLists.txt", "w") as f: # Be careful, it will overwrite other files
        write_header_CMake(f)
        f.write("#Project's name\n")
        f.write("project(Automatic)\n")

        try:
            # Write the requirements.txt file
            with open("requirements.txt") as req:
                for line in req:
                    f.write(line)
        except FileNotFoundError:
            print("requirements.txt does not exist. You can create this file",  \
            "to add content in the CMakeLists, the program will automtically concatenate it.")

        f.write("\n#SOURCES\n")
        f.write("add_subdirectory(src)\n\n")
        f.write("#TESTS\n")
        f.write("add_subdirectory(test)\n\n")


def write_CMakeList_src():
    """
    The src CMakeList will be created automatically
    It we will regroup all te cpp files as libraries
    """
    with open("src/CMakeLists.txt", "w") as f: # Be careful, it will overwrite other files
        write_header_CMake(f)
        f.write("include_directories(library)\n")

        for cpp in glob.glob("src/*.cpp"):
            name_file = cpp.split("/")[-1]
            f.write("add_library(" + name_file[:-4] + " SHARED " + name_file + ")\n")

def find_libraries(name_file, dependencies):
    """
    Find all the libraries from a file, returns all the libraries as list
    """
    with open(name_file) as f:
        for line in f:
            if '#include "' in line:
                # There we have found a private dependency from the file
                include = line.split('"')[1][:-2]
                if include not in dependencies:
                    dependencies.append(include)
                    find_libraries("src/" + include + ".h", dependencies)
            if "opencv" in line and "${OpenCV_LIBS}" not in dependencies:
                dependencies.append("${OpenCV_LIBS}")

def write_CMakeList_test():
    """
    The test CMakeList will be created autoatically.
    It will scan the source files to find which libraries are linked.
    """
    with open("test/CMakeLists.txt", "w") as f: # Be careful, it will overwrite other files
        write_header_CMake(f)

        # First we add the source directory
        f.write("include_directories(${PROJECT_SOURCE_DIR}/src)\n")

        f.write("\n#EXECUTABLES\n\n")

        # We add all the executables
        for test_file in glob.glob("test/*.cpp"):
            name_file = test_file.split("/")[-1]
            f.write("add_executable(" + name_file[:-4] + " " + name_file + ")\n")

        f.write("\n# LINKING LIBRARIES \n\n")

        # Then we try to find all the dependencies recursively in the code
        for test_file in glob.glob("test/*.cpp"):
            name_file = test_file.split("/")[-1]
            f.write("target_link_libraries(" + name_file[:-4] + " ")
            list_libraries = []
            find_libraries(test_file, list_libraries)
            f.write(" ".join(list_libraries) + ")\n")

if __name__ == "__main__":
    print("Run this script in the folder where you want to create your CMakeLists")
    print("Make a backup, this program will erase your previous CMake lists")
    print("Organize your folder as following")
    print("-your_project")
    print("-- src")
    print("-- test")
    print("We imagine that you have named you .h and your .cpp associated ", \
    "with exactly the same names")

    write_CMakeList()
    write_CMakeList_src()
    write_CMakeList_test()

