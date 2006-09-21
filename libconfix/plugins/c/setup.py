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
from clusterer import CClusterer
from installer import Installer
from namefinder import LongNameFinder, ShortNameFinder
from configurator import ConfiguratorInterface

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

    def initial_builders(self, parentbuilder, package):
        return Setup.initial_builders(self, parentbuilder=parentbuilder, package=package) + \
               [ConfiguratorInterface(parentbuilder=parentbuilder,
                                      package=package),
                Creator(parentbuilder=parentbuilder,
                        package=package),
                CClusterer(parentbuilder=parentbuilder,
                           package=package,
                           namefinder=self.namefinder_,
                           use_libtool=self.use_libtool_),
                Installer(parentbuilder=parentbuilder,
                          package=package)]

    pass    
