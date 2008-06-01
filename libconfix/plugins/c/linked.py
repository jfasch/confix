# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2008 Joerg Faschingbauer

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

from libconfix.core.machinery.builder import Builder
from libconfix.core.machinery.filebuilder import FileBuilder

class LinkedBuilder(Builder):
    def __init__(self):
        Builder.__init__(self)
        self.__members = set()
        pass

    def members(self):
        return self.__members

    def add_member(self, b):
        assert isinstance(b, FileBuilder)
        self.__members.add(b)
        pass

    def remove_member(self, b):
        self.__members.remove(b)
        pass

    pass
