# $Id: find.py,v 1.1 2006/03/27 20:20:01 jfasch Exp $

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

from libconfix.core.hierarchy import DirectoryBuilder
from libconfix.core.filebuilder import FileBuilder

import types

def find_entrybuilder(rootbuilder, path):
    assert type(path) is types.ListType
    list = path[:]
    if len(list) == 0:
        return rootbuilder
    entryname = list.pop(0)
    for b in rootbuilder.builders():
        if isinstance(b, DirectoryBuilder) and b.directory().name() == entryname:
            if len(list) == 0:
                return b
            else:
                return find_entrybuilder(b, list)
            pass
        if isinstance(b, FileBuilder) and b.file().name() == entryname:
            if len(list) == 0:
                return b
            else:
                raise Error('Found FileBuilder ('+str(b)+') and rest of path ('+list+')remains')
            pass
        pass
    return None

def find_managing_node_of_builder(nodes, builder):
    for n in nodes:
        if builder in n.managed_builders():
            return n
        pass
    return None
