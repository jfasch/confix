# $Id: helper_pickle.py,v 1.9 2006/06/21 11:06:49 jfasch Exp $

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

from libconfix.core.utils.error import Error, SystemError

import sys

# pickle segfaults on interix
mypickle = None
if sys.platform.startswith('interix'):
    import core.debug
    core.debug.warn('using pickle instead of cPickle on interix')
    import pickle
    mypickle = pickle
else:
    import cPickle
    mypickle = cPickle
    pass

def load_object_from_file(filename):
    try:
        file = open(filename, 'r')
    except IOError, e:
        raise Error('Cannot open file '+filename+' for reading', [e])

    try:
        object = mypickle.load(file)
    except Exception, e:
        raise Error('Cannot read Python object from file '+filename, [SystemError(e, sys.exc_traceback)])

    return object

def dump_object_to_file(object, filename):
    try:
        file = open(filename, 'w')
    except IOError, e:
        raise Error('Cannot open file '+filename+' for writing', [e])
    try:
        mypickle.dump(object, file)
    except Exception, e:
        raise Error('Cannot dump Python object "'+str(object)+'" to file '+filename, [SystemError(e, sys.exc_traceback)])

def load_object_from_string(string):
    try:
        object = mypickle.loads(string)
    except Exception, e:
        raise Error('Cannot read Python object from string', [SystemError(e, sys.exc_traceback)])

    return object

def dump_object_to_string(object):
    try:
        return mypickle.dumps(object)
    except Exception, e:
        raise Error('Cannot dump Python object to string', [SystemError(e, sys.exc_traceback)])
