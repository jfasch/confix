# $Id: const.py,v 1.3 2006/07/18 10:43:15 jfasch Exp $

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

# Confix package version

CONFIX_VERSION = '1.5.2'

# the default name of interface files

MAKEFILE_PY = 'Makefile.py'

# the name of our auxiliary files directory

AUXDIR = 'confix-admin'

# the name of the include directory that mimics the include directory
# structure before the files are installed in $(includedir). (this
# directory is located in $(top_builddir).)

LOCAL_INCLUDE_DIR = 'confix_include'

# name of the per-directory file which contains the list of
# automatically generated sources (the pseudo hand-written generated
# files)

PSEUDO_HANDWRITTEN_LIST_FILENAME = '.confix-pseudo-handwritten'

# is this an advanced confix user ?

ARG_ADVANCED = 'ADVANCED'

# the configuration files to read. default [ ~/.confix ].

ARG_CONFIGFILES = 'CONFIGFILES'

# the selected configuration profile name. defaults to 'default'.

ARG_PROFILE = 'PROFILE'

# 'prefix' of the package. a term coined by autoconf. this is where
# the package gets installed to (--configure action), *and* where the
# repository is by default.

ARG_PREFIX = 'PREFIX'

# package root directory. used both when instrumenting a package, as
# well as when calling the configure script.

ARG_PACKAGEROOT = 'PACKAGEROOT'

# name and version of the package to instrument. name defaults to the basename
# of ARG_PACKAGEROOT ; version defaults to 0.0.0.

ARG_PACKAGENAME = 'PACKAGENAME'
ARG_PACKAGEVERSION = 'PACKAGEVERSION'

# tracing and debugging.

ARG_TRACE = 'TRACE'
ARG_DEBUG = 'DEBUG'

# list of paths to "repository" directories

ARG_REPOSITORY = 'REPOSITORY'

# blah jjj document that

ARG_READONLY_PREFIXES = 'READONLY_PREFIXES'

# the directory where the packages are compiled. each package has its
# own subdirectory there.

ARG_BUILDROOT = 'BUILDROOT'

# compile directory for the current package.

ARG_BUILDDIR = 'BUILDDIR'

# an object of class ConfigConfix, used by Confix itself.

ARG_CONFIXPARAMS = 'CONFIXPARAMS'

# an object of class ConfigConfigure, used when calling configure.

ARG_CONFIGUREPARAMS = 'CONFIGUREPARAMS'

# an object of class ConfigMake, used when calling make.

ARG_MAKEPARAMS = 'MAKEPARAMS'
ARG_TARGETS = 'TARGETS'

# this one is (not anymore) settable from outside. it is historically
# provided as a parameter, nevertheless.

ARG_M4INCDIR = 'M4INCDIR'

# flag (0 or 1) that decides whether to generate output files that use
# libtool.

ARG_USELIBTOOL = 'USELIBTOOL'

ARG_USE_BULK_INSTALL = 'USE_BULK_INSTALL'

ARG_USE_KDE_HACK = 'USE_KDE_HACK'

ARG_PRINT_TIMINGS = 'PRINT_TIMINGS'

ARG_MESSAGE_PREFIX = ''

# the verbosity, which controls the amount of diagnostic information.

ARG_VERBOSITY = 'VERBOSITY'

# dictionary keys used in the config file

CFG_PROF_PREFIX = 'PREFIX'

CFG_PROF_BUILDROOT = 'BUILDROOT'

CFG_PROF_USE_LIBTOOL = 'USE_LIBTOOL'

CFG_PROF_USE_BULK_INSTALL = 'USE_BULK_INSTALL'

CFG_PROF_USE_KDE_HACK = 'USE_KDE_HACK'

CFG_PROF_PRINT_TIMINGS = 'PRINT_TIMINGS'

CFG_PROF_MESSAGE_PREFIX = 'MESSAGE_PREFIX'

CFG_PROF_ADVANCED = 'ADVANCED'

CFG_PROF_CONFIX = 'CONFIX'

CFG_PROF_CONFIGURE = 'CONFIGURE'

CFG_PROF_MAKE = 'MAKE'

CFG_PROF_CONFIX_REPOSITORY = 'REPOSITORY'

CFG_PROF_CONFIX_READONLY_PREFIXES = 'READONLY_PREFIXES'

CFG_PROF_CONFIX_GLOBAL_REQUIRES = 'GLOBAL_REQUIRES'

CFG_PROF_CONFIX_BUILDABLECREATORS = 'BUILDABLECREATORS'

CFG_PROF_CONFIX_BUILDABLECLUSTERERS = 'BUILDABLECLUSTERERS'

CFG_PROF_EXT_ENV = 'ENV'

CFG_PROF_EXT_ARGS = 'ARGS'

