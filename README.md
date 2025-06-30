# Scons scripts to run pybind11 example on a Windows-10 computer using MS Visual Studio and msys2 (g++ and clang++)
After having had a hard time when I tried to find out how to run the pybind11 example code on my computer I finally succeeded with the help of Gemini. Therefore I want to share the code with you.

For the example, please have a look on [pybind11 / Creating bindings for a simple function in https://pybind11.readthedocs.io/en/latest/basics.html#compiling-the-test-cases](https://pybind11.readthedocs.io/en/latest/basics.html#compiling-the-test-cases)! Since I'm using [python scons](https://scons.org/) as build system for C++ I was looking for pybind11 examples but was not very successful, this means in particular that the code should run under MS Visual C++ and msys2 g++ or clang++. Regarding msys2 I found an example with Cmake, see [stackoverflow](https://stackoverflow.com/questions/78503768/use-pybind11-with-cmake-and-msys2-and-mingw) which I add for completeness. 

Finally I asked [Gemini](https://gemini.google.com) and within 2 hours had the solution for scons for all 3 cases, which I want to share with you. The Sconstruct files are

+ Sconstruct_msvc.py for MS Visual C++
+ Sconstruct_gpp.py for msys2/ucrt64/g++ and
+ Sconstruct_clang.py for msys2/ucrt64/clang++

A major stumbling block you should be aware of was that the two scons msys2 scripts created a .dll that had to be renamed manually into a .pyd file. 
