from libconfix.plugins.mico.local import LocalMicoIDLGenerator
import libconfix.helper

idlfile = 'localinterface.idl'

BUILDABLE(LocalMicoIDLGenerator(
    dir=DIR(),
    filename=idlfile,
    lines=libconfix.helper.lines_of_file(idlfile)))
