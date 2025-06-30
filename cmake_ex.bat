REM see https://stackoverflow.com/questions/78503768/use-pybind11-with-cmake-and-msys2-and-mingw
mkdir buildmingw
cd buildmingw
cmake .. -G "MinGW Makefiles"
mingw32-make