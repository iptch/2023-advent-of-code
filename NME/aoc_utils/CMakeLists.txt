# Set the project name
project (aoc_utils)

############################################################
# Create a library
############################################################

# Add a library with the above sources
add_library(${PROJECT_NAME} src/aoc_utils.c)
add_library(utils::aoc_utils ALIAS ${PROJECT_NAME})

target_include_directories( ${PROJECT_NAME}
        PUBLIC ${PROJECT_SOURCE_DIR}/include
)