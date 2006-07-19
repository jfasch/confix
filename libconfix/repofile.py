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

from core.error import Error
import helper_pickle

class RepositoryFile:

    VERSION = 1

    def __init__(self, filename):
        self.filename_ = filename
        pass

    def load(self):
        try:
            obj = helper_pickle.load_object_from_file(self.filename_)
            if obj['version'] != RepositoryFile.VERSION:
                raise Error('Version mismatch in repository file '+self.filename_+''
                            ' (file: '+str(obj['version'])+','
                            ' current: '+str(RepositoryFile.VERSION)+')')
            return obj['package']
        except Error, e:
            raise Error('Could not read repository file '+self.filename_, [e])
        pass
    
    def dump(self, package):
        try:
            helper_pickle.dump_object_to_file({'version': RepositoryFile.VERSION,
                                               'package': package},
                                              self.filename_)
        except Error, e:
            raise Error('Could not write repository file '+self.filename_, [e])
        pass
