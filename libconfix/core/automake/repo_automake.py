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

from libconfix.core.filesys.file import File
from libconfix.core.filesys.filesys import FileSystem
from libconfix.core.filesys.scan import scan_filesystem
from libconfix.core.repo.repo import PackageRepository
from libconfix.core.repo.repofile import RepositoryFile
from libconfix.core.utils import helper_pickle, debug
from libconfix.core.utils.error import Error

import re, os, types

_re_repo = re.compile('^.*\\.repo$')

def dir_for_automake(): return os.path.join('$(datadir)', 'confix2', 'repo')

class AutomakePackageRepository(PackageRepository):

    def __init__(self, prefix):
        assert type(prefix) in [types.ListType, types.TupleType]

        PackageRepository.__init__(self)
        self.packages_ = []

        repodir = prefix+['share', 'confix2', 'repo']
        if not os.path.isdir(os.sep.join(repodir)):
            debug.warn('No repository directory '+os.sep.join(repodir))
            return
        
        self.fs_ = scan_filesystem(path=repodir)

        errlist = []

        for name, entry in self.fs_.rootdirectory().entries():
            if not isinstance(entry, File):
                continue
            if _re_repo.match(name):
                try:
                    package = RepositoryFile(entry).load()
                    self.packages_.append(package)
                except Error, e:
                    errlist.append(Error('Error reading file "'+os.sep.join(entry.abspath()), [e]))
                except Exception, e:
                    errlist.append(Error('Error reading file "'+os.sep.join(entry.abspath()), [e]))
                    pass
                pass
            pass

        if len(errlist):
            raise Error('Error in repo directory "'+os.sep.join(self.fs_.rootdirectory().abspath())+'"', errlist)

        pass

    def description(self):
        return self.dir_+' (Automake style)'

    def packages(self):
        return self.packages_

