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

import os
import types

from libconfix.core.builder import Builder
from libconfix.core.iface.proxy import InterfaceProxy

from base import CBaseBuilder
from compiled import CompiledCBuilder
from executable import ExecutableBuilder
from library import LibraryBuilder
import helper

class CClusterer(Builder):
    def __init__(self, parentbuilder, package, namefinder, use_libtool):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            package=package)
        self.namefinder_ = namefinder
        self.use_libtool_ = use_libtool
        self.libtool_version_info_ = (0,0,0)

        self.library_ = None
        # ExecutableBuilder objects, indexed by their center builders
        self.executables_ = {}
        pass

    def set_libtool_version_info(self, version_tuple):
        self.libtool_version_info_ = version_tuple
        pass

    def enlarge(self):
        super(CClusterer, self).enlarge()
        # copy what we will be iterating over because we will change
        # its size
        for b in self.parentbuilder().builders().values()[:]:
            if not isinstance(b, CBaseBuilder):
                continue
            if isinstance(b, CompiledCBuilder) and (helper.has_main(b.file()) or b.exename() is not None):
                if self.executables_.has_key(b):
                    # already got that one.
                    continue
                center_stem, center_ext = os.path.splitext(b.file().name())
                if center_stem.startswith('_check'):
                    what = ExecutableBuilder.CHECK
                elif center_stem.startswith('_'):
                    what = ExecutableBuilder.NOINST
                else:
                    what = ExecutableBuilder.BIN
                    pass
                exename = b.exename()
                if exename is None:
                    exename = self.namefinder_.find_exename(
                        packagename=self.package().name(),
                        path=self.parentbuilder().directory().relpath(self.package().rootdirectory()),
                        centername=center_stem)
                    pass
                exe = ExecutableBuilder(
                    parentbuilder=self.parentbuilder(),
                    package=self.package(),
                    center=b,
                    exename=exename,
                    use_libtool=self.use_libtool_,
                    what=what)
                self.parentbuilder().add_builder(exe)
                self.executables_[b] = exe
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
                                                               path=self.parentbuilder().directory().relpath(self.package().rootdirectory())),
                        use_libtool=self.use_libtool_,
                        libtool_version_info=self.libtool_version_info_)
                    self.parentbuilder().add_builder(self.library_)
                    pass
                if self.library_ is not None:
                    if b not in self.library_.members():
                        self.library_.add_member(b)
                        pass
                    pass
                for e in self.executables_.values():
                    if b not in e.members():
                        e.add_member(b)
                        pass
                    pass
                pass
            pass
        pass
    pass

class CClustererInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self)
        self.object_ = object
        self.add_global('LIBTOOL_LIBRARY_VERSION', getattr(self, 'LIBTOOL_LIBRARY_VERSION'))
        pass

    def LIBTOOL_LIBRARY_VERSION(self, version):
        if type(version) not in [types.ListType, types.TupleType]:
            raise Error("LIBTOOL_LIBRARY_VERSION: 'version' argument must be a tuple")
        if len(version) != 3:
            raise Error("LIBTOOL_LIBRARY_VERSION: 'version' argument must be a tuple of 3 integers")
        for i in range(len(version)):
            if type(version[i]) is not types.IntType:
                raise Error("LIBTOOL_LIBRARY_VERSION: part "+str(i)+" of version is not an integer")
            pass
        self.object_.set_libtool_version_info(version)
        pass

    pass
