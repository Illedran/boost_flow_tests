cmake_minimum_required(VERSION 3.5)
project(boost_flow_tests)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp)
add_executable(boost_flow_tests ${SOURCE_FILES})