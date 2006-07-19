# $Id: repo_automake.py,v 1.7 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2002 Salomon Automation
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

from core.error import Error
from repo import PackageRepository
from repofile import RepositoryFile
from modbase import ModuleBase
import helper_pickle
import core.debug

import re
import os

_re_repo = re.compile('^.*\\.repo$')

def dir(prefix): return os.path.join(prefix, 'share', 'confix', 'repo')
def dir_for_automake(): return os.path.join('$(datadir)', 'confix', 'repo')

class AutomakePackageRepository(PackageRepository):

    def __init__(self, dir):
        PackageRepository.__init__(self)
        self.dir_ = dir
        self.packages_ = []

        errlist = []
        if not os.path.isdir(self.dir_):
            core.debug.warn('No repository directory '+self.dir_)
            return

        for f in os.listdir(self.dir_):
            fullpath = os.path.join(self.dir_, f)
            if _re_repo.match(f) and os.path.isfile(fullpath):
                try:
                    self.packages_.append(RepositoryFile(fullpath).load())
                except Error, e:
                    errlist.append(Error('Error reading file ' + fullpath, [e]))
                except Exception, e:
                    errlist.append(Error('Error reading file ' + fullpath, [e]))
                    pass
                pass
            pass
        
        if len(errlist):
            raise Error('Error in repo directory ' + dir, errlist)

        pass

    def description(self):
        return self.dir_+' (Automake style)'

    def packages(self): return self.packages_

