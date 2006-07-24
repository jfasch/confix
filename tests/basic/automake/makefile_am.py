# $Id: makefile_am.py,v 1.2 2006/07/13 20:27:24 jfasch Exp $

# Copyright (C) 2002-2006 Salomon Automation

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

from libconfix.core.automake.makefile_am import Makefile_am
from libconfix.core.utils.error import Error

import unittest, re

class MakefileAmSuite(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self)
        self.addTest(MakefileAmTest('test_standard_lists'))
        self.addTest(MakefileAmTest('test_errors'))
        self.addTest(MakefileAmTest('test_defined_install_directories'))
        pass
    pass

rex_macro = re.compile(r'^([\w_\.]+)\s*=\s(.*)$')
rex_listsep = re.compile(r'\s+')

class MakefileAmTest(unittest.TestCase):
    def test_standard_lists(self):

        mf_am = Makefile_am()

        mf_am.add_compound_sources('the_program', 'source.h')
        mf_am.add_compound_sources('the_program', 'source.c')

        mf_am.add_compound_ldflags('the_program', '-some-flag')
        mf_am.add_compound_ldflags('the_program', '-some-other-flag')

        mf_am.add_compound_libadd('libsome_ltlibrary_la', 'some_library')
        mf_am.add_compound_libadd('libsome_ltlibrary_la', 'some_other_library')

        mf_am.add_compound_ldadd('the_program', 'some_library')
        mf_am.add_compound_ldadd('the_program', 'some_other_library')

        mf_am.add_am_cflags('-some-cflag')
        mf_am.add_am_cflags('-some-other-cflag')
        mf_am.add_am_cxxflags('-some-cxxflag')
        mf_am.add_am_cxxflags('-some-other-cxxflag')
        mf_am.add_am_lflags('-some-lflag')
        mf_am.add_am_lflags('-some-other-lflag')
        mf_am.add_am_yflags('-some-yflag')
        mf_am.add_am_yflags('-some-other-yflag')

        mf_am.add_extra_dist('some-extra-dist-file')
        mf_am.add_extra_dist('some-other-extra-dist-file')
        mf_am.add_mostlycleanfiles('some-mostlycleanfile')
        mf_am.add_mostlycleanfiles('some-other-mostlycleanfile')
        mf_am.add_cleanfiles('some-cleanfile')
        mf_am.add_cleanfiles('some-other-cleanfile')
        mf_am.add_distcleanfiles('some-distcleanfile')
        mf_am.add_distcleanfiles('some-other-distcleanfile')
        mf_am.add_maintainercleanfiles('some-maintainercleanfiles')
        mf_am.add_maintainercleanfiles('some-other-maintainercleanfiles')
        
        mf_am.add_ltlibrary('libsome-ltlibrary.la')
        mf_am.add_ltlibrary('libsome-other-ltlibrary.la')
        mf_am.add_library('libsome-library.a')
        mf_am.add_library('libsome-other-library.a')
        mf_am.add_bin_program('some-program')
        mf_am.add_bin_program('some-other-program')
        mf_am.add_bin_script('some-script')
        mf_am.add_bin_script('some-other-script')
        mf_am.add_check_program('some-check-program')
        mf_am.add_check_program('some-other-check-program')
        mf_am.add_dir_primary('xxx', 'YYY', 'some-xxx-YYY-thing')
        mf_am.add_dir_primary('xxx', 'YYY', 'some-other-xxx-YYY-thing')
        mf_am.add_dir_primary('aaa', 'YYY', 'some-aaa-YYY-thing')
        mf_am.add_dir_primary('aaa', 'YYY', 'some-other-aaa-YYY-thing')

        mf_am.add_built_sources('some-built-source')
        mf_am.add_built_sources('some-other-built-source')

        ##########################
        lines = mf_am.lines()
        lines = self.collapse_continuations_(lines)

        self.failUnlessEqual(self.find_list_('the_program_SOURCES', lines),
                             ['source.h', 'source.c'])
        self.failUnlessEqual(self.find_list_('the_program_LDFLAGS', lines),
                             ['-some-flag', '-some-other-flag'])
        self.failUnlessEqual(self.find_list_('libsome_ltlibrary_la_LIBADD', lines),
                             ['some_library', 'some_other_library'])
        self.failUnlessEqual(self.find_list_('the_program_LDADD', lines),
                             ['some_library', 'some_other_library'])
        self.failUnlessEqual(self.find_list_('AM_CFLAGS', lines),
                             ['-some-cflag', '-some-other-cflag'])
        self.failUnlessEqual(self.find_list_('AM_CXXFLAGS', lines),
                             ['-some-cxxflag', '-some-other-cxxflag'])
        self.failUnlessEqual(self.find_list_('AM_LFLAGS', lines),
                             ['-some-lflag', '-some-other-lflag'])
        self.failUnlessEqual(self.find_list_('AM_YFLAGS', lines),
                             ['-some-yflag', '-some-other-yflag'])
        self.failUnlessEqual(self.find_list_('EXTRA_DIST', lines),
                             ['some-extra-dist-file', 'some-other-extra-dist-file'])
        self.failUnlessEqual(self.find_list_('MOSTLYCLEANFILES', lines),
                             ['some-mostlycleanfile', 'some-other-mostlycleanfile'])
        self.failUnlessEqual(self.find_list_('CLEANFILES', lines),
                             ['some-cleanfile', 'some-other-cleanfile'])
        self.failUnlessEqual(self.find_list_('DISTCLEANFILES', lines),
                             ['some-distcleanfile', 'some-other-distcleanfile'])
        self.failUnlessEqual(self.find_list_('MAINTAINERCLEANFILES', lines),
                             ['some-maintainercleanfiles', 'some-other-maintainercleanfiles'])
        self.failUnlessEqual(self.find_list_('lib_LTLIBRARIES', lines),
                             ['libsome-ltlibrary.la', 'libsome-other-ltlibrary.la'])
        self.failUnlessEqual(self.find_list_('lib_LIBRARIES', lines),
                             ['libsome-library.a', 'libsome-other-library.a'])
        self.failUnlessEqual(self.find_list_('bin_PROGRAMS', lines),
                             ['some-program', 'some-other-program'])
        self.failUnlessEqual(self.find_list_('bin_SCRIPTS', lines),
                             ['some-script', 'some-other-script'])
        self.failUnlessEqual(self.find_list_('check_PROGRAMS', lines),
                             ['some-check-program', 'some-other-check-program'])
        self.failUnlessEqual(self.find_list_('xxx_YYY', lines),
                             ['some-xxx-YYY-thing', 'some-other-xxx-YYY-thing'])
        self.failUnlessEqual(self.find_list_('aaa_YYY', lines),
                             ['some-aaa-YYY-thing', 'some-other-aaa-YYY-thing'])
        self.failUnlessEqual(self.find_list_('BUILT_SOURCES', lines),
                             ['some-built-source', 'some-other-built-source'])

        pass

    def test_errors(self):
        mf_am = Makefile_am()

        mf_am.add_compound_sources('the_program', 'source.c')
        self.assertRaises(Error, mf_am.add_compound_sources, 'the_program', 'source.c')

        mf_am.add_dir_primary('dir', 'PRIMARY', 'something')
        self.assertRaises(Error, mf_am.add_dir_primary, 'dir', 'PRIMARY', 'something')
        
        pass

    def test_defined_install_directories(self):
        mf_am = Makefile_am()
        mf_am.define_install_directory(symbolicname='publicheaders_blah', dirname='$(includedir)/blah')
        mf_am.add_to_install_directory(symbolicname='publicheaders_blah', family='HEADERS', files=['file1.h', 'file2.h'])
        mf_am.add_to_install_directory(symbolicname='publicheaders_blah', family='HEADERS', files=['file0.h'])

        lines = mf_am.lines()
        lines = self.collapse_continuations_(lines)

        dirdefinition = self.find_list_(name='publicheaders_blahdir', lines=lines)
        self.failIf(dirdefinition is None)
        self.failUnless(len(dirdefinition) == 1)
        self.failUnless(dirdefinition[0] == '$(includedir)/blah')

        headerlist = self.find_list_(name='publicheaders_blah_HEADERS', lines=lines)
        self.failIf(headerlist is None)
        self.failUnless(headerlist == ['file1.h', 'file2.h', 'file0.h'])
        
        pass

    def collapse_continuations_(self, lines):
        ret = []
        cur_line = None
        for l in lines:
            if cur_line:
                cur_line += l
            else:
                cur_line = l
                pass
            if not cur_line.endswith('\\'):
                ret.append(cur_line)
                cur_line = None
            else:
                cur_line = cur_line[0:-1]
                pass
            pass
        self.failUnless(cur_line is None)
        return ret

    def find_macro_(self, name, lines):
        for l in lines:
            match = rex_macro.search(l)
            if not match:
                continue
            if match.group(1) == name:
                return match.group(2)
            continue
        return None

    def find_list_(self, name, lines):
        value = self.find_macro_(name, lines)
        if value:
            values = rex_listsep.split(value)
            # some lists are terminated by
            # $(CONFIX_BACKSLASH_MITIGATOR). eliminate that.
            if len(values) > 0 and values[-1] == '$(CONFIX_BACKSLASH_MITIGATOR)':
                del values[-1]
                pass
            return values
        return None

    pass

if __name__ == '__main__':
    unittest.TextTestRunner().run(MakefileAmSuite())
    pass
