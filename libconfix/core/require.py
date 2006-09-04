# $Id: require.py,v 1.4 2006/06/27 15:08:59 jfasch Exp $

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

from marshalling import \
     Marshallable, \
     MarshalledVersionUnknownError
from libconfix.core.utils.error import Error
import libconfix.core.utils.debug

class Require(Marshallable):
    def get_marshalling_data(self):
        return {Marshallable.GENERATING_CLASS: Require,
                Marshallable.VERSIONS: {'Require': 1},
                Marshallable.ATTRIBUTES: {'id': self.id_,
                                          'urgency': self.urgency_}}
    def set_marshalling_data(self, data):
        version = data[Marshallable.VERSIONS]['Require']
        if version != 1:
            raise MarshalledVersionUnknownError(
                klass=self.__class__,
                marshalled_version=version,
                current_version=1)
        self.id_ = data[Marshallable.ATTRIBUTES]['id']
        self.urgency_ = data[Marshallable.ATTRIBUTES]['urgency']
        pass

    # it is no accident that these are sorted by urgency level

    URGENCY_IGNORE = URGENCY_DEFAULT = URGENCY_DONTCARE = 0
    URGENCY_WARN = 1
    URGENCY_ERROR = 2

    def __init__(self, id, urgency=URGENCY_DEFAULT):
        self.id_ = id
        self.urgency_ = urgency
        pass
    def id(self):
        return self.id_
    def urgency(self):
        return self.urgency_
    def set_urgency(self, u):
        self.urgency_ = u

    def update(self, r):

        """ When multiple equivalent Require objects are added to the
        same module, this adds unnecessary (and sometimes
        considerable) overhead to the resolving process. This method
        is an attempt to collapse r with self.

        @rtype: boolean

        @return: A boolean that indicates whether the objects could be
        collapsed.

        """

        debug.abstract('Require.update()')
        pass

