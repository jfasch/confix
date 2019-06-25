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

import types
import hashlib
import os
import os.path

from libconfix.core.utils.error import Error

from .error import Error
from . import external_cmd


def find_confix_share_dir(argv0):
    '''We use the `share/confix/` directory to distribute the autoconf
    archive, and other kinds of support material. Given an argv[0], we
    use this location to find out what could be the location of the
    .../share/confix directory.

    Note that the algorithm used here is in no way comprehensive -
    rather, it just guesses, and guessing might fail.

    '''

    progdir = os.path.normpath(argv0)
    progdir = os.path.abspath(progdir)
    if not os.path.isdir(progdir):
        progdir = os.path.dirname(progdir)

    # first the uninstalled case. argv0 has been called from the
    # source directory. either the path points there, or a relative
    # path has been given. search upwards for a directory that
    # contains AUTHORS, COPYING, MANIFEST.in and guess that this is
    # the source root.
    root = progdir
    while root != '/':
        authors_file = os.path.join(root, 'AUTHORS')
        copying_file = os.path.join(root, 'COPYING')
        manifest_file = os.path.join(root, 'MANIFEST.in')

        # check for files, requiring that all three or none are there.
        have_authors = os.path.exists(authors_file) and 1 or 0
        have_copying = os.path.exists(copying_file) and 1 or 0
        have_manifest = os.path.exists(manifest_file) and 1 or 0

        all = have_authors + have_copying + have_manifest
        if all == 0:
            root = os.path.dirname(root)
            continue
        if all < 3:
            raise Error('WTF: only a subset of {AUTHORS, COPYING, MANIFEST.in} seen in {}'.format(root))
        
        # more sanity checking
        for f in (authors_file, copying_file, manifest_file):
            if not os.path.isfile(f):
                raise Error('{} is not a file'.format(f))

        return os.path.join(root, 'share', 'confix')

    # the installed case.
    root, bin = os.path.split(progdir)
    if bin != 'bin':
        raise Error("{} does not end with 'bin/'".format(argv0))
    return os.path.join(root, 'share', 'confix')

def format_cycle_error(error):

    assert error.edgelist() is not None

    lines = []
    lines.append('ERROR: cycle detected')
    lines.append(' '*2+'->'.join([n.short_description() for n in error.nodelist()]))
    lines.append('Details follow:')

    for edge in error.edgelist():
        lines.append(' '*2+edge.tail().short_description()+'->'+edge.head().short_description())
        for require in edge.annotations():
            lines.append(' '*4+str(require))
            pass
        pass
    return lines

    for i in xrange(len(path)-1):

        # from the successors of #i along the circle path, get the one
        # which is the next on the path. print the edge.

        successors = path[i].successors()

        cirlepathnode = None
        cirlepathreasons = []

        for (succnode, succreasons) in successors:
            if succnode is path[i+1]:
                cirlepathnode = succnode
                cirlepathreasons = succreasons
                break
        else:
            assert 0, \
                   'Successor ' + '.'.join(path[i+1].module().name()) + ' of ' + \
                   '.'.join(path[i].module().name()) + ' on circle path is not a successor in the dependency graph'
            pass

        lines.append('  '+'.'.join(path[i].module().name()) + ' depends on ' + '.'.join(path[i+1].module().name()) + ' because of')
        for r in succreasons:
            lines.append('    ' + str(r))
            pass
        pass

    return lines

def normalize_lines(lines):
    """
    When a line contains embedded newlines, it is split into several
    lines.
    """
    ret = None
    for i in xrange(len(lines)):
        if lines[i].find('\n') >= 0:
            if ret is None: ret = lines[:i]
            ret.extend(lines[i].split('\n'))
        else:
            if ret:
                ret.append(lines[i])
                pass
            pass
        pass
    if ret: return ret
    return lines

def md5_hexdigest_from_lines(lines):
    md5sum = hashlib.md5()
    for l in lines:
        md5sum.update(l)
        pass
    return md5sum.hexdigest()

def write_lines_to_file(filename, lines):

    """ Write lines to filename, appending newlines to each. """

    try:
        file = open(filename, 'w')
        for l in lines:
            file.write(l+'\n')
        file.close()
    except Exception as e:
        raise Error("Could not write "+filename+":", [e])

def lines_of_file(filename):

    """ Return a list containing the lines of a file, with newlines
    stripped. """

    try:
        file = open(filename, 'r')
    except IOError as e:
        raise Error('Could not open file \'' + filename + '\' for reading', [e])

    lines = [l.rstrip('\n') for l in file]
    
    file.close()
    return lines

def write_lines_to_file_if_changed(filename, lines):

    """ Write lines to filename if the lines are not what the file
    has, or if the file does not exist. (It's not that writing the
    file should be considered expensive; rather, writing the file
    unnecessarily can be expensive if the file is a dependency of
    another file in the build process.) """

    m_file = hashlib.md5()
    m_lines = hashlib.md5()

    if os.path.exists(filename):
        try:
            file = open(filename, 'r')
        except IOError as e:
            raise Error('Could not open file \'' + filename + '\' for reading', [e])
        for l in file:
            m_file.update(l)
            pass
        for l in lines:
            m_lines.update(l+'\n')
            pass

        if m_file.digest() != m_lines.digest():
            write_lines_to_file(filename, lines)
            pass
        pass

    else:
        write_lines_to_file(filename, lines)
        pass
    pass

def copy_file_if_changed(sourcename, targetname, mode):
    sourcedigest = md5_of_file(sourcename)
    if os.path.exists(targetname):
        targetdigest = md5_of_file(targetname)
    else:
        targetdigest = None
        pass
    if targetdigest is None or sourcedigest != targetdigest:
        copy_file(sourcename, targetname, mode)
        pass
    pass

def copy_file(sourcename, targetname, mode):
    try:
        sourcefile = open(sourcename, 'r')
    except IOError as e:
        raise Error('Could not open file \'' + sourcename + '\' for reading', [e])
    try:
        targetfile = open(targetname, 'w')
    except IOError as e:
        raise Error('Could not open file \'' + targetname + '\' for writing', [e])
    for l in sourcefile:
        targetfile.write(l)
        pass
    targetfile.close()
    os.chmod(targetname, mode)
    pass

def md5_of_file(filename):
    finger = hashlib.md5()
    try:
        file = open(filename, 'r')
    except IOError as e:
        raise Error('Could not open file \'' + filename + '\' for reading', [e])
    for l in file:
        finger.update(l)
        pass
    return finger.digest()

def read_boolean(b):

    """ Read a boolean from whatever we offer as boolean value, and
    return real boolean values 0 and 1, or raise an exception. """

    if b is None: return False
    if type(b) in [types.IntType, types.BooleanType]:
        return b
    if type(b) is types.StringType:
        b = b.lower()
        if b == 'yes' or b == 'y' or b == 'true' or b == 't' or b == '1':
            return True
        if b == 'no' or b == 'n' or b == 'false' or b == 'f' or b == '0':
            return False
        raise Error("Boolean value must be "
                    "'yes', 'no', 'y', 'n', 'true', 'false', "
                    "'t', 'f', '1', '0', 1, 0")
    raise Error("Bad boolean type")

def intersect_lists(l1, l2):

    dict = {}
    for el in l1:
        dict[el] = 1
    ret = []
    for el in l2:
        if dict.has_key(el): ret.append(el)

    return ret

def normalize_filename(fn):
    return fn.replace('\\', '/')

def clone_value(v):

    if type(v) is types.ListType or type(v) is types.TupleType:
        ret = []
        for e in v:
            ret.append(clone_value(e))
        return ret

    if type(v) is types.DictionaryType:
        ret = {}
        for k in v.iterkeys():
            ret[k] = clone_value(v[k])
        return ret

    return v

def make_path(str_or_list):
    if isinstance(str_or_list, types.StringType):
        if len(str_or_list) == 0:
            return []
        else:
            return str_or_list.split(os.sep)
        pass
    if isinstance(str_or_list, (list, tuple)):
        return str_or_list
    raise Error('Cannot make a path (list of strings) out of a '+str(str_or_list.__class__))
