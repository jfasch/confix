# $Id: iface.py,v 1.7 2006/07/07 15:29:19 jfasch Exp $

# Copyright (C) 2002-2006 Salomon Automation

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

import filesys
from libconfix.core.utils.error import Error, SystemError

import os
import sys
import types

class CodePiece:
    def __init__(self, start_lineno, lines):
        self.start_lineno_ = start_lineno
        self.lines_ = lines
        pass
    def start_lineno(self):
        return self.start_lineno_
    def lines(self):
        return self.lines_
    pass

class InterfacePiece:
    def __init__(self, globals, lines):
        assert type(globals) is types.DictionaryType
        self.globals_ = globals
        self.lines_ = lines
        pass
    def globals(self):
        return self.globals_
    def lines(self):
        return self.lines_
    pass

class InterfaceExecutor:
    def __init__(self, iface_pieces):
        self.context_ = {}
        for piece in iface_pieces:
            for n, v in piece.globals().iteritems():
                assert type(n) is types.StringType
                assert not self.context_.has_key(n), n
                self.context_[n] = v
                pass
            assert type(piece.lines()) is types.ListType or type(piece.lines()) is types.TupleType
            code = '\n'.join(piece.lines())
            exec code in self.context_
            pass
        pass

    def execute_file(self, file):
        assert isinstance(file, filesys.file.File), file
        assert file.parent() is not None
        assert isinstance(file.parent(), filesys.directory.Directory)

        chdirbackto = None
            
        try:
            if file.is_persistent():
                chdirbackto = os.getcwd()
                os.chdir(file.parent().abspath())
                execfile(file.name(), self.context_)
                os.chdir(chdirbackto)
                return
            else:
                exec '\n'.join(file.lines()) in self.context_
                return
            pass
        except Exception, e:
            if chdirbackto is not None:
                os.chdir(chdirbackto)
                pass
            raise Error('Error in '+'/'.join(file.relpath()), [SystemError(e, sys.exc_traceback)])
        pass

    def execute_pieces(self, pieces):
        for p in pieces:
            try:
                exec '\n'.join(p.lines()) in self.context_
            except Exception, e:
                raise Error('Error in code piece starting at line '+str(p.start_lineno())+' ('+p.lines()[0]+')',
                            [SystemError(e, sys.exc_traceback)])
            pass
        pass
    pass
