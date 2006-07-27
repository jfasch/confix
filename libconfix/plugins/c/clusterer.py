# $Id: clusterer.py,v 1.9 2006/07/13 20:27:24 jfasch Exp $

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

from base import CBaseBuilder
from compiled import CompiledCBuilder
from executable import ExecutableBuilder
from library import LibraryBuilder
import helper

from libconfix.core.builder import Builder

import os

class CClusterer(Builder):
    def __init__(self, parentbuilder, package, namefinder, use_libtool, libtool_version_info):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)
        self.namefinder_ = namefinder
        self.use_libtool_ = use_libtool
        self.libtool_version_info_ = libtool_version_info

        self.library_ = None
        # ExecutableBuilder objects, indexed by their center builders
        self.executables_ = {}
        pass

    def enlarge(self):
        ret = 0
        # copy what we will be iterating over because we will change
        # its size
        for b in self.parentbuilder().builders().values()[:]:
            if not isinstance(b, CBaseBuilder):
                continue
            if isinstance(b, CompiledCBuilder) and helper.has_main(b.file()):
                if self.executables_.has_key(b):
                    continue
                center_stem, center_ext = os.path.splitext(b.file().name())
                exe = ExecutableBuilder(
                    parentbuilder=self.parentbuilder(),
                    package=self.package(),
                    center=b,
                    exename=self.namefinder_.find_exename(packagename=self.package().name(),
                                                          path=self.parentbuilder().directory().relpath(),
                                                          centername=center_stem),
                    use_libtool=self.use_libtool_)
                self.parentbuilder().add_builder(exe)
                self.executables_[b] = exe
                ret += 1
                if self.library_ is not None:
                    self.parentbuilder().remove_builder(self.library_)
                    for m in self.library_.members():
                        exe.add_member(m)
                        pass
                    self.library_ = None
                    pass
                pass
            else:
                assert not (self.library_ and len(self.executables_))
                if not self.library_ and len(self.executables_) == 0:
                    self.library_ = LibraryBuilder(
                        parentbuilder=self.parentbuilder(),
                        package=self.package(),
                        basename=self.namefinder_.find_libname(packagename=self.package().name(),
                                                               path=self.parentbuilder().directory().relpath()),
                        use_libtool=self.use_libtool_,
                        libtool_version_info=self.libtool_version_info_)
                    self.parentbuilder().add_builder(self.library_)
                    ret += 1
                    pass
                if self.library_ is not None:
                    if b not in self.library_.members():
                        self.library_.add_member(b)
                        ret += 1
                        pass
                    pass
                for e in self.executables_.values():
                    if b not in e.members():
                        e.add_member(b)
                        ret += 1
                        pass
                    pass
                pass
            pass

        return ret + Builder.enlarge(self)
