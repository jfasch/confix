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

from libconfix.core.repo.marshalling import Marshallable, update_marshalling_data

from node import Node

class InstalledNode(Node):
    def get_marshalling_data(self):
        assert type(self.provides_) is types.ListType
        assert type(self.requires_) is types.ListType
        assert type(self.buildinfos_) is types.ListType
        return update_marshalling_data(
            marshalling_data=Node.get_marshalling_data(self),
            generating_class=InstalledNode,
            attributes={'provides': self.provides_,
                        'requires': self.requires_,
                        'buildinfos': self.buildinfos_},
            version={'InstalledNode': 1})
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['InstalledNode']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.provides_ = data[Marshallable.ATTRIBUTES]['provides']
        self.requires_ = data[Marshallable.ATTRIBUTES]['requires']
        self.buildinfos_ = data[Marshallable.ATTRIBUTES]['buildinfos']
        assert type(self.provides_) is types.ListType
        assert type(self.requires_) is types.ListType
        assert type(self.buildinfos_) is types.ListType
        Node.set_marshalling_data(self, data)
        pass
    
    def __init__(self, provides, requires, buildinfos):
        self.provides_ = provides
        self.requires_ = requires
        self.buildinfos_ = buildinfos
        pass
    def provides(self):
        return self.provides_
    def requires(self):
        return self.requires_
    def buildinfos(self):
        return self.buildinfos_
    pass
