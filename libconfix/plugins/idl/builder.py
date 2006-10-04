# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006 Joerg Faschingbauer

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

import re
import os

from libconfix.core.utils.error import Error
from libconfix.core.filebuilder import FileBuilder
from libconfix.core.require import Require

import libconfix.plugins.c.helper

from dependency import \
     Require_IDL, \
     Provide_IDL
from buildinfo import \
     BuildInfo_IDL_NativeLocal, \
     BuildInfo_IDL_NativeInstalled

class IDLBuilder(FileBuilder):
    def __init__(self, file, parentbuilder, package):
        FileBuilder.__init__(
            self,
            file=file,
            parentbuilder=parentbuilder,
            package=package)

        lines = file.lines()

        # remember the #includes for later use (we generate require
        # objects, and we generate a buildinfo object that carries
        # them). fortunately IDL is similar to C in that it uses the C
        # preprocessor for includes, so we can use the C plugin for
        # that.

        self.includes_ = libconfix.plugins.c.helper.extract_requires(lines)

        # search lines for a namespace. if one is found, our
        # install path is the namespace (or the concatenation of
        # nested namespaces). if none is found, the file is
        # installed directly into <prefix>/include.
        
        self.install_path_ = []
        paths = self.parse_modules_(lines)
        if len(paths) > 1:
            raise Error(os.sep.join(file.relpath(package.rootdirectory())) + ': error: '
                        'found multiple modules, ' + ', '.join(['::'.join(p) for p in paths]))
        if len(paths):
            for p in paths[0]:
                self.install_path_.append(p)
                pass
            pass

        external_name = '/'.join(self.install_path_ + [file.name()])
        internal_name = file.name()

        self.add_provide(Provide_IDL(external_name))
        if external_name != internal_name:
            self.add_internal_provide(Provide_IDL(internal_name))
            pass
            
        for inc in self.includes_:
            self.add_require(Require_IDL(filename=inc,
                                         found_in='/'.join(file.relpath(package.rootdirectory())),
                                         urgency=Require.URGENCY_WARN))
            pass

        self.add_buildinfo(
            BuildInfo_IDL_NativeLocal(filename='/'.join(self.install_path_ + [file.name()]),
                                      includes=self.includes_))
        pass

    def install_path(self):
        return self.install_path_

    def output(self):
        super(IDLBuilder, self).output()

        self.parentbuilder().makefile_am().add_extra_dist(self.file().name())
        self.parentbuilder().file_installer().add_private_header(
            filename=self.file().name(),
            dir=self.install_path_)
        self.parentbuilder().file_installer().add_public_header(
            filename=self.file().name(),
            dir=self.install_path_)
        pass

    re_beg_mod_ = re.compile(r'^\s*module(.*){')
    re_beg_mod_named_ = re.compile(r'^\s*(\w+)')
    re_end_mod_ = re.compile(r'^\s*}\s*;?\s*//.*(end of|/)\s*module')

    def parse_modules_(self, lines):

        stack_growth = 0
        stack = []
        found_modules = []

        lineno = 0
        for l in lines:
            lineno = lineno + 1
            m = IDLBuilder.re_beg_mod_.search(l)
            if m:
                n = IDLBuilder.re_beg_mod_named_.search(m.group(1))
                mod_name = n and n.group(1) or ''
                stack.append(mod_name)
                stack_growth = 1
                continue

            m = IDLBuilder.re_end_mod_.search(l)            
            if m:
                if len(stack) == 0:
                    raise Error(self.fullname() + ':' + str(lineno) + ': error: '
                                'end of module found though none was begun')
                if stack_growth == 1 and len(stack[-1]) > 0:
                    found_modules.append(stack[0:]) # copy, not just ref
                del stack[-1]
                stack_growth = 0
                continue

        if len(stack):
            raise Error(self.fullname()+': error: '
                        'module \''+'::'.join(stack)+'\' was opened but not closed '
                        '(remember, you have to close it with a line like \'} // /module\')')

        return found_modules
    pass