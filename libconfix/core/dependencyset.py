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

from libconfix.core.repo.marshalling import Unmarshallable

from provide_string import Provide_String

class DependencySet(Unmarshallable):

    """ A template class (if this were C++) that is suppoed to hold
    either Require or Provide objects. Has special handling for the
    special purpose high performance `Provide_String` incarnations of either
    of them."""

    def __init__(self, klass, string_klass):
        self.klass_ = klass
        self.string_klass_ = string_klass
        self.string_ = {}
        self.rest_ = []
        pass

    def size(self):
        n = len(self.rest_)
        for k, v in self.string_.iteritems():
            n += len(v)
            pass
        return n

    def add(self, obj):
        assert isinstance(obj, self.klass_)
        if isinstance(obj, self.string_klass_):
            klass_dict = self.string_.setdefault(obj.__class__, {})
            existing_obj = klass_dict.get(obj.string())
            if existing_obj:
                if obj is not existing_obj:
                    existing_obj.update(obj)
                    pass
                pass
            else:
                klass_dict[obj.string()] = obj
                pass
            pass
        else:
            for o in self.rest_:
                if obj is o or o.update(obj):
                    return
                pass
            self.rest_.append(obj)
            pass
        pass

    def merge(self, other):
        for obj in other.values():
            self.add(obj)
            pass
        pass

    def values(self):
        ret = []
        for klass, klass_dict in self.string_.iteritems():
            ret.extend(klass_dict.values())
            pass
        ret.extend(self.rest_)
        return ret
