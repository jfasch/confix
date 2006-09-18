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

from node import Node
from installed_node import InstalledNode
from depinfo import DependencyInformation
from depindex import ProvideMap
from buildinfoset import BuildInformationSet
from libconfix.core.digraph import toposort

class LocalNode(Node):
    def get_marshalling_data(self):
        assert 0
        pass
    def set_marshalling_data(self, data):
        assert 0
        pass
    
    def __init__(self, responsible_builder, managed_builders):
        self.responsible_builder_ = responsible_builder
        self.managed_builders_ = managed_builders
        self.dependency_info_ = DependencyInformation()
        self.buildinfos_ = BuildInformationSet()

        # calculate dependency information ...

        # add all but internal provide objects to the node's
        # dependency info.
        for b in self.managed_builders_:
            for p in b.provides():
                self.dependency_info_.add_provide(p)
                pass
            pass

        # index provide objects
        provide_map = ProvideMap(permissive=False)
        for b in self.managed_builders_:
            for p in b.dependency_info().provides():
                provide_map.add(p, 1)
            for p in b.dependency_info().internal_provides():
                provide_map.add(p, 1)
            pass

        # add require objects that are not internally resolved to the
        # node's dependency info.
        for b in self.managed_builders_:
            for r in b.requires():
                found_nodes = provide_map.find_match(r)
                if len(found_nodes) == 0:
                    self.dependency_info_.add_require(r)
                    pass
                pass
            pass


        # collect build information ...

        for b in self.managed_builders_:
            self.buildinfos_.merge(b.buildinfos())
            pass
        
        pass
    
    def __str__(self):
        return 'LocalNode:'+str(self.responsible_builder_)+', package:'+str(self.responsible_builder_.package())
    def responsible_builder(self):
        return self.responsible_builder_
    def managed_builders(self):
        return self.managed_builders_
    def provides(self):
        return self.dependency_info_.provides()
    def requires(self):
        return self.dependency_info_.requires()
    def buildinfos(self):
        return self.buildinfos_

    def relate(self, digraph):
        topolist = toposort.toposort(digraph=digraph, nodes=[self])
        assert topolist[-1] is self
        topolist = topolist[0:-1]
        for b in self.managed_builders_:
            b.relate(node=self, digraph=digraph, topolist=topolist)
            assert b.base_relate_called(), str(b)
            pass
        pass

    def install(self):
        return InstalledNode(provides=self.dependency_info_.provides(),
                             requires=self.dependency_info_.requires(),
                             buildinfos=[b.install() for b in self.buildinfos_])
