# DO NOT EDIT!
# This file was automatically generated by confix
# as description for the module dummygen.bin

__this_module_here__ = Module(name = ['dummygen', 'bin'])
# require
__this_module_require_here__ = None
__this_module_require_here__ = RequireInclude(file='y.h', found_in=['bin/main.cc'])
__this_module_here__.add_require(__this_module_require_here__)

# provide (public only)
__this_module_provide_here__ = None

# checks
__this_module_check_here__ = AC_PROG_CXX()
__this_module_here__.add_check(__this_module_check_here__)

# feature macros