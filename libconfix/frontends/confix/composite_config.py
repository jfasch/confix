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

class CompositeConfiguration(Configuration):
    def __init__(self):
        Configuration.__init__(self)
        self.configurations_ = []
        pass

    def add(self, config):
        self.configurations_.append(config)
        pass

    def prefix(self): return self.search_param_('prefix')
    def buildroot(self): return self.search_param_('buildroot')
    def use_libtool(self): return self.search_param_('use_libtool')
    def use_bulk_install(self): return self.search_param_('use_bulk_install')
    def use_kde_hack(self): return self.search_param_('use_kde_hack')
    def print_timings(self): return self.search_param_('print_timings')
    def message_prefix(self): return self.search_param_('message_prefix')
    def advanced(self): return self.search_param_('advanced')
    def configure(self): return self.search_param_('configure')

    def search_param_(self, methodname):
        for config in self.configurations_:
            method = getattr(config, methodname)
            ret = apply(config, method)
            if ret:
                return ret
            pass
        else:
            return None
        pass

    pass
