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
from configure_config import ConfigureConfig

class Profile(Configuration):

    PREFIX = 'PREFIX'
    BUILDROOT = 'BUILDROOT'
    USE_LIBTOOL = 'USE_LIBTOOL'
    USE_BULK_INSTALL = 'USE_BULK_INSTALL'
    USE_KDE_HACK = 'USE_KDE_HACK'
    PRINT_TIMINGS = 'PRINT_TIMINGS'
    MESSAGE_PREFIX = 'MESSAGE_PREFIX'
    ADVANCED = 'ADVANCED'
    CONFIGURE = 'CONFIGURE'

    def __init__(self, dict):
        self.dictionary_ = dict
        pass

    def prefix(self):
        return self.dictionary_.get(ConfigProfile.PREFIX)
    def buildroot(self):
        return self.dictionary_.get(ConfigProfile.BUILDROOT)
    def use_libtool(self):
        return self.dictionary_.get(ConfigProfile.USE_LIBTOOL)
    def use_bulk_install(self):
        return self.dictionary_.get(ConfigProfile.USE_BULK_INSTALL)
    def use_kde_hack(self):
        return self.dictionary_.get(ConfigProfile.USE_KDE_HACK)
    def print_timings(self):
        return self.dictionary_.get(ConfigProfile.PRINT_TIMINGS)
    def message_prefix(self):
        return self.dictionary_.get(ConfigProfile.MESSAGE_PREFIX)
    def advanced(self):
        return self.dictionary_.get(ConfigProfile.ADVANCED)

    def configure(self):
        dict = self.dictionary_.get(ConfigProfile.CONFIGURE)
        if dict is not None:
            return ConfigureConfig(dict)
        return None
    

##         if dict.has_key(const.CFG_PROF_CONFIX_READONLY_PREFIXES):
##             if not type(dict[const.CFG_PROF_CONFIX_READONLY_PREFIXES]) is ListType:
##                 raise Error("'"+const.CFG_PROF_CONFIX_READONLY_PREFIXES+"' must be a list")
##             self.readonly_prefixes_ = dict[const.CFG_PROF_CONFIX_READONLY_PREFIXES]
##         else:
##             self.readonly_prefixes_ = None

##         if dict.has_key(const.CFG_PROF_BUILDROOT):
##             self.buildroot_ = dict[const.CFG_PROF_BUILDROOT]
##         else:
##             self.buildroot_ = None

##         if dict.has_key(const.CFG_PROF_USE_LIBTOOL):
##             try:
##                 self.use_libtool_ = core.helper.read_boolean(dict[const.CFG_PROF_USE_LIBTOOL])
##             except Error, e:
##                 raise Error("Could not read boolean value '"+const.CFG_PROF_USE_LIBTOOL+"'")
##         else:
##             self.use_libtool_ = None

##         if dict.has_key(const.CFG_PROF_USE_BULK_INSTALL):
##             try:
##                 self.use_bulk_install_ = helper.read_boolean(dict[const.CFG_PROF_USE_BULK_INSTALL])
##             except Error, e:
##                 raise Error("Could not read boolean value '"+const.CFG_PROF_USE_BULK_INSTALL+"'")
##         else:
##             self.use_bulk_install_ = None

##         if dict.has_key(const.CFG_PROF_USE_KDE_HACK):
##             try:
##                 self.use_kde_hack_ = helper.read_boolean(dict[const.CFG_PROF_USE_KDE_HACK])
##             except Error, e:
##                 raise Error("Could not read boolean value '"+const.CFG_PROF_USE_KDE_HACK+"'")
##         else:
##             self.use_kde_hack_ = None

##         if dict.has_key(const.CFG_PROF_MESSAGE_PREFIX):
##             self.message_prefix_ = dict[const.CFG_PROF_MESSAGE_PREFIX]
##         else:
##             self.message_prefix_ = ''

##         if dict.has_key(const.CFG_PROF_PRINT_TIMINGS):
##             try:
##                 self.print_timings_ = helper.read_boolean(dict[const.CFG_PROF_PRINT_TIMINGS])
##             except Error, e:
##                 raise Error("Could not read boolean value '"+const.CFG_PROF_PRINT_TIMINGS+"'")
##         else:
##             self.print_timings_ = None

##         if dict.has_key(const.CFG_PROF_ADVANCED):
##             try:
##                 self.advanced_ = core.helper.read_boolean(dict[const.CFG_PROF_ADVANCED])
##             except Error, e:
##                 raise Error("Could not read boolean value '"+const.CFG_PROF_ADVANCED+"'")
##         else:
##             self.advanced_ = None




##         if dict.has_key(const.CFG_PROF_CONFIX):
##             try:
##                 self.confix_ = ConfigConfix(dict[const.CFG_PROF_CONFIX])
##             except Error, e:
##                 raise Error("Error in '"+const.CFG_PROF_CONFIX+"' section", [e])
##         else:
##             self.confix_ = ConfigConfix()

##         if dict.has_key(const.CFG_PROF_CONFIGURE):
##             try:
##                 self.configure_ = ConfigConfigure(dict[const.CFG_PROF_CONFIGURE])
##             except Error, e:
##                 raise Error("Error in '"+const.CFG_PROF_CONFIGURE+"' section", [e])
##         else:
##             self.configure_ = ConfigConfigure()

##         if dict.has_key(const.CFG_PROF_MAKE):
##             try:
##                 self.make_ = ConfigMake(dict[const.CFG_PROF_MAKE])
##             except Error, e:
##                 raise Error("Error in '"+const.CFG_PROF_MAKE+"' section", [e])
##         else:
##             self.make_ = ConfigMake()

##     def prefix(self):
##         return self.prefix_

##     def readonly_prefixes(self):
##         return self.readonly_prefixes_

##     def buildroot(self):
##         return self.buildroot_

##     def use_libtool(self):
##         return self.use_libtool_

##     def use_bulk_install(self):
##         return self.use_bulk_install_

##     def use_kde_hack(self):
##         return self.use_kde_hack_

##     def message_prefix(self):
##         return self.message_prefix_

##     def print_timings(self):
##         return self.print_timings_

##     def advanced(self):
##         return self.advanced_

##     def confix(self):
##         return self.confix_

##     def configure(self):
##         return self.configure_

##     def make(self):
##         return self.make_
