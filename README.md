# Automatic_CMakeLists
Simple script to generate an automatic CMakeLists for your CMake projects in C++

# How to use the script
Put the script in your project folder.  
Your project folder should be organized like this :  
- project folder  
  + src
  + test
  + automated_CMake_Lists.py

Launch the script. It should create a CMakeLists.txt in each folder.  
Than, use CMake as usual.

# Adding information to CMakeLists

If you are using other dependencies than the one in your project you ca put a
requirement.txt in the project folder to add some text in the global CmakeLists.txt  

You should do this if you are using openCV or OpenGL for exemple.

# Questions, improvements?

Raise an issue or a pull requests if you have any problem. 
