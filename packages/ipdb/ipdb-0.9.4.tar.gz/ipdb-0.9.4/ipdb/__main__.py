# Copyright (c) 2011-2016 Godefroid Chapelle and ipdb development team
#
# This file is part of ipdb.
# Redistributable under the revised BSD license
# https://opensource.org/licenses/BSD-3-Clause

from __future__ import print_function
from inspect import getargspec
import os
import sys
from pkg_resources import parse_version

from contextlib import contextmanager

import IPython


def import_module(possible_modules, needed_module):
    """Make it more resilient to different versions of IPython and try to
    find a module."""
    count = len(possible_modules)
    for module in possible_modules:
        try:
            return __import__(module, fromlist=[needed_module])
        except ImportError:
            count -= 1
            if count == 0:
                raise

if parse_version(IPython.__version__) > parse_version('0.10.2'):
    from IPython.core.debugger import Pdb, BdbQuit_excepthook

    possible_modules = ['IPython.terminal.ipapp',           # Newer IPython
                        'IPython.frontend.terminal.ipapp']  # Older IPython

    app = import_module(possible_modules, "TerminalIPythonApp")
    TerminalIPythonApp = app.TerminalIPythonApp

    possible_modules = ['IPython.terminal.embed',           # Newer IPython
                        'IPython.frontend.terminal.embed']  # Older IPython
    embed = import_module(possible_modules, "InteractiveShellEmbed")
    InteractiveShellEmbed = embed.InteractiveShellEmbed
    try:
        get_ipython
    except NameError:
        # Build a terminal app in order to force ipython to load the
        # configuration
        ipapp = TerminalIPythonApp()
        # Avoid output (banner, prints)
        ipapp.interact = False
        ipapp.initialize([])
        def_colors = ipapp.shell.colors
    else:
        # If an instance of IPython is already running try to get an instance
        # of the application. If there is no TerminalIPythonApp instanciated
        # the instance method will create a new one without loading the config.
        # i.e: if we are in an embed instance we do not want to load the config.
        ipapp = TerminalIPythonApp.instance()
        shell = get_ipython()
        def_colors = shell.colors

        # Detect if embed shell or not and display a message
        if isinstance(shell, InteractiveShellEmbed):
            shell.write_err(
                "\nYou are currently into an embedded ipython shell,\n"
                "the configuration will not be loaded.\n\n"
            )

    def_exec_lines = [line + '\n' for line in ipapp.exec_lines]

    from IPython.utils import io

    if 'nose' in sys.modules.keys():
        def update_stdout():
            # setup stdout to ensure output is available with nose
            io.stdout = sys.stdout = sys.__stdout__
    else:
        def update_stdout():
            pass
else:
    from IPython.Debugger import Pdb, BdbQuit_excepthook
    from IPython.Shell import IPShell
    from IPython import ipapi

    ip = ipapi.get()
    if ip is None:
        IPShell(argv=[''])
        ip = ipapi.get()
    def_colors = ip.options.colors
    def_exec_lines = []

    from IPython.Shell import Term

    if 'nose' in sys.modules.keys():
        def update_stdout():
            # setup stdout to ensure output is available with nose
            Term.cout = sys.stdout = sys.__stdout__
    else:
        def update_stdout():
            pass


def _init_pdb(context=3):
    if 'context' in getargspec(Pdb.__init__)[0]:
        p = Pdb(def_colors, context=context)
    else:
        p = Pdb(def_colors)
    p.rcLines += def_exec_lines
    return p


def wrap_sys_excepthook():
    # make sure we wrap it only once or we would end up with a cycle
    #  BdbQuit_excepthook.excepthook_ori == BdbQuit_excepthook
    if sys.excepthook != BdbQuit_excepthook:
        BdbQuit_excepthook.excepthook_ori = sys.excepthook
        sys.excepthook = BdbQuit_excepthook


def set_trace(frame=None, context=3):
    update_stdout()
    wrap_sys_excepthook()
    if frame is None:
        frame = sys._getframe().f_back
    p = _init_pdb(context).set_trace(frame)
    if p and hasattr(p, 'shell'):
        p.shell.restore_sys_module_state()


def post_mortem(tb=None):
    update_stdout()
    wrap_sys_excepthook()
    p = _init_pdb()
    p.reset()
    if tb is None:
        # sys.exc_info() returns (type, value, traceback) if an exception is
        # being handled, otherwise it returns None
        tb = sys.exc_info()[2]
    if tb:
        p.interaction(None, tb)


def pm():
    post_mortem(sys.last_traceback)


def run(statement, globals=None, locals=None):
    _init_pdb().run(statement, globals, locals)


def runcall(*args, **kwargs):
    return _init_pdb().runcall(*args, **kwargs)


def runeval(expression, globals=None, locals=None):
    return _init_pdb().runeval(expression, globals, locals)


@contextmanager
def launch_ipdb_on_exception():
    try:
        yield
    except Exception:
        e, m, tb = sys.exc_info()
        print(m.__repr__(), file=sys.stderr)
        post_mortem(tb)
    finally:
        pass


def main():
    import traceback
    import sys
    try:
        from pdb import Restart
    except ImportError:
        class Restart(Exception):
            pass

    if not sys.argv[1:] or sys.argv[1] in ("--help", "-h"):
        print("usage: ipdb.py scriptfile [arg] ...")
        sys.exit(2)

    mainpyfile = sys.argv[1]     # Get script filename
    if not os.path.exists(mainpyfile):
        print('Error:', mainpyfile, 'does not exist')
        sys.exit(1)

    del sys.argv[0]         # Hide "pdb.py" from argument list

    # Replace pdb's dir with script's dir in front of module search path.
    sys.path[0] = os.path.dirname(mainpyfile)

    # Note on saving/restoring sys.argv: it's a good idea when sys.argv was
    # modified by the script being debugged. It's a bad idea when it was
    # changed by the user from the command line. There is a "restart" command
    # which allows explicit specification of command line arguments.
    pdb = _init_pdb()
    while 1:
        try:
            pdb._runscript(mainpyfile)
            if pdb._user_requested_quit:
                break
            print("The program finished and will be restarted")
        except Restart:
            print("Restarting", mainpyfile, "with arguments:")
            print("\t" + " ".join(sys.argv[1:]))
        except SystemExit:
            # In most cases SystemExit does not warrant a post-mortem session.
            print("The program exited via sys.exit(). Exit status: ", end='')
            print(sys.exc_info()[1])
        except:
            traceback.print_exc()
            print("Uncaught exception. Entering post mortem debugging")
            print("Running 'cont' or 'step' will restart the program")
            t = sys.exc_info()[2]
            pdb.interaction(None, t)
            print("Post mortem debugger finished. The " + mainpyfile +
                  " will be restarted")

if __name__ == '__main__':
    main()
