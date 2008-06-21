# Copyright (C) 2002-2006 Salomon Automation
# Copyright (C) 2006-2007 Joerg Faschingbauer

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

class Setup(object):
    def __init__(self):
        pass
    def interfaces(self):
        """
        Returns a list of InterfaceProxy objects that define the
        methods available in Confix2.dir files.
        """
        assert False, 'abstract'
        return []
    def initial_builders(self):
        """
        Returns a list of builders that initially populate a directory
        builder.
        """
        assert False, 'abstract'
        return []
    pass

class CompositeSetup(Setup):
    def __init__(self, setups):
        Setup.__init__(self)
        self.setups_ = setups
        pass

    def initial_builders(self):
        ret = super(CompositeSetup, self).initial_builders()
        for s in self.setups_:
            ret.extend(s.initial_builders())
            pass
        return ret

    pass
