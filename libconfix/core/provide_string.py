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

import re
import fnmatch

from provide import Provide
from require import Require
from libconfix.core.repo.marshalling import \
     Marshallable, \
     MarshalledVersionUnknownError, \
     update_marshalling_data

class Provide_String(Provide):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Provide.get_marshalling_data(self),
            generating_class=Provide_String,
            attributes={'string': self.string_,
                        'match': self.match_},
            version={'Provide_String': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Provide_String']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.string_ = data[Marshallable.ATTRIBUTES]['string']
        self.match_ = data[Marshallable.ATTRIBUTES]['match']
        Provide.set_marshalling_data(self, data)
        pass
    
    EXACT_MATCH = 0
    PREFIX_MATCH = 1
    GLOB_MATCH = 2

    def __init__(self, string, match=EXACT_MATCH):
        assert match in [Provide_String.EXACT_MATCH,
                         Provide_String.PREFIX_MATCH,
                         Provide_String.GLOB_MATCH]
        Provide.__init__(self)
        self.string_ = string
        self.match_ = match
        pass
    def string(self):
        return self.string_
    def match(self):
        return self.match_

    def resolve(self, req):
        assert isinstance(req, Require), \
               "Provide_CInclude::resolve(): not even a Require"
        
        for c in self.can_match_classes():
            if c is req.__class__:
                break
        else:
            return 0

        if self.match_ == Provide_String.EXACT_MATCH:
            if req.string() != self.string_:
                return 0
        elif self.match_ == Provide_String.PREFIX_MATCH:
            if req.string().find(self.string_) != 0:
                return 0
        elif self.match_ == Provide_String.GLOB_MATCH:
            if not fnmatch.fnmatchcase(req.string(), self.string_):
                return 0
        return 1

    def update(self, other):
        if not isinstance(other, self. __class__):
            return False
        if self.string_ != other.string_:
            return False
        return True

    def can_match_classes(self):
        assert 0
        pass
