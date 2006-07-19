from libconfix.plugin_salomon_bmw_assembly import BuildableBMWAssembly

BUILDABLE(
    BuildableBMWAssembly(dir=DIR(),
                         assytype=BuildableBMWAssembly.FOREGROUND,
                         assyname='the_assy',
                         components=BuildableBMWAssembly.ALL_AVAILABLE))

