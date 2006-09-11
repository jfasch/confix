# $Id: depinfo.py,v 1.4 2006/03/26 19:12:46 jfasch Exp $

# Copyright (C) 2005 Salomon Automation

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

from require import Require
from require_string import Require_String
from provide import Provide
from provide_string import Provide_String
from dependencyset import DependencySet

from libconfix.core.repo.marshalling import Unmarshallable
import libconfix.core.utils.debug

class DependencyInformation(Unmarshallable):

    def __init__(self):

        self.requires_ = DependencySet(klass=Require, string_klass=Require_String)
        self.provides_ = DependencySet(klass=Provide, string_klass=Provide_String)

        # a set of provide objects that can be resolved internal to a
        # module. rationale: local C and h source files include local
        # header files like #include "file.h". the source file
        # scanning stuff can not know that this is not a real require
        # object because it does not know that file.h is present
        # locally, and produces a require object for each local
        # include. these molest the dependency graph calculation a
        # lot, so we have to weed them out. we do this by maintaining
        # this set of "internal" provide objects, which are basically
        # our local header files. (BuildableHeader is responsible for
        # filling it.)

        self.internal_provides_ = DependencySet(klass=Provide, string_klass=Provide_String)
        pass

    def size(self):
        return self.requires_.size() + \
               self.provides_.size() + \
               self.internal_provides_.size()

    def requires(self): return self.requires_.values()
    def provides(self): return self.provides_.values()
##     def public_provides(self):
##         debug.warn(str(self.__class__)+'.public_provides() is deprecated')
##         return self.provides_.values()
##     def package_provides(self):
##         debug.warn(str(self.__class__)+'.package_provides() is deprecated')
##         return []
    def internal_provides(self): return self.internal_provides_.values()

    def add_require(self, r): self.requires_.add(r)
    def add_provide(self, p): self.provides_.add(p)
    def add_internal_provide(self, p): self.internal_provides_.add(p)

##     def add_public_provide(self, p):
##         debug.warn(str(self.__class__)+'.add_public_provide() is deprecated')
##         self.provides_.add(p)
##         pass
##     def add_package_provide(self, p):
##         debug.warn(str(self.__class__)+'.add_package_provide() is deprecated')
##         self.provides_.add(p)
##         pass

    def add_requires(self, rs):
        for r in rs:
            self.requires_.add(r)
            pass
        pass
    def add_provides(self, provides):
        for p in provides:
            self.provides_.add(p)
            pass
        pass
    def add_internal_provides(self, provides):
        for p in provides:
            self.internal_provides_.add(p)
            pass
        pass
    def add(self, other):
        self.requires_.merge(other.requires_)
        self.provides_.merge(other.provides_)
        self.internal_provides_.merge(other.internal_provides_)
        pass
    pass

