set(CMAKE_EXECUTABLE_SUFFIX .exe)
add_executable(bb4.exe bb4.cpp )
set_target_properties(bb4.exe PROPERTIES SUFFIX "")

# installing executables and libraries
install(TARGETS bb4.exe
    RUNTIME DESTINATION ${CMAKE_CURRENT_SOURCE_DIR} )

# Add a test for this example
message(STATUS "    Add example batch #4") 

# Test run in working directory AFTER install of bb1.exe executable
add_test(NAME Example4BasicBatch
	COMMAND ${CMAKE_INSTALL_PREFIX}/bin/nomad param.txt 
	WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR} )
