# $Id: repofile.py,v 1.3 2006/03/22 15:03:54 jfasch Exp $

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

from libconfix.core.utils.error import Error
from libconfix.core.utils import helper_pickle

import os

class RepositoryFile:

    VERSION = 1

    def __init__(self, file):
        self.file_ = file
        pass

    def load(self):
        try:
            # fixme: File.lines() is currently the only method of
            # reading the content of a file. we read the lines, join
            # them together, and then unpickle the object from the
            # whole buffer. to make this more efficient, we'd need
            # something like File.content().
            obj = helper_pickle.load_object_from_string('\n'.join(self.file_.lines()))
            if obj['version'] != RepositoryFile.VERSION:
                raise Error('Version mismatch in repository file '+os.sep.join(self.file_.abspath())+''
                            ' (file: '+str(obj['version'])+','
                            ' current: '+str(RepositoryFile.VERSION)+')')
            return obj['package']
        except Error, e:
            raise Error('Could not read repository file '+os.sep.join(self.file_.abspath()), [e])
        pass
    
    def dump(self, package):
        try:
            self.file_.truncate()
            self.file_.add_line(helper_pickle.dump_object_to_string(
                {'version': RepositoryFile.VERSION,
                 'package': package}))
        except Error, e:
            raise Error('Could not write repository file '+os.sep.join(self.file_.abspath()), [e])
        pass
    
