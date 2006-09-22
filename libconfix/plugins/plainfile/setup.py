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

from iface import PLAINFILE_InterfaceProxy

class PlainFileSetup(Setup):
    def __init__(self):
        Setup.__init__(self)
        pass

    def setup_directory(self, directory_builder):
        Setup.setup_directory(self, directory_builder)
        directory_builder.configurator().add_method(
            PLAINFILE_InterfaceProxy(object=directory_builder))
        pass

    pass    
