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

from libconfix.core.builder import Builder

from iface import EXTERNAL_LIBRARY_InterfaceProxy, \
     REQUIRE_H_InterfaceProxy, \
     PROVIDE_H_InterfaceProxy

class ConfiguratorInterface(Builder):
    def __init__(self, parentbuilder, package):
        Builder.__init__(
            self,
            id=str(self.__class__)+'('+os.sep.join(parentbuilder.directory().relpath(package.rootdirectory()))+')',
            parentbuilder=parentbuilder,
            package=package)
        pass
    def confix2_in_iface_pieces(self):
        return [EXTERNAL_LIBRARY_InterfaceProxy(object=self),
                REQUIRE_H_InterfaceProxy(object=self),
                PROVIDE_H_InterfaceProxy(object=self)]
    pass

