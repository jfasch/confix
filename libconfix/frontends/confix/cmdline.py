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

from optparse import OptionParser

from libconfix.core.utils.error import Error
from libconfix.core.utils import const

from cmdline_config import CommandlineConfiguration
import todo

def parse(args):

    parser = OptionParser(version='%prog '+const.CONFIX_VERSION)

    parser.add_option('--bootstrap',
                      action='store_true',
                      help='Generate build instructions, and feed them to the autotools.')
    parser.add_option('--output',
                      action='store_true',
                      help='Generate build instructions (no autotools invoked).')
    parser.add_option('--enlarge',
                      action='store_true',
                      help='Dry run. Massage the package as if it was for real, '
                      'but do not generate any output.')
    parser.add_option('--configure',
                      action='store_true',
                      help='Call the configure script that was generated by a bootstrap run.')
    parser.add_option('--make',
                      action='store_true',
                      help='Call the make program in the package\'s build directory.')
    
    parser.add_option('--configdir',
                      metavar='DIRECTORY',
                      help='Directory that contains the configuration file \'config\'.')
    parser.add_option('--profile',
                      metavar='NAME',
                      help='NAME of the profile to take configuration from.')
    
    parser.add_option('--packageroot',
                      metavar='DIR',
                      help='Top level directory of the package to be scanned '
                      '(default: current working directory).')
    parser.add_option('--packagename',
                      metavar='NAME',
                      help='Set the name of the package to NAME.')
    parser.add_option('--packageversion',
                      metavar='VERSION',
                      help='set the version of the package to VERSION '
                      '(preferred, but not mandated: major.minor.bugfix).')
    parser.add_option('--buildroot',
                      metavar='DIR',
                      help='Set the package build root to DIR.')
    parser.add_option('--builddir',
                      metavar='DIR',
                      help='Set the package build directory to DIR '
                      '(default: BUILDROOT/PACKAGENAME).')
    parser.add_option('--prefix',
                      metavar='DIR',
                      help='Use DIR as the installation prefix.')
    parser.add_option('--advanced',
                      help='Create build directory if necessary.')
    parser.add_option('--targets',
                      metavar='STRING',
                      help='The arguments that are passed to the make program.')
    parser.add_option('--trace',
                      metavar='STRING1,STRING2,...',
                      help='Turn on debugging for the given trace levels.')
    parser.add_option('--short-libnames',
                      action='store_true',
                      help='Generate library names that are as short as possible '
                      '(albeit still unique). You want to do this when you have '
                      'a deep directory tree with many libraries, and you constantly see your '
                      'linker line overflowing. The drawback is that the library names don\'t '
                      'generally reflect their respective source directories.')
    parser.add_option('--use-libtool',
                      action='store_true',
                      help='Generate build instructions that use libtool.')
    parser.add_option('--use-bulk-install',
                      action='store_true',
                      help='Tune up the package install time, using one or two bad hacks.')
    parser.add_option('--use-kde-hack',
                      action='store_true',
                      help='Tune up Makefile creation time, using a hack invented in the KDE project.')
    parser.add_option('--verbose',
                      action='store_const',
                      const=1,
                      dest='verbosity',
                      help='Talk a little about what\'s going on.')
    parser.add_option('--message-prefix',
                      metavar='PREFIX',
                      help='Prefix every message with PREFIX.')
    parser.add_option('--print-timings',
                      help='Some historical relic.')

    opts, args = parser.parse_args(args)

    if len(args):
        raise Error('Positional arguments are not understood')

    # collect parameters
    config = CommandlineConfiguration(
        configdir=opts.configdir,
        profile=opts.profile,
        
        packageroot=opts.packageroot,
        packagename=opts.packagename,
        packageversion=opts.packageversion,
        prefix=opts.prefix,
        buildroot=opts.buildroot,
        builddir=opts.builddir,
        short_libnames=opts.short_libnames,
        use_libtool=opts.use_libtool,
        use_bulk_install=opts.use_bulk_install,
        use_kde_hack=opts.use_kde_hack,
        print_timings=opts.print_timings,
        verbosity=opts.verbosity,
        message_prefix=opts.message_prefix,
        advanced=opts.advanced,
        )

    # collect actions
    actions = []
    if opts.bootstrap is not None:
        actions.append(todo.BOOTSTRAP)
        pass
    if opts.configure is not None:
        actions.append(todo.CONFIGURE)
        pass
    if opts.make is not None:
        actions.append(todo.MAKE)
        pass
    if opts.enlarge is not None:
        actions.append(todo.ENLARGE)
        pass
    if opts.output is not None:
        actions.append(todo.OUTPUT)
        pass

    return (config, actions)

