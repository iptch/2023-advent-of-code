cmake_minimum_required(VERSION 3.26)
project(2023-advent-of-code)
set(CMAKE_C_STANDARD 17)

add_subdirectory(aoc_utils)

############################################################
# Add subdirectories for each day
############################################################
add_subdirectory(src/day_1)