# Copyright (C) 2008 Joerg Faschingbauer

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

from configure_ac import Configure_ac

from libconfix.core.hierarchy.confix2_dir_contributor import Confix2_dir_Contributor
from libconfix.core.machinery.setup import Setup
from libconfix.core.iface.proxy import InterfaceProxy

import types

class AutomakeInterfaceSetup(Setup):
    def initial_builders(self):
        return super(AutomakeInterfaceSetup, self).initial_builders() + [AutomakeInterface_Confix2_dir()]
    pass

class AutomakeInterface_Confix2_dir(Confix2_dir_Contributor):
    def get_iface_proxies(self):
        return [AutomakeInterfaceProxy(object=self)]
    def locally_unique_id(self):
        return str(self.__class__)
    def initialize(self, package):
        super(AutomakeInterface_Confix2_dir, self).initialize(self.package)
        pass
    pass

class AutomakeInterfaceProxy(InterfaceProxy):
    def __init__(self, object):
        InterfaceProxy.__init__(self, object)

        self.add_global('LOCAL', self.AC_BUILDINFO_TRANSPORT_LOCAL)
        self.add_global('PROPAGATE', self.AC_BUILDINFO_TRANSPORT_PROPAGATE)
        self.add_global('AC_BOILERPLATE', Configure_ac.BOILERPLATE)
        self.add_global('AC_OPTIONS', Configure_ac.OPTIONS)
        self.add_global('AC_PROGRAMS', Configure_ac.PROGRAMS)
        self.add_global('AC_LIBRARIES', Configure_ac.LIBRARIES)
        self.add_global('AC_HEADERS', Configure_ac.HEADERS)
        self.add_global('AC_TYPEDEFS_AND_STRUCTURES', Configure_ac.TYPEDEFS_AND_STRUCTURES)
        self.add_global('AC_FUNCTIONS', Configure_ac.FUNCTIONS)
        self.add_global('AC_OUTPUT', Configure_ac.OUTPUT)

        self.add_global('CONFIGURE_AC', getattr(self, 'CONFIGURE_AC'))
        self.add_global('ACINCLUDE_M4', getattr(self, 'ACINCLUDE_M4'))

        pass

    AC_BUILDINFO_TRANSPORT_LOCAL = 0
    AC_BUILDINFO_TRANSPORT_PROPAGATE = 1
    def CONFIGURE_AC(self, lines, order, flags=None):
        if type(order) not in [types.IntType or types.LongType]:
            raise Error('CONFIGURE_AC(): "order" parameter must be an integer')
        if flags is None or self.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            print 'CONFIGURE_AC '+str(self.object())+' '+str(self.object().package())
            self.object().package().configure_ac().add_paragraph(
                paragraph=Paragraph(lines=lines),
                order=order)
            pass
        if flags is None or self.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.object().add_buildinfo(BuildInfo_Configure_in(
                lines=lines,
                order=order))
            pass
        pass

    def ACINCLUDE_M4(self, lines, flags=None):
        if flags is None or self.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            self.object().package().acinclude_m4().add_paragraph(
                paragraph=Paragraph(lines=lines))
            pass
        if flags is None or self.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.object().add_buildinfo(BuildInfo_ACInclude_m4(
                lines=lines))
            pass
        pass
        
    pass
