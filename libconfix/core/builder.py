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

import os
import types

from libconfix.core.utils.error import Error
from libconfix.core.utils.paragraph import Paragraph
from libconfix.core.automake.configure_ac import Configure_ac
from libconfix.core.automake.buildinfo import \
     BuildInfo_Configure_in, \
     BuildInfo_ACInclude_m4

from libconfix.core.iface.proxy import InterfaceProxy

from depinfo import DependencyInformation
from provide import Provide
from provide_string import Provide_String
from provide_callable import Provide_Callable
from provide_symbol import Provide_Symbol
from require import Require
from require_symbol import Require_Symbol
from require_callable import Require_Callable
from buildinfoset import BuildInformationSet

class Builder(object):
    def __init__(self, id, parentbuilder, package):
        self.id_ = id
        self.parentbuilder_ = parentbuilder
        self.package_ = package

##         self.dep_info_ = DependencyInformation()

        self.buildinfos_ = BuildInformationSet()

        # flags to ensure that every derived builder's methods have
        # called their immediate base's methods that they overload,
        # and that the chain did reach the base of all builders.
        self.base_get_dependency_info_called_ = False
        self.base_enlarge_called_ = False
        self.base_relate_called_ = False
        self.base_output_called_ = False
        
        pass
    
    def id(self): return self.id_
    def __str__(self): return self.id_

    def parentbuilder(self):
        return self.parentbuilder_
    def package(self):
        return self.package_

##     def add_require(self, r):
##         self.dep_info_.add_require(r)
##         pass
##     def add_provide(self, p):
##         self.dep_info_.add_provide(p)
##         pass
##     def add_internal_provide(self, p):
##         self.dep_info_.add_internal_provide(p)
##         pass
##     def requires(self):
##         return self.dep_info_.requires()
##     def provides(self):
##         return self.dep_info_.provides()
##     def dependency_info(self):
##         return self.dep_info_

    def get_dependency_info(self):
        self.get_dependency_info_called_ = True
        pass

    def add_buildinfo(self, b):
        self.buildinfos_.add(b)
        pass

    def buildinfos(self):
        return self.buildinfos_
    
    def enlarge(self):
        self.base_enlarge_called_ = True
        pass
    
    def relate(self, node, digraph, topolist):
        self.base_relate_called_ = True

        for n in topolist:
            for bi in n.buildinfos():
                if isinstance(bi, BuildInfo_Configure_in):
                    self.package().configure_ac().add_paragraph(
                        paragraph=Paragraph(lines=bi.lines()),
                        order=bi.order())
                    continue
                if isinstance(bi, BuildInfo_ACInclude_m4):
                    self.package().acinclude_m4().add_paragraph(
                        paragraph=Paragraph(lines=bi.lines()))
                    continue
                pass
            pass
        pass

    def node(self):
        return None
    
    def output(self):
        self.base_output_called_ = True
        pass

    def iface_pieces(self):
        return [BuilderInterfaceProxy(builder=self)]

    # these are mainly for use by test programs, and serve no real
    # functionality
    def base_get_dependency_info_called(self):
        if self.base_get_dependency_info_called_:
            self.base_get_dependency_info_called_ = False
            return True
        return False
    def base_enlarge_called(self):
        if self.base_enlarge_called_:
            self.base_enlarge_called_ = False
            return True
        return False
    def base_relate_called(self):
        if self.base_relate_called_:
            self.base_relate_called_ = False
            return True
        return False
    def base_output_called(self):
        if self.base_output_called_:
            self.base_output_called_ = False
            return True
        return False
    
    pass

class BuilderInterfaceProxy(InterfaceProxy):
    def __init__(self, builder):
        InterfaceProxy.__init__(self)

        self.builder_ = builder
        
        # PROVIDE, PROVIDE_SYMBOL, and associated flag values
        self.add_global('URGENCY_IGNORE', Require.URGENCY_IGNORE)
        self.add_global('URGENCY_WARN', Require.URGENCY_WARN)
        self.add_global('URGENCY_ERROR', Require.URGENCY_ERROR)
        self.add_global('REQUIRED', Require.URGENCY_ERROR) # backward compat with 1.5
        self.add_global('EXACT_MATCH', Provide_String.EXACT_MATCH)
        self.add_global('PREFIX_MATCH', Provide_String.PREFIX_MATCH)
        self.add_global('GLOB_MATCH', Provide_String.GLOB_MATCH)

        self.add_global('PROVIDE', getattr(self, 'PROVIDE'))
        self.add_global('REQUIRE', getattr(self, 'REQUIRE'))
        self.add_global('PROVIDE_SYMBOL', getattr(self, 'PROVIDE_SYMBOL'))
        self.add_global('REQUIRE_SYMBOL', getattr(self, 'REQUIRE_SYMBOL'))
        self.add_global('PROVIDE_CALLABLE', getattr(self, 'PROVIDE_CALLABLE'))
        self.add_global('REQUIRE_CALLABLE', getattr(self, 'REQUIRE_CALLABLE'))

        # BUILDINFORMATION
        self.add_global('BUILDINFORMATION', getattr(self, 'BUILDINFORMATION'))

        # CONFIGURE_AC, ACINCLUDE_M4, and associated flag values
        self.add_global('LOCAL', BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_LOCAL)
        self.add_global('PROPAGATE', BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_PROPAGATE)
        self.add_global('AC_BOILERPLATE', Configure_ac.BOILERPLATE)
        self.add_global('AC_OPTIONS', Configure_ac.OPTIONS)
        self.add_global('AC_PROGRAMS', Configure_ac.PROGRAMS)
        self.add_global('AC_LIBRARIES', Configure_ac.LIBRARIES)
        self.add_global('AC_HEADERS', Configure_ac.HEADERS)
        self.add_global('AC_TYPEDEFS_AND_STRUCTURES', Configure_ac.TYPEDEFS_AND_STRUCTURES)
        self.add_global('AC_FUNCTIONS', Configure_ac.FUNCTIONS)
        self.add_global('AC_OUTPUT', Configure_ac.OUTPUT)

        self.add_global('CONFIGURE_AC', getattr(self, 'CONFIGURE_AC'))
        self.add_global('ACINCLUDE_M4', getattr(self, 'ACINCLUDE_M4'))        
        
        pass

    def PROVIDE(self, provide):
        if not isinstance(provide, Provide):
            raise Error('PROVIDE(): argument must be of type '+str(Provide)+' (was '+str(provide)+')')
        self.builder_.add_provide(provide)
        pass

    def REQUIRE(self, require):
        if not isinstance(require, Require):
            raise Error('REQUIRE(): argument must be of type '+str(Require))
        self.builder_.add_require(require)
        pass

    def PROVIDE_SYMBOL(self, symbol, match=Provide_String.EXACT_MATCH):
        if not symbol or len(symbol) == 0:
            raise Error('PROVIDE_SYMBOL(): need a non-zero symbol parameter')
        if not match in [Provide_String.EXACT_MATCH, Provide_String.PREFIX_MATCH, Provide_String.GLOB_MATCH]:
            raise Error('PROVIDE_SYMBOL(): match must be one of EXACT_MATCH, PREFIX_MATCH, GLOB_MATCH')
        self.builder_.add_provide(Provide_Symbol(symbol=symbol, match=match))
        pass

    def REQUIRE_SYMBOL(self, symbol, urgency=Require.URGENCY_IGNORE):
        if not symbol or len(symbol)==0:
            raise Error('REQUIRE_SYMBOL(): need a non-zero symbol parameter')
        if not urgency in [Require.URGENCY_IGNORE, Require.URGENCY_WARN, Require.URGENCY_ERROR]:
            raise Error('REQUIRE_SYMBOL(): urgency must be one of URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR')
        self.builder_.add_require(Require_Symbol(
            symbol,
            found_in=[str(self.builder_)],
            urgency=urgency))
        pass

    def PROVIDE_CALLABLE(self, name):
        if not name or len(name) == 0:
            raise Error('PROVIDE_CALLABLE(): need a non-zero name parameter')
        self.builder_.add_provide(Provide_Callable(exename=name))
        pass

    def REQUIRE_CALLABLE(self, name, urgency=Require.URGENCY_IGNORE):
        if not name or len(name)==0:
            raise Error('REQUIRE_CALLABLE(): need a non-zero name parameter')
        if not urgency in [Require.URGENCY_IGNORE, Require.URGENCY_WARN, Require.URGENCY_ERROR]:
            raise Error('REQUIRE_SYMBOL(): urgency must be one of URGENCY_IGNORE, URGENCY_WARN, URGENCY_ERROR')
        self.builder_.add_require(Require_Callable(
            exename=name,
            found_in=[str(self.builder_)],
            urgency=urgency))
        pass

    def BUILDINFORMATION(self, buildinfo):
        self.builder_.add_buildinfo(buildinfo)
        pass

    AC_BUILDINFO_TRANSPORT_LOCAL = 0
    AC_BUILDINFO_TRANSPORT_PROPAGATE = 1
    def CONFIGURE_AC(self, lines, order, flags=None):
        if type(order) not in [types.IntType or types.LongType]:
            raise Error('CONFIGURE_AC(): "order" parameter must be an integer')
        if flags is None or BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            self.builder_.package().configure_ac().add_paragraph(
                paragraph=Paragraph(lines=lines),
                order=order)
            pass
        if flags is None or BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.builder_.add_buildinfo(BuildInfo_Configure_in(
                lines=lines,
                order=order))
            pass
        pass

    def ACINCLUDE_M4(self, lines, flags=None):
        if flags is None or BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_LOCAL in flags:
            self.builder_.package().acinclude_m4().add_paragraph(
                paragraph=Paragraph(lines=lines))
            pass
        if flags is None or BuilderInterfaceProxy.AC_BUILDINFO_TRANSPORT_PROPAGATE in flags:
            self.builder_.add_buildinfo(BuildInfo_ACInclude_m4(
                lines=lines))
            pass
        pass
    pass

class BuilderSet(object):
    def __init__(self):
        # dictionary: builder id->builder
        self.builders_ = {}
        pass

    def __iter__(self):
        return self.builders_.itervalues()

    def __contains__(self, b):
        return self.builders_.has_key(b.id())

    def __len__(self):
        return len(self.builders_)

    def values(self):
        return self.builders_.values()

    def add(self, b):
        assert not self.builders_.has_key(b.id()), str(b)
        self.builders_[b.id()] = b
        pass

    def remove(self, b):
        assert self.builders_.has_key(b.id()), str(b)
        del self.builders_[b.id()]
        pass

    def is_equal(self, other):
        if len(self.builders_) != len(other.builders_):
            return False
        for id in self.builders_.keys():
            if not other.builders_.has_key(id):
                return False
            pass
        return True
        
    pass
