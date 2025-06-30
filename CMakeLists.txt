cmake_minimum_required(VERSION 4.0)
# Notre projet est étiqueté hello
project(example)

find_package(Python COMPONENTS Interpreter Development)
find_package(pybind11 CONFIG)

# pybind11 method:
pybind11_add_module(example example.cpp)