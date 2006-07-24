# $Id: makefile_am.py,v 1.7 2006/07/13 20:36:19 jfasch Exp $

# Copyright (C) 2004 Salomon Automation

# This library is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
# USA

import helper_automake

from libconfix.core.utils import helper, const
from libconfix.core.utils.error import Error

import os
import re
import types

class CompoundList:
    def __init__(self, unique):
        self.list_ = []
        if unique:
            self.have_ = set()
        else:
            self.have_ = None
            pass
        pass
    def add(self, member):
        if self.have_ is not None:
            if member in self.have_:
                raise Error('Duplicate addition of "'+member+'"')
            self.have_.add(member)
            pass
        self.list_.append(member)
        pass
    def list(self):
        return self.list_
    pass

class CompoundListManager:
    def __init__(self,
                 unique, # complain about duplicates?
                 extension, # e.g. SOURCES, or LIBADD, and such
                 ):
        self.compounds_ = {}
        self.unique_ = unique
        self.extension_ = extension
        pass
    def add(self, compound_name, member):
        canonic_name = helper_automake.automake_name(compound_name)
        compound_list = self.compounds_.get(canonic_name)
        if compound_list is None:
            compound_list = CompoundList(self.unique_)
            self.compounds_[canonic_name] = compound_list
            pass
        try:
            compound_list.add(member)
        except Error, e:
            raise Error('Cannot add member "'+member+'" to "'+compound_name+'_'+self.extension_+'"')
        pass
    def list(self, compound_name):
        canonic_name = helper_automake.automake_name(compound_name)
        list = self.compounds_.get(canonic_name)
        if list:
            return list.list()
        else:
            return []
        pass
    def lines(self):
        ret = []
        for compound_name, list in self.compounds_.iteritems():
            assert len(list.list()) > 0
            ret.extend(helper_automake.format_make_macro(name=compound_name+'_'+self.extension_,
                                                         values=list.list()))
            pass
        return ret
    pass

class Makefile_am:

    def __init__(self):
        # free lines to be output.

        self.lines_ = []

        # AUTOMAKE_OPTIONS.

        self.automake_options_ = []

        # SUBDIRS.

        self.subdirs_ = []

        # Rule objects.

        self.rules_ = []

        # sets of filenames that will come to rest in EXTRA_DIST,
        # MOSTLYCLEANFILES, CLEANFILES, DISTCLEANFILES, and
        # MAINTAINERCLEANFILES, respectively.

        self.extra_dist_ = []
        self.mostlycleanfiles_ = []
        self.cleanfiles_ = []
        self.distcleanfiles_ = []
        self.maintainercleanfiles_ = []

        # AM_CFLAGS, AM_CXXFLAGS, AM_LFLAGS, AM_YFLAGS. we collect
        # them in a dictionary to keep them unique. (keys are the
        # flags themselves, data is irrelevant.)

        self.am_cflags_ = []
        self.am_cxxflags_ = []
        self.am_lflags_ = []
        self.am_yflags_ = []

        # source files (_SOURCES) of compound objects (i.e. libraries
        # and executables).

        self.compound_sources_ = CompoundListManager(unique=True, extension='SOURCES')

        # _LDFLAGS specific to an executable or a library.

        self.compound_ldflags_ = CompoundListManager(unique=False, extension='LDFLAGS')

        # _LIBADD for compound objects.

        self.compound_libadd_ = CompoundListManager(unique=True, extension='LIBADD')

        # _LDADD for compound objects.

        self.compound_ldadd_ = CompoundListManager(unique=True, extension='LDADD')
        
        # AM_CPPFLAGS. includepath and commandline macros make their
        # way into AM_CPPFLAGS. we maintain them separately because
        # they have different overriding semantics.

        self.includepath_ = []
        self.have_includedir_ = {}

        self.cmdlinemacros_ = {}

        # generic way to register files (programs, libraries, etc.)
        # that will be built, and eventually installed. for example,
        # 'lib_LIBRARIES' is a list of library names that have to be
        # built (ok, we only build one library in a module, but that's
        # another story). other examples are 'bin_PROGRAMS', or
        # 'check_PROGRAMS'.

        # the structure is a dictionary, with the keys being the
        # variables (such as 'lib_LIBRARIES'), and the data being
        # dictionaries that have as keys the filenames that the
        # variable holds. sounds complicated, see the
        # add_dir_primary() method for more.

        self.dir_primary_ = {}

        # different scheme here. in the future all methods
        # (define_directory() etc) will only act as a factory for
        # lines which are added explicitly *by the user* (this is so
        # that the user can wrap them into automake conditionals of
        # his choice, for example).

        # symbolicname -> dirname
        self.defined_directories_ = {}

        # TESTS_ENVIRONMENT. a dictionary (string->string) that
        # contains the environment for test programs.

        self.tests_environment_ = {}

        # BUILT_SOURCES. list of files that must be built before
        # everything else is built.

        self.built_sources_ = []

        # hook-targets to be made after the local (module) thing is
        # over. see the "all-local:" and "clean-local:" hook target
        # documentation in the automake manual.

        self.all_local_ = []
        self.clean_local_ = []
        self.install_data_local_ = []

        pass

    def add_line(self, line): self.lines_.append(line)

    def add_lines(self, lines): self.lines_.extend(lines)

    
    def automake_options(self): return self.automake_options_
    def add_automake_options(self, option): self.automake_options_.append(option)

    def subdirs(self): return self.subdirs_
    def add_subdir(self, subdir): self.subdirs_.append(subdir)

    def rules(self): return self.rules_
    def add_rule(self, rule): self.rules_.append(rule)

    def extra_dist(self): return self.extra_dist_
    def add_extra_dist(self, name): self.extra_dist_.append(name)

    def add_mostlycleanfiles(self, name): self.mostlycleanfiles_.append(name)

    def add_cleanfiles(self, name): self.cleanfiles_.append(name)

    def add_distcleanfiles(self, name): self.distcleanfiles_.append(name)

    def maintainercleanfiles(self): return self.maintainercleanfiles_
    def add_maintainercleanfiles(self, name): self.maintainercleanfiles_.append(name)

    def add_am_cflags(self, f): self.am_cflags_.append(f)

    def add_am_cxxflags(self, f): self.am_cxxflags_.append(f)

    def add_am_lflags(self, f): self.am_lflags_.append(f)

    def add_am_yflags(self, f): self.am_yflags_.append(f)

    def compound_sources(self, compound_name):
        return self.compound_sources_.list(compound_name)
    def add_compound_sources(self, compound_name, source):
        self.compound_sources_.add(compound_name, source)
        pass

    def compound_ldflags(self, compound_name):
        return self.compound_ldflags_.list(compound_name)
    def add_compound_ldflags(self, compound_name, flag):
        self.compound_ldflags_.add(compound_name, flag)
        pass

    def compound_libadd(self, compound_name):
        return self.compound_libadd_.list(compound_name)
    def add_compound_libadd(self, compound_name, lib):
        self.compound_libadd_.add(compound_name, lib)
        pass

    def compound_ldadd(self, compound_name):
        return self.compound_ldadd_.list(compound_name)
    def add_compound_ldadd(self, compound_name, lib):
        self.compound_ldadd_.add(compound_name, lib)
        pass

    def add_includepath(self, d):

        """ Interface for L{libconfix.buildable.Buildable} objects. Add an include path to
        the module's C{AM_CPPFLAGS}. The include path is not added
        immediately, but it is rather collected and kept small/unique
        until it makes its way into C{AM_CPPFLAGS}.

        If you add an include directory to the search list twice, only the first
        occurrence takes effect. In fact, if we passed all paths on to the
        output (the compile command line, finally), the command line could
        become quite large, although it would be correct. To make the command
        line shorter, we apply some checks to make the search directories appear
        on the command line only once, namely the first time that they appear.

        Note that generally the include path is composed of autoconf
        substitutions, such as
        "E{@}some_include_dir_of_some_sortE{@}", and it is not the
        responsibility of this class to take care that the '-I' flag
        is present in the final output. Rather, the added string is
        completely opaque, and it is the responsibility of the adder
        to ensure that it is present.

        @type d: string

        @param d: A whitespace-delimited list of directories to add to
        the include path.

        """

        dirs = d.split()
        for dir in dirs:
            if not self.have_includedir_.has_key(dir):
                self.includepath_.append(dir)
                self.have_includedir_[dir] = 1

    def add_cmdlinemacro(self, m, value=None):

        if self.cmdlinemacros_.has_key(m):
            if self.cmdlinemacros_[m] != value:
                raise Error("Conflicting definitions of macro "+m+": "+\
                            str(self.cmdlinemacros_[m])+" and "+str(value))
        self.cmdlinemacros_[m] = value
        pass

    def define_directory(self, symbolicname, dirname):
        assert len(dirname)
        if self.defined_directories_.has_key(symbolicname):
            assert self.defined_directories_[symbolicname] == dirname
            return []
        self.defined_directories_[symbolicname] = dirname
        return helper_automake.format_dir(name=symbolicname+'dir', value=dirname)

    def set_dir_dirname(self, dir, dirname):
        debug.warn(self.dir_+': Makefile_am.set_dir_dirname() is deprecated; use Makefile_am.define_directory() instead')
        self.add_lines(self.define_directory(symbolicname=dir, dirname=dirname))
        pass

    def add_dir_primary(self, dir, primary, filename):

        # insane sanity checks

        assert dir.find('_')<0, "add_dir_primary(): dir cannot contain '_'"
        assert primary.find('_')<0, "add_dir_primary(): primary cannot contain '_'"

        # compose variable

        key = '_'.join([dir, primary])

        # create variable if not yet defined

        if not self.dir_primary_.has_key(key):
            self.dir_primary_[key] = []
            pass

        if filename in self.dir_primary_[key]:
            raise Error('Duplicate addition of "'+filename+' to "'+key+'"')
        self.dir_primary_[key].append(filename)
        pass

    def dir_primary(self, dir, primary):

        # insane sanity checks

        assert dir.find('_')<0, "dir_primary(): dir cannot contain '_'"
        assert primary.find('_')<0, "dir_primary(): primary cannot contain '_'"

        # compose variable

        key = '_'.join([dir, primary])

        if not self.dir_primary_.has_key(key):
            return []

        return self.dir_primary_[key]

    def add_library(self, libname):
        self.add_dir_primary('lib', 'LIBRARIES', libname)
        pass
        
    def ltlibraries(self): return self.dir_primary('lib', 'LTLIBRARIES')        
    def add_ltlibrary(self, libname):
        self.add_dir_primary('lib', 'LTLIBRARIES', libname)
        pass

    def bin_programs(self): return self.dir_primary('bin', 'PROGRAMS')
    def add_bin_program(self, progname):
        self.add_dir_primary('bin', 'PROGRAMS', progname)
        pass

    def add_bin_script(self, scriptname):
        self.add_dir_primary('bin', 'SCRIPTS', scriptname)
        pass

    def add_check_program(self, progname):
        self.add_dir_primary('check', 'PROGRAMS', progname)
        pass

    def add_check_script(self, scriptname):
        self.add_dir_primary('check', 'SCRIPTS', scriptname)
        pass

    def add_noinst_program(self, progname):
        self.add_dir_primary('noinst', 'PROGRAMS', progname)
        pass

    def add_noinst_script(self, scriptname):
        self.add_dir_primary('noinst', 'SCRIPTS', scriptname)
        pass

    def add_tests_environment(self, key, value):
        assert type(key) is types.StringType
        assert type(value) is types.StringType
        self.tests_environment_[key] = value
        pass

    def add_built_sources(self, filename):
        self.built_sources_.append(filename)
        pass

    def add_all_local(self, hook):
        self.all_local_.append(hook)
        pass

    def add_clean_local(self, hook):
        self.clean_local_.append(hook)
        pass

    def add_install_data_local(self, hook):
        self.install_data_local_.append(hook)
        pass

    def lines(self):
        lines = ['# DO NOT EDIT! This file was automatically generated',
                 '# by Confix version '+const.CONFIX_VERSION,
                 '']

        # AUTOMAKE_OPTIONS

        if len(self.automake_options_):
            lines.extend(helper_automake.format_list(
                name='AUTOMAKE_OPTIONS',
                values=self.automake_options_))
            pass

        # SUBDIRS

        lines.extend(helper_automake.format_make_macro(name='SUBDIRS', values=self.subdirs_))

        # Rules

        for r in self.rules_:
            lines.extend(r.lines())
            pass

        # EXTRA_DIST, MOSTLYCLEANFILES, CLEANFILES, DISTCLEANFILES,
        # and MAINTAINERCLEANFILES

        if len(self.extra_dist_):
            lines.extend(helper_automake.format_make_macro(
                name='EXTRA_DIST',
                values=self.extra_dist_))
            pass
        if len(self.mostlycleanfiles_):
            lines.extend(helper_automake.format_make_macro(
                name='MOSTLYCLEANFILES',
                values=self.mostlycleanfiles_))
            pass
        if len(self.cleanfiles_):
            lines.extend(helper_automake.format_make_macro(
                name='CLEANFILES',
                values=self.cleanfiles_))
            pass
        if len(self.distcleanfiles_):
            lines.extend(helper_automake.format_make_macro(
                name='DISTCLEANFILES',
                values=self.distcleanfiles_))
            pass
        if len(self.maintainercleanfiles_):
            lines.extend(helper_automake.format_make_macro(
                name='MAINTAINERCLEANFILES',
                values=self.maintainercleanfiles_))
            pass
        lines.append('')

        # AM_{C,CXX,L,Y}FLAGS, straightforwardly.

        if len(self.am_cflags_):
            lines.extend(helper_automake.format_make_macro(
                name='AM_CFLAGS',
                values=self.am_cflags_))
            pass
        if len(self.am_cxxflags_):
            lines.extend(helper_automake.format_make_macro(
                name='AM_CXXFLAGS',
                values=self.am_cxxflags_))
            pass
        if len(self.am_lflags_):
            lines.extend(helper_automake.format_make_macro(
                name='AM_LFLAGS',
                values=self.am_lflags_))
            pass
        if len(self.am_yflags_):
            lines.extend(helper_automake.format_make_macro(
                name='AM_YFLAGS',
                values=self.am_yflags_))
            pass

        # AM_CPPFLAGS. it is supposed to contain include paths and
        # macros.

        am_cppflags = self.includepath_[:]

        for m in self.cmdlinemacros_.keys():
            macro = '-D' + m
            if self.cmdlinemacros_[m] is not None:
                macro = macro + '=' + self.cmdlinemacros_[m]
            am_cppflags.append(macro)
            pass

        if len(am_cppflags):
            lines.extend(helper_automake.format_make_macro(
                name='AM_CPPFLAGS',
                values=am_cppflags))
            pass
 
        # primaries

        for dp in self.dir_primary_.keys():
            assert len(self.dir_primary_[dp])
            lines.extend(helper_automake.format_list(
                name=dp,
                values=self.dir_primary_[dp]))
            pass

        # compound-sources and such
        lines.extend(self.compound_sources_.lines())
        lines.extend(self.compound_ldflags_.lines())
        lines.extend(self.compound_libadd_.lines())
        lines.extend(self.compound_ldadd_.lines())

        # register automatic tests and set their environment

        tests = self.dir_primary('check', 'PROGRAMS') + \
                self.dir_primary('check', 'SCRIPTS')
        if len(tests):
            lines.extend(helper_automake.format_make_macro(
                name='TESTS',
                values=tests))
            if len(self.tests_environment_):
                lines.extend(helper_automake.format_make_macro(
                    name='TESTS_ENVIRONMENT',
                    values=[k+'='+self.tests_environment_[k] \
                            for k in self.tests_environment_.keys()]))
                pass
            pass

        # BUILT_SOURCES

        if len(self.built_sources_):
            lines.append('')
            lines.extend(helper_automake.format_make_macro(
                name='BUILT_SOURCES',
                values=self.built_sources_))

        # the registered local-hooks.

        if len(self.all_local_):
            lines.extend(helper_automake.format_rule(targets=['all-local'],
                                                     prerequisites=self.all_local_,
                                                     commands=[]))
        if len(self.clean_local_):
            lines.extend(helper_automake.format_rule(targets=['clean-local'],
                                                     prerequisites=self.clean_local_,
                                                     commands=[]))
            
        if len(self.install_data_local_):
            lines.extend(helper_automake.format_rule(targets=['install-data-local'],
                                                     prerequisites=self.install_data_local_,
                                                     commands=[]))

        # code directly contributed by my files.

        lines.append('')
        lines.extend(self.lines_)

        return lines

    pass
