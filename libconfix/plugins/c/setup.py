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

import types

from libconfix.core.setup import Setup

from creator import Creator
from clusterer import CClusterer, CClustererInterfaceProxy
from installer import Installer, InstallerInterfaceProxy
from namefinder import LongNameFinder, ShortNameFinder
from iface import \
     EXTERNAL_LIBRARY_InterfaceProxy, \
     REQUIRE_H_InterfaceProxy, \
     PROVIDE_H_InterfaceProxy, \
     TESTS_ENVIRONMENT_InterfaceProxy

class CSetup(Setup):
    def __init__(self,
                 short_libnames,
                 use_libtool):
        Setup.__init__(self)

        if short_libnames == True:
            self.namefinder_ = ShortNameFinder()
        else:
            self.namefinder_ = LongNameFinder()
            pass
        self.use_libtool_ = use_libtool

        pass

    def setup_directory(self, directory_builder):
        Setup.setup_directory(self, directory_builder)
        
        clusterer = CClusterer(
            parentbuilder=directory_builder,
            package=directory_builder.package(),
            namefinder=self.namefinder_,
            use_libtool=self.use_libtool_)
        installer = Installer(
            parentbuilder=directory_builder,
            package=directory_builder.package())

        directory_builder.add_builders([Creator(parentbuilder=directory_builder,
                                                package=directory_builder.package()),
                                        clusterer,
                                        installer])

        if directory_builder.configurator() is not None:
            directory_builder.configurator().add_method(
                CClustererInterfaceProxy(object=clusterer))
            directory_builder.configurator().add_method(
                InstallerInterfaceProxy(object=installer))
            directory_builder.configurator().add_method(
                EXTERNAL_LIBRARY_InterfaceProxy(object=directory_builder.configurator()))
            directory_builder.configurator().add_method(
                REQUIRE_H_InterfaceProxy(object=directory_builder.configurator()))
            directory_builder.configurator().add_method(
                PROVIDE_H_InterfaceProxy(object=directory_builder.configurator()))
            directory_builder.configurator().add_method(
                TESTS_ENVIRONMENT_InterfaceProxy(object=directory_builder.configurator()))
            pass
        
        pass

    pass    
