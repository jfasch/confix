#!/usr/bin/env python

from libconfix.core.coordinator import BuildCoordinator
from libconfix.core.builder import CompositeBuilder, FlatBuilder

from libconfix.core.hierarchy import DirectorySetupFactory
from libconfix.error import Error
from libconfix.plugins.c.setup import CSetupFactory

import sys

def print_builder(builder, indent):
    print ' '*indent + str(builder)
    if isinstance(builder, CompositeBuilder):
        for b in builder.builders():
            print_builder(b, indent+2)
            pass
        pass
    elif isinstance(builder, FlatBuilder):
        pass
    else:
        assert 0
    pass

rootdir = sys.argv[1]

try:
    pkg = Package(rootdir)
    pkg.scan()
    coordinator = BuildCoordinator(
        package=pkg,
        setups=[CSetupFactory(),
                DirectorySetupFactory()])
    coordinator.enlarge()
    print coordinator.name()+':'+coordinator.version()
    print_builder(coordinator.rootbuilder(), 0)
    pass
except Error, e:
    sys.stderr.write('***ERROR***\n')
    sys.stderr.write(`e`+'\n')
    sys.exit(1)
