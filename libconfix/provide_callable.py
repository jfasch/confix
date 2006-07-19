# $Id: provide_callable.py,v 1.7 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2003 Salomon Automation

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

from core.provide_string import Provide_String
from require_callable import Require_Callable
from core.marshalling import Marshallable, MarshalledVersionUnknownError, update_marshalling_data

class Provide_Callable(Provide_String):
    def get_marshalling_data(self):
        return update_marshalling_data(
            marshalling_data=Provide_String.get_marshalling_data(self),
            generating_class=Provide_Callable,
            attributes={},
            version={'Provide_Callable': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Provide_Callable']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        Provide_String.set_marshalling_data(self, data)
        pass


    MATCH_CLASSES = [Require_Callable]

    def __init__(self, exename):
        
        Provide_String.__init__(
            self,
            string=exename,
            match=Provide_String.EXACT_MATCH)

    def __repr__(self): return self.__class__.__name__ + ':' + self.string()

    def can_match_classes(self): return Provide_Callable.MATCH_CLASSES
