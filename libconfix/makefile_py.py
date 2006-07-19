# $Id: makefile_py.py,v 1.17 2006/06/21 11:06:49 jfasch Exp $

# Copyright (C) 2002 Salomon Automation
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from core.error import Error, SystemError
from fileprops import FileProperties
from modbuildprops import BuildableModuleProperties
from buildable_h import BuildableHeader
from core.require import Require
from plugins.c.dependency import Require_CInclude
from core.require_symbol import Require_Symbol
from provide_h import Provide_CInclude
from core.provide_symbol import Provide_Symbol
import helper_configure_in
import const
import core.debug

import os
import sys

class Makefile_py:

    def __init__(self, dir, package, module, silent=0):

        self.dir_ = dir

        self.module_ = module
        self.package_ = package

        self.context_ = {
            'PACKAGE_': self.package_,
            'MODULE_': self.module_,
            'SILENT_': silent,
            'IGNORE_AS_SUBMODULE_': 0,

            # some constants we export and document

            'AC_BOILERPLATE': helper_configure_in.ORDER_BOILERPLATE,
            'AC_OPTIONS': helper_configure_in.ORDER_OPTIONS,
            'AC_PROGRAMS': helper_configure_in.ORDER_PROGRAMS,
            'AC_LIBRARIES': helper_configure_in.ORDER_LIBRARIES,
            'AC_HEADERS': helper_configure_in.ORDER_HEADERS,
            'AC_TYPEDEFS_AND_STRUCTURES': helper_configure_in.ORDER_TYPEDEFS_AND_STRUCTURES,
            'AC_FUNCTIONS': helper_configure_in.ORDER_FUNCTIONS,
            'AC_OUTPUT': helper_configure_in.ORDER_OUTPUT,

            'REQUIRED': Require.URGENCY_ERROR,
            'WELCOMED': Require.URGENCY_WARN,
            'BLUNZN': Require.URGENCY_DONTCARE,
            }

        # compile my functions

        exec _funcs in self.context_

    def ignore_as_submodule(self):
        return self.context_['IGNORE_AS_SUBMODULE_']

    def execute(self):

        if not os.path.isfile(os.path.join(self.dir_, const.MAKEFILE_PY)):
            return

        cwd = os.getcwd()
        try:
            os.chdir(self.dir_)
            execfile(const.MAKEFILE_PY, self.context_)
        except Exception, e:
            os.chdir(cwd)
            raise Error('An error occured while executing '+\
                        os.path.join(self.dir_, const.MAKEFILE_PY),
                        [SystemError(e, sys.exc_traceback)])

        os.chdir(cwd)

_funcs = """

import os
import types

from libconfix.core.require import Require
from libconfix.buildable import Buildable
from libconfix.core.provide import Provide
from libconfix.provide_callable import Provide_Callable
from libconfix.paragraph import Paragraph
from libconfix.core.error import Error
from libconfix.fileprops import FileProperties, FilePropertiesSet
from libconfix.modbuildprops import BuildableModuleProperties
from libconfix.buildable_h import BuildableHeader
from libconfix.plugins.c.dependency import Require_CInclude
from libconfix.core.require_symbol import Require_Symbol
from libconfix.require_callable import Require_Callable
from libconfix.provide_h import Provide_CInclude
from libconfix.core.provide_symbol import Provide_Symbol
from libconfix.buildinfo import BuildInformation
from libconfix.buildinfo_common import \
    BuildInfo_Configure_in, \
    BuildInfo_ACInclude_m4, \
    BuildInfo_CIncludePath_External, \
    BuildInfo_CLibrary_External, \
    BuildInfo_CommandlineMacros, \
    BuildInfo_CFLAGS, \
    BuildInfo_CXXFLAGS
import libconfix.const

import libconfix.core.debug

def PACKAGE_NAME(name):

    global PACKAGE_
    if PACKAGE_ is None:
        raise Error('PACKAGE_NAME() is only available in the toplevel Makefile.py')
    if type(name) is not types.StringType:
        raise Error('PACKAGE_NAME(): argument must be a string')
    PACKAGE_.makefile_py_set_name(name)

def PACKAGE_VERSION(version):

    global PACKAGE_
    if PACKAGE_ is None:
        raise Error('PACKAGE_VERSION() is only available in the toplevel Makefile.py')
    if type(version) is not types.StringType:
        raise Error('PACKAGE_VERSION(): argument must be a string')
    PACKAGE_.makefile_py_set_version(version)

def NAME(name):

    if not SILENT_: libconfix.core.debug.warn('NAME() is deprecated; use PACKAGE_NAME() instead')
    PACKAGE_NAME(name)

def VERSION(version):

    if not SILENT_: libconfix.core.debug.warn('VERSION() is deprecated; use PACKAGE_VERSION() instead')
    PACKAGE_VERSION(version)

def PACKAGE():

    global PACKAGE_
    return PACKAGE_

def MODULE():

    global MODULE_
    return MODULE_

def IGNORE_AS_SUBMODULE():

    global IGNORE_AS_SUBMODULE_
    IGNORE_AS_SUBMODULE_ = 1
    pass

LOCAL = 0
def CONFIGURE_IN(
    lines,
    order,
    id=None,
    propagate_only=0,
    propagate_mode=None
    ):

    global MODULE_
    assert MODULE_ is not None

    if type(order) not in [types.IntType or types.LongType]:
        raise Error('CONFIGURE_IN(): order parameter must be an integer')

    if not propagate_only:
        MODULE_.add_configure_in(paragraph=Paragraph(lines=lines), order=order)
        pass

    if propagate_mode is None or propagate_mode != LOCAL:
        MODULE_.add_buildinfo(BuildInfo_Configure_in(lines=lines, order=order))
        pass
    pass

def ACINCLUDE_M4(
    lines,
    id=None,
    propagate_only=0):

    global MODULE_
    assert MODULE_ is not None

    if id is not None:
        libconfix.core.debug.warn(os.path.join(MODULE_.dir(), libconfix.const.MAKEFILE_PY)+": "
                             "ACINCLUDE_M4(): 'id' is deprecated and ignored")
        pass

    if not propagate_only:
        MODULE_.add_acinclude_m4(Paragraph(lines))
        pass
    MODULE_.add_buildinfo(BuildInfo_ACInclude_m4(lines=lines))

def ACINCLUDE(
    lines,
    id,
    propagate_only=0):

    global MODULE_
    assert MODULE_ is not None

    libconfix.core.debug.warn(os.path.join(MODULE_.dir(), libconfix.const.MAKEFILE_PY)+": "
                         "ACINCLUDE() is deprecated, use ACINCLUDE_M4() instead")
    ACINCLUDE_M4(lines, id, propagate_only)

def MAKEFILE_AM(
    line):
    
    global MODULE_
    assert MODULE_ is not None

    MODULE_.makefile_am().add_line(line)

def EXTRA_DIST(
    filename):

    global MODULE_
    assert MODULE_ is not None

    MODULE_.makefile_am().add_extra_dist(filename)

def PROVIDE_H(
    filematch,
    provide_mode='public'):

    global MODULE_
    assert MODULE_ is not None

    if not filematch or len(filematch)==0:
        raise Error('PROVIDE_H(): need a non-zero filematch parameter')

    if not provide_mode in ['public', 'package']:
        raise Error('PROVIDE_H(\\'' + filematch + '\\', ...): '
                    'provide_mode parameter must be one of "public", "package"')

    prov = Provide_CInclude(filematch, match=Provide_CInclude.GLOB_MATCH)

##     if provide_mode == 'public':
##         MODULE_.add_public_provide(prov)
##     elif provide_mode == 'package':
##         MODULE_.add_package_provide(prov)
##     else: assert 0

    MODULE_.add_provide(prov)

def PROVIDE(
    provide,
    provide_mode='public'):

    global MODULE_
    assert MODULE_ is not None

    if provide is None:
        raise Error('PROVIDE(): "provide" must not be None')

    if not isinstance(provide, Provide):
        raise Error('PROVIDE(): "provide" parameter must be of type "Provide"')

    if not provide_mode in ['public', 'package']:
        raise Error('PROVIDE(): '
                    'provide_mode parameter must be one of "public", "package"')
    
##     if provide_mode == 'public':
##         MODULE_.add_public_provide(provide)
##     elif provide_mode == 'package':
##         MODULE_.add_package_provide(provide)
##     else: assert 0

    MODULE_.add_provide(provide)

def PROVIDE_SYMBOL(
    symbol,
    provide_mode='public'):

    global MODULE_
    assert MODULE_ is not None

    if not symbol or len(symbol)==0:
        raise Error('PROVIDE_SYMBOL(): need a non-zero symbol parameter')

    if not provide_mode in ['public', 'package']:
        raise Error('PROVIDE_SYMBOL("' + symbol + '", ...): '
                    'provide_mode parameter must be one of "public", "package"')

    prov = Provide_Symbol(symbol)

##     if provide_mode == 'public':
##         MODULE_.add_public_provide(prov)
##     elif provide_mode == 'package':
##         MODULE_.add_package_provide(prov)
##     else: assert 0

    MODULE_.add_provide(prov)

def PROVIDE_CALLABLE(
    name,
    provide_mode='public'):

    global MODULE_
    assert MODULE_ is not None

    if not name or len(name)==0:
        raise Error('PROVIDE_CALLABLE(): need a non-zero name parameter')

    if not provide_mode in ['public', 'package']:
        raise Error('PROVIDE_CALLABLE("' + name + '", ...): '
                    'provide_mode parameter must be one of "public", "package"')

    prov = Provide_Callable(exename=name)

##     if provide_mode == 'public':
##         MODULE_.add_public_provide(prov)
##     elif provide_mode == 'package':
##         MODULE_.add_package_provide(prov)
##     else: assert 0

    MODULE_.add_provide(prov)

def REQUIRE(require): # copied to core.builder
 # copied to core.builder
    global MODULE_ # copied to core.builder
    assert MODULE_ is not None # copied to core.builder
 # copied to core.builder
    if not require: # copied to core.builder
        raise Error('REQUIRE(): parameter must not be None') # copied to core.builder
    if not isinstance(require, Require): # copied to core.builder
        raise Error('REQUIRE(): parameter must be of type Require') # copied to core.builder
 # copied to core.builder
    MODULE_.add_require(require) # copied to core.builder

def REQUIRE_H(filename, urgency=Require.URGENCY_DONTCARE):

    global MODULE_
    assert MODULE_ is not None

    if not filename or len(filename)==0:
        raise Error('REQUIRE_H(): need a non-zero filename parameter')

    if not urgency in [Require.URGENCY_DONTCARE, Require.URGENCY_WARN,
                       Require.URGENCY_ERROR]:
        raise Error('REQUIRE_H(): urgency must be one of REQUIRED, WELCOMED, BLUNZN')

    MODULE_.add_require(Require_CInclude(
        filename,
        found_in=os.path.join(MODULE_.dir(), 'Makefile.py'),
        urgency=urgency))

def REQUIRE_SYMBOL(symbol, urgency=Require.URGENCY_DONTCARE):

    global MODULE_
    assert MODULE_ is not None

    if not symbol or len(symbol)==0:
        raise Error('REQUIRE_SYMBOL(): need a non-zero symbol parameter')

    if not urgency in [Require.URGENCY_DONTCARE, Require.URGENCY_WARN,
                       Require.URGENCY_ERROR]:
        raise Error('REQUIRE_SYMBOL(): urgency must be one of REQUIRED, WELCOMED, BLUNZN')

    MODULE_.add_require(Require_Symbol(
        symbol,
        found_in=os.path.join(MODULE_.dir(), 'Makefile.py'),
        urgency=urgency))

def REQUIRE_CALLABLE(name, urgency=Require.URGENCY_DONTCARE):

    global MODULE_
    assert MODULE_ is not None

    if not name or len(symbol)==0:
        raise Error('REQUIRE_CALLABLE(): need a non-zero name parameter')

    if not urgency in [Require.URGENCY_DONTCARE, Require.URGENCY_WARN,
                       Require.URGENCY_ERROR]:
        raise Error('REQUIRE_CALLABLE(): urgency must be one of REQUIRED, WELCOMED, BLUNZN')

    MODULE_.add_require(Require_Callable(
        exename=name,
        found_in=os.path.join(MODULE_.dir(), 'Makefile.py'),
        urgency=urgency))

def FEATURE_MACRO(macroname, description):
    raise Error('FEATURE_MACRO() is no longer supported; use CONFIGURE_IN(AC_DEFINE(...)) instead.')

def EXTERNAL_LIBRARY2(

    # the former is treated like a single item in the latter
    inc='',
    incpath=[],
    
    libpath=[],
    lib='',
    cmdlinemacros={},
    cflags=[],
    cxxflags=[]
    ):

    global MODULE_
    assert MODULE_ is not None

    if not type(cxxflags) is types.ListType:
        raise Error("EXTERNAL_LIBRARY2() in module " + '.'.join(MODULE_.name()) + ": "
                    "'cxxflags' argument must be a list")
    if not type(cflags) is types.ListType:
        raise Error("EXTERNAL_LIBRARY2() in module " + '.'.join(MODULE_.name()) + ": "
                    "'cflags' argument must be a list")
    if not type(libpath) is types.ListType:
        raise Error("EXTERNAL_LIBRARY2() in module " + '.'.join(MODULE_.name()) + ": "
                    "'libpath' argument must be a list")

    MODULE_.add_buildinfo(BuildInfo_CommandlineMacros(cmdlinemacros))
    MODULE_.add_buildinfo(BuildInfo_CFLAGS(cflags))
    MODULE_.add_buildinfo(BuildInfo_CXXFLAGS(cxxflags))

    passed_incpath = []
    if len(inc):
        passed_incpath.append(inc)
    passed_incpath.extend(incpath)
    MODULE_.add_buildinfo(BuildInfo_CIncludePath_External(passed_incpath))

    MODULE_.add_buildinfo(BuildInfo_CLibrary_External(libpath, [lib]))

def BUILDINFORMATION(
    buildinfo
    ):

    global MODULE_
    assert MODULE_ is not None

    if not isinstance(buildinfo, BuildInformation):
        raise Error('BUILDINFORMATION(): "buildinfo" parameter must be of type "BuildInformation"')

    MODULE_.add_buildinfo(buildinfo)

# provide backward compatibility: BuildInformation was formerly
# (around about Sep. 2005) called Content
def CONTENT(content): BUILDINFORMATION(buildinfo=content)

def IGNORE_FILE(
    filename
    ):

    global MODULE_
    assert MODULE_ is not None

    if type(filename) is not types.StringType:
        raise Error('IGNORE_FILE(): "filename" parameter must be a string')
        
    MODULE_.add_ignore_file(filename)

def FILE_PROPERTIES(
    filename,
    properties
    ):

    global MODULE_
    assert MODULE_ is not None

    if not type(filename) is types.StringType:
        raise Error("FILE_PROPERTIES(): "
                    "'filename' parameter must be a string")
    if properties is None:
        raise Error("FILE_PROPERTIES(filename="+filename+"): "
                    "'properties' parameter cannot be None")
    if not type(properties) is types.DictionaryType:
        raise Error("FILE_PROPERTIES(filename="+filename+"): "
                    "'properties' parameter must be a dictionary")

    MODULE_.fileproperties().add(
        filename=filename,
        buildable_type=None, 
        properties=FileProperties(properties=properties))

def MODULE_PROPERTIES(
    properties
    ):

    global MODULE_
    assert MODULE_ is not None

    if properties is None:
        raise Error("MODULE_PROPERTIES(): "
                    "'properties' parameter cannot be None")
    if not type(properties) is types.DictionaryType:
        raise Error("MODULE_PROPERTIES(): "
                    "'properties' parameter must be a dictionary")

    MODULE_.buildmodprops().update(BuildableModuleProperties(properties))

def LIBNAME(name):

    global MODULE_
    assert MODULE_ is not None

    MODULE_PROPERTIES({'LIBNAME': name})

def INSTALLDIR_H(dir):

    global MODULE_
    assert MODULE_ is not None

    if type(dir) is not types.StringType:
        raise Error('INSTALLDIR_H(): parameter must be a string')

    fp = FileProperties()
    fp.set_install_path(dir)

    MODULE_.fileproperties().add(
        filename=None,
        buildable_type=BuildableHeader,
        properties=fp)

def DIR():

    global MODULE_
    assert MODULE_ is not None
    return MODULE_.dir()

def BUILDABLE(buildable):

    global MODULE_
    assert MODULE_ is not None

    if not isinstance(buildable, Buildable):
        raise Error('BUILDABLE() argument must be of type Buildable')

    MODULE_.add_buildable(buildable)

def BUILDABLECREATOR(regex, creator):

    global MODULE_
    assert MODULE_ is not None
    
    try:
        MODULE_.buildable_manager().register_creator(regex, creator)
    except Error, e:
        raise Error('Could not register buildable creator for regex "'+regex+'"', [e])

def BUILDABLECLUSTERER(clusterer):

    global MODULE_
    assert MODULE_ is not None
    
    try:
        MODULE_.buildable_manager().register_clusterer(clusterer)
    except Error, e:
        raise Error('Could not register buildable clusterer')

def TESTS_ENVIRONMENT(key, value):

    global MODULE_
    assert MODULE_ is not None

    if type(key) is not types.StringType:
        raise Error('TESTS_ENVIRONMENT(): key must be a string')
    if type(value) is not types.StringType:
        raise Error('TESTS_ENVIRONMENT(): value must be a string')

    MODULE_.makefile_am().add_tests_environment(key, value)

def _add_require_includes(reqs):

    global MODULE_
    assert MODULE_ is not None
    
    errors = []
    for r in reqs:
        if not r or len(r) == 0:
            errors.append('cannot make require object from an empty #include name')
            continue
        try:
            MODULE_.add_require(Require_CInclude(filename=r, found_in=''))
        except Error, e:
            errors.append(Error('module error', [e]))
            continue
    return errors

def _add_require_symbols(reqs):

    global MODULE_
    assert MODULE_ is not None
    
    errors = []
    for r in reqs:
        if not r or len(r) == 0:
            errors.append('cannot make require object from an empty symbol name')
            continue
        try:
            MODULE_.add_require(Require_Symbol(symbol=r, found_in=''))
        except Error, e:
            errors.append(Error('module error', [e]))
            continue
    return errors

"""
