# $Id: setup.py,v 1.3 2006/07/07 15:29:19 jfasch Exp $

# Copyright (C) 2002-2006 Salomon Automation

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

from builder import Builder

class Setup(Builder):

    """ A setup object is a builder which is utilized by
    L{<DirectoryBuilder>} instances to customize their
    behaviours. When a L{<DirectoryBuilder>} creates a child
    L{<DirectoryBuilder>} object of itself, it copies (clones) all its
    setup objects there. This makes the child directory builder behave
    much like it parent."""
    
    def __init__(self, id, parentbuilder, package):
        Builder.__init__(
            self,
            id=id,
            parentbuilder=parentbuilder,
            package=package)
        pass
    def clone(self, parentbuilder, package):
        assert 0, 'abstract'
        pass

    def makefile_py_iface_pieces(self):
        return []
    pass

class SetupFactory:
    def __init__(self): pass
    def create(self, parentbuilder, package):
        assert 0, 'abstract'
        pass
