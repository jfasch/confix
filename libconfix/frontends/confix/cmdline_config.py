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

from config import Configuration

class CommandlineConfiguration(Configuration):
    def __init__(self):
        self.prefix_ = None
        self.buildroot_ = None
        self.use_libtool_ = None
        self.use_bulk_install_ = None
        self.use_kde_hack_ = None
        self.print_timings_ = None
        self.message_prefix_ = None
        self.advanced_ = None
        pass

    def prefix(self): return self.prefix_
    def buildroot(self): return self.buildroot_
    def use_libtool(self): return self.use_libtool_
    def use_bulk_install(self): return self.use_bulk_install_
    def use_kde_hack(self): return self.use_kde_hack_
    def print_timings(self): return self.print_timings_
    def message_prefix(self): return self.message_prefix_
    def advanced(self): return self.advanced_

    def configure(self): return None
    
