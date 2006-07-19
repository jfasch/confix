# $Id: repo_composite.py,v 1.3 2006/03/22 15:03:54 jfasch Exp $

# Copyright (C) 2004 Salomon Automation

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

from repo import PackageRepository
from core.error import Error

class CompositePackageRepository(PackageRepository):

    def __init__(self):

        PackageRepository.__init__(self)
        self.repositories_ = []

    def description(self):

        return 'Composite: '+','.join([r.description() for r in self.repositories()])

    def add_repo(self, repo):

        self.repositories_.append(repo)

    def packages(self):

        ret_packages = []
        have_packages = {}

        for r in self.repositories_:
            for p in r.packages():
                if have_packages.has_key(p.name()):
                    continue
                have_packages[p.name()] = 1
                ret_packages.append(p)

        return ret_packages
