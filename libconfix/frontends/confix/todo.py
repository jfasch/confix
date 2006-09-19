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

import os, sys

from libconfix.core.local_package import LocalPackage
from libconfix.core.utils import debug
from libconfix.core.utils import helper
from libconfix.core.utils.error import Error
from libconfix.core.filesys.scan import scan_filesystem
from libconfix.core.hierarchy import DirectorySetup
from libconfix.core.repo.repo_composite import CompositePackageRepository
from libconfix.core.digraph.cycle import CycleError
from libconfix.core.automake import bootstrap, configure, make
from libconfix.core.automake.repo_automake import AutomakePackageRepository

from libconfix.plugins.c.setup import CSetup

from confix_setup import ConfixSetup

TODO = []
CONFIG = None

repository = None
filesystem = None
package = None

def todo():
    global TODO
    for a in TODO:
        err = a()
        if err: return err
        pass
    pass

DONE_PACKAGE = 0
def PACKAGE():
    global DONE_PACKAGE
    global package
    global filesystem

    if DONE_PACKAGE: return 0

    debug.message("scanning package in %s ..." % CONFIG.packageroot(),
                  CONFIG.verbosity())

    setups = CONFIG.setups()
    if setups is None:
        setups = [ConfixSetup(use_libtool=CONFIG.use_libtool(),
                              short_libnames=CONFIG.short_libnames())]
        pass

    filesystem = scan_filesystem(path=CONFIG.packageroot().split(os.sep))
    package = LocalPackage(rootdirectory=filesystem.rootdirectory(),
                           setups=setups)
    DONE_PACKAGE = 1
    return 0

DONE_READREPO = 0
def READ_REPO():
    global DONE_READREPO
    global repository
    global ARGS

    if DONE_READREPO: return 0

    # collect list of repositories to use

    prefixes = []

    if CONFIG.prefix() is not None:
        prefixes.append(CONFIG.prefix())
        pass

##     if ARGS.has_key(const.ARG_REPOSITORY) and len(ARGS[const.ARG_REPOSITORY]):
##         if ARGS.has_key(const.ARG_READONLY_PREFIXES) and len(ARGS[const.ARG_READONLY_PREFIXES]):
##             core.debug.warn('both repositories and readonly-prefixes specified; '
##                             'taking only repositories ('+','.join(ARGS[const.ARG_REPOSITORY])+')')
##             repodirs.extend(ARGS[const.ARG_REPOSITORY][:])
##         elif ARGS.has_key(const.ARG_READONLY_PREFIXES) and len(ARGS[const.ARG_READONLY_PREFIXES]):
##             repodirs.extend([repo_automake.dir(prefix) for prefix in ARGS[const.ARG_READONLY_PREFIXES]])
##             pass
##         pass

    # make sure we don't read the same repo twice
    have = {}
    unique_prefixes = []
    for prefix in prefixes:
        dir = os.path.expanduser(os.path.expandvars(prefix))
        if not have.has_key(dir):
            have[dir] = 1
            unique_prefixes.append(dir)
            pass
        pass
    prefixes = unique_prefixes

    # finally, do our job
    repository = CompositePackageRepository()
    for prefix in prefixes:
        debug.message("reading repository "+prefix+" ", CONFIG.verbosity())
        repository.add_repo(AutomakePackageRepository(prefix=prefix.split(os.sep)))
        debug.message("done.", CONFIG.verbosity())
        pass

    DONE_READREPO = 1
    return 0

DONE_ENLARGE = 0
def ENLARGE():
    global DONE_ENLARGE
    global repository
    global package

    if DONE_ENLARGE: return 0

    if PACKAGE(): return -1
    if READ_REPO(): return -1

    # as input for the dependency graph calculation, extract all nodes
    # from our package repository.
    external_nodes = []
    for p in repository.packages():
        if p.name() != package.name():
            external_nodes.extend(p.nodes())
            pass
        pass

    debug.message("massaging package ...", CONFIG.verbosity())
    try:
        package.enlarge(external_nodes=external_nodes)
    except CycleError, e:
        for l in core.helper.format_cycle_error(e):
            sys.stderr.write(l+'\n')
            pass
        return 1
    debug.message("done massaging", CONFIG.verbosity())

    DONE_RESOLVE = 1
    return 0

DONE_DUMPGRAPH = 0
def DUMPGRAPH():
    global package
    global repository
    if ENLARGE(): return -1
    if READ_REPO(): return -1

    repo = CompositePackageRepository()
    repo.add_repo(LocalPackageRepository(package.install()))
    repo.add_repo(repository)
    modules = []
    for p in repo.packages():
        modules.extend(p.modules())
        pass
    digraph = DirectedGraph(nodes=modules, edgefinder=EdgeFinder(nodes=modules))

    pickle.dump(DirectedGraph(nodes=digraph.nodes(), edges=digraph.edges()), sys.stdout)
    return 0

DONE_BOOTSTRAP = 0
def BOOTSTRAP():
    global DONE_BOOTSTRAP
    global ARGS

    if DONE_BOOTSTRAP: return 0

    if OUTPUT(): return -1

    debug.message('+ BOOTSTRAP')
    debug.message('+ Current working directory: '+os.getcwd())
    debug.message('')

    bootstrap.bootstrap(packageroot=CONFIG.packageroot().split(os.sep),
                        use_libtool=CONFIG.use_libtool(),
                        path=None,
                        argv0=sys.argv[0])

##     am_prefix = '' # '/usr/local/automake-1.5'
##     ac_prefix = '' # '/usr/local/autoconf-2.52'
##     lt_prefix = '' # '/usr/local/libtool-1.4.0'

##     aclocal = 'aclocal'
##     autoheader = 'autoheader'
##     autoheader_args = ''
##     automake = 'automake'
##     automake_args = ' --foreign --add-missing --copy'
##     autoconf = 'autoconf'
##     autoconf_args = ''
##     libtoolize = 'libtoolize'
##     libtoolize_args = ' --force --copy'

##     assert ARGS.has_key(const.ARG_M4INCDIR)

##     aclocal_args = ''
##     for d in ARGS[const.ARG_M4INCDIR]:
##         aclocal_args = aclocal_args + ' -I ' + d

##     if (ARGS[const.ARG_USELIBTOOL]):

##         # see where libtool lives, in order to set aclocal's include
##         # path to libtool's macros (roughly stolen from apr's
##         # buildconf)

##         if os.environ.has_key('PATH'): path = os.environ['PATH']
##         else: path = ['/usr/bin']

##         libtooldir = None

##         for dir in path.split(os.pathsep):
##             file = os.path.join(dir, libtoolize)
##             if os.path.exists(file) and os.path.isfile(file) and os.access(file, os.X_OK):
##                 libtooldir = dir
##                 break

##         if libtooldir is None:
##             raise Error('libtoolize not found along path')

##         aclocal_args = aclocal_args + ' -I ' + libtooldir + '/../share/aclocal'

##     if len(am_prefix): aclocal = os.path.join(am_prefix, 'bin', aclocal)

##     aclocal = aclocal + aclocal_args # in confix2
##     debug.message(aclocal + '...') # in confix2
##     if os.system(aclocal): # in confix2
##         return -1

##     if ARGS[const.ARG_USELIBTOOL]:
##         if len(lt_prefix):
##             libtoolize = os.path.join(lt_prefix, 'bin', libtoolize)
##         libtoolize = libtoolize + libtoolize_args
##         debug.message(libtoolize + '...')
##         if os.system(libtoolize):
##             return -1

##     if len(ac_prefix): autoheader = os.path.join(ac_prefix, 'bin', autoheader)
##     autoheader = autoheader + autoheader_args # in confix2
##     debug.message(autoheader + '...') # in confix2
##     if os.system(autoheader): # in confix2
##         return -1 # in confix2

##     if len(am_prefix): automake = os.path.join(am_prefix, 'bin', automake)
##     automake = automake + automake_args # in confix2
##     debug.message(automake + '...') # in confix2
##     if os.system(automake): # in confix2
##         return -1 # in confix2

##     if ARGS[const.ARG_USE_KDE_HACK]:
##         # somehow autoconf will not create a new configure script when
##         # it decides that this is not necessary (still don't know how
##         # it would decide that). anyway, if it leaves the old script
##         # around which we have already patched, then conf.change.pl
##         # (the patch is about calling conf.change.pl) will complain
##         # about something I don't quite understand. solution: remove
##         # configure before re-creating it.
##         if os.path.isfile('configure'):
##             debug.message('KDE hack: removing existing configure script')
##             os.remove('configure')
##             pass
##         pass

##     if len(ac_prefix): autoconf = os.path.join(ac_prefix, 'bin', autoconf)
##     autoconf = autoconf + autoconf_args # in confix2
##     debug.message(autoconf + '...') # in confix2
##     if os.system(autoconf): # in confix2
##         return -1 # in confix2

##     if ARGS[const.ARG_USE_KDE_HACK]:
##         debug.message('KDE hack: patching configure script...')            
##         kde_hack.patch_configure_script('configure')
##         pass

    DONE_BOOTSTRAP = 1
    return 0

DONE_OUTPUT = 0
def OUTPUT():
    global DONE_OUTPUT
    global package
    global filesystem

    if DONE_OUTPUT: return 0

    if ENLARGE(): return -1

    debug.message("generating output ...", CONFIG.verbosity())
    package.output()
    filesystem.sync()
    debug.message("done generating output", CONFIG.verbosity())

    DONE_OUTPUT = 1
    return 0

DONE_BUILDDIR = 0
def BUILDDIR():
    global DONE_BUILDDIR
    if DONE_BUILDDIR: return 0

    if ARGS.has_key(const.ARG_BUILDDIR): return 0

    if PACKAGE(): return -1

    if not ARGS.has_key(const.ARG_BUILDROOT):
        raise Error("Cannot determine build directory because root of "
                    "package compilation tree (aka BUILDROOT) "
                    "not specified")

    global package

    builddir = os.path.join(ARGS[const.ARG_BUILDROOT], package.name())
    ARGS[const.ARG_BUILDDIR] = builddir

    DONE_BUILDDIR = 1
    return 0

DONE_CONFIGURE = 0
def CONFIGURE():
    global DONE_CONFIGURE
    if DONE_CONFIGURE: return 0

    cmdline = []
    env = {}
    env.update(os.environ)

    configure_args = CONFIG.configure_args()
    if configure_args is not None:
        cmdline.extend(configure_args)
        pass
    configure_env = CONFIG.configure_env()
    if configure_env is not None:
        env.update(configure_env)
        pass

    builddir = deduce_builddir()
    
    if CONFIG.advanced() and not os.path.exists(builddir):
        os.makedirs(builddir)
        pass
    
##     if ARGS.has_key(const.ARG_READONLY_PREFIXES) and len(ARGS[const.ARG_READONLY_PREFIXES]):
##         cmdline.append('--with-readonly-prefixes='+','.join(ARGS[const.ARG_READONLY_PREFIXES]))

    try:
        configure.configure(packageroot=CONFIG.packageroot().split(os.sep),
                            builddir=builddir.split(os.sep),
                            prefix=CONFIG.prefix().split(os.sep),
                            args=CONFIG.configure_args(),
                            env=CONFIG.configure_env())
    except Error, e:
        raise Error("Error calling configure:", [e])

    DONE_CONFIGURE = 1
    return 0

DONE_MAKE = 0
def MAKE():
    global DONE_MAKE
    if DONE_MAKE: return 0

    cmdline = []
    env = {}
    env.update(os.environ)

    make_args = CONFIG.make_args()
    if make_args is not None:
        cmdline.extend(make_args)
        pass
    make_env = CONFIG.make_env()
    if make_env is not None:
        env.update(make_env)
        pass

    builddir = deduce_builddir()

    try:
        make.make(builddir=builddir.split(os.sep),
                  args=make_args,
                  env=make_env)
    except Error, e:
        raise Error("Error calling make:", [e])

    DONE_MAKE = 1
    return 0



def deduce_builddir():
    builddir = CONFIG.builddir()
    if builddir is not None:
        return builddir
    buildroot = CONFIG.buildroot()
    if buildroot is None:
        raise Error('Cannot determine build directory: neither builddir nor buildroot are set')
    packageroot = CONFIG.packageroot()
    if packageroot is None:
        raise Error('Cannot determine build directory: need packageroot')

    PACKAGE()

    return os.path.join(buildroot, package.name()+'-'+package.version())
