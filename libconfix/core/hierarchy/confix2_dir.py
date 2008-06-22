# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from confix2_dir_contributor import Confix2_dir_Contributor

from libconfix.core.iface.executor import InterfaceExecutor
from libconfix.core.iface.proxy import InterfaceProxy
from libconfix.core.machinery.filebuilder import FileBuilder
from libconfix.core.utils.error import Error

import os

class Confix2_dir(FileBuilder):
    def __init__(self, file):
        FileBuilder.__init__(self, file=file)
        self.__executed = False
        pass

    def shortname(self):
        return 'Hierarchy.Confix2_dir'

    def enlarge(self):
        super(Confix2_dir, self).enlarge()
        if self.__executed:
            return
        self.__executed = True

        ifaces = []
        ifaces.extend(self.parentbuilder().iface_pieces())
        ifaces.extend(self.package().setup().interfaces())

        try:
            InterfaceExecutor(iface_pieces=ifaces).execute_file(file=self.file())
        except Error, e:
            raise Error('Could not execute file "'+\
                        os.sep.join(self.file().relpath(self.package().rootdirectory()))+'"', [e])
        pass

    def output(self):
        super(Confix2_dir, self).output()

        # only add it to the distribution package if it is part of the
        # physical package structure
        if not self.file().is_overlayed():
            self.parentbuilder().makefile_am().add_extra_dist(self.file().name())
            pass
        pass

    pass
