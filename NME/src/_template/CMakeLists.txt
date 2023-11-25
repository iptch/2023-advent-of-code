project(solutions)

############################################################
# Create an executable
############################################################

# Add part 1 as an executable
add_executable(part1
        part_1.c
)

# Add part 2 as an executable
add_executable(part2
        part_2.c
)


# link the aoc_utils library target with part1
target_link_libraries( part1
        PRIVATE
        utils::aoc_utils
)

# link the aoc_utils library target with part1
target_link_libraries( part2
        PRIVATE
        utils::aoc_utils
)

############################################################
# Copy input files to executable directory. Add examples at your discretion
############################################################
FILE(COPY input.txt DESTINATION "${CMAKE_CURRENT_BINARY_DIR}")