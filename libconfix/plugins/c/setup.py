# $Id: setup.py,v 1.6 2006/07/07 15:29:19 jfasch Exp $

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

from creator import Creator
from clusterer import CClusterer
from installer import Installer
from namefinder import LongNameFinder, ShortNameFinder

from libconfix.core.setup import SetupFactory, Setup
from libconfix.core.iface import InterfacePiece

import types

class CSetupFactory(SetupFactory):
    def __init__(self, short_libnames, use_libtool):
        SetupFactory.__init__(self)
        self.short_libnames_ = short_libnames
        self.use_libtool_ = use_libtool
        pass
    def create(self, parentbuilder, coordinator):
        if self.short_libnames_ == True:
            namefinder = ShortNameFinder()
        else:
            namefinder = LongNameFinder()
            pass
        return CSetup(parentbuilder=parentbuilder,
                      coordinator=coordinator,
                      namefinder=namefinder,
                      use_libtool=self.use_libtool_)
    pass

class CSetup(Setup):
    def __init__(self,
                 parentbuilder,
                 coordinator,
                 namefinder,
                 use_libtool):
        Setup.__init__(
            self,
            id=str(self.__class__)+'('+str(parentbuilder)+')',
            parentbuilder=parentbuilder,
            coordinator=coordinator)
        self.namefinder_ = namefinder
        self.use_libtool_ = use_libtool

        # version info for libtool library is not supposed to be
        # passed in the ctor, as setup objects are always cloned from
        # the parent builder's setup objects -- and the version sure
        # differ.

        # version info, if it is set, must always be set explicitly by
        # the maintainer (actually, this is one of his jobs), so we
        # have to leave it empty.
        
        self.libtool_version_info_ = None
        
        self.bursted_ = False
        pass

    def set_libtool_version_info(self, v):
        assert type(v) in [types.ListType, types.TupleType]
        assert len(v) == 3
        self.libtool_version_info_ = v
        pass

    def clone(self, parentbuilder, coordinator):
        return CSetup(parentbuilder=parentbuilder,
                      coordinator=coordinator,
                      namefinder=self.namefinder_,
                      use_libtool=self.use_libtool_)

    def enlarge(self):
        if self.bursted_:
            return 0
        self.bursted_ = True
        self.parentbuilder().add_builder(
            Creator(parentbuilder=self.parentbuilder(),
                    coordinator=self.coordinator()))
        self.parentbuilder().add_builder(
            CClusterer(parentbuilder=self.parentbuilder(),
                       coordinator=self.coordinator(),
                       namefinder=self.namefinder_,
                       use_libtool=self.use_libtool_,
                       libtool_version_info=self.libtool_version_info_))
        self.parentbuilder().add_builder(
            Installer(parentbuilder=self.parentbuilder(),
                      coordinator=self.coordinator()))
        
        return 1 + Setup.enlarge(self)

    def makefile_py_iface_pieces(self):
        return Setup.makefile_py_iface_pieces(self) + \
               [InterfacePiece(globals={'CSETUP_': self},
                               lines=[code_])]
        
    pass    

code_ = """

from libconfix.core.utils.error import Error
import types

def LIBTOOL_LIBRARY_VERSION(version):
    if type(version) not in [types.ListType, types.TupleType]:
        raise Error("LIBTOOL_LIBRARY_VERSION: 'version' argument must be a tuple")
    if len(version) != 3:
        raise Error("LIBTOOL_LIBRARY_VERSION: 'version' argument must be a tuple of 3 integers")
    for i in range(len(version)):
        if type(version[i]) is not types.IntType:
            raise Error("LIBTOOL_LIBRARY_VERSION: part '+str(i)+' of version is not an integer")
        pass
    CSETUP_.set_libtool_version_info(version)
    pass

"""
