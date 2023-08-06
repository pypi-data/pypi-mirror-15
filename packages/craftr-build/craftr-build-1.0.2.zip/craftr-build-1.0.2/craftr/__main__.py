# Copyright (C) 2016  Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
''' That's what happens when you run Craftr. '''

import craftr
from craftr import *
from craftr import shell

import argparse
import atexit
import errno
import importlib
import os
import time
import shutil
import subprocess
import sys

from functools import partial

MANIFEST = 'build.ninja'


def _set_env(defs, main_module_name):
  ''' This function updates the environment variables based on a list
  of strings of the format `KEY=VALUE` where each subsequent part is
  optional. The following behaviour applies:

  - `KEY`: Assigns a value of `'true'` to the specified key
  - `KEY=`: Deletes the specified key from the environment
  - `KEY=VALUE`: Sets the specified key to the specified value.

  If the key is prefixed with a dot, it is prefixed with the current
  main modules name.
  '''

  for item in defs:
    key, assign, value = item.partition('=')
    if assign and not value:
      environ.pop(key, None)
      continue
    elif not assign:
      value = 'true'
    if key.startswith('.'):
      key = main_module_name + key
    environ[key] = value


def _abs_env(cwd=None):
  ''' Converts relative paths in the process environment to absolute
  paths. This is necessary since Craftr switches to another working
  directory during execution. See craftr-build/craftr#33 . '''

  cwd = path.abspath(cwd) if cwd else os.getcwd()
  def mk_abs(value):
    # Actually on Windows, there are variables like HOMEDRIVE and
    # SYSTEMDRIVE that look like 'C:' (without trailing backslash)
    # and these are not seen as absolute paths and path.join()
    # also bugs out.
    if os.name == 'nt':
      if len(value) == 2 and value[1] == ':':
        # Just a drive letter.
        return value
    if not path.isabs(value):
      test_path = path.normpath(path.join(cwd, value))
      if path.exists(test_path):
        return test_path
    return value

  for key, value in list(environ.items()):
    if key == 'PATH':
      value = path.pathsep.join(map(mk_abs, value.split(path.pathsep)))
    else:
      value = mk_abs(value)
    environ[key] = value


def _run_func(main_module, name, args):
  ''' Called to run a function with the specified *name* and passes
  it *args* as its positional arguments. If *name* is a relative
  identifier, it will be searched relative to the *main_module* name. '''

  if '.' not in name:
    name = main_module + '.' + name
  module_name, func_name = name.rsplit('.', 1)
  if module_name not in session.modules:
    error('no module "{0}" was loaded'.format(module_name))
    return errno.ENOENT
  module = session.modules[module_name]
  if not hasattr(module, func_name):
    error('module "{0}" has no member "{1}"'.format(module_name, func_name))
    return errno.ENOENT
  func = getattr(module, func_name)
  if not callable(func):
    error('"{0}" is not callable'.format(name))
    return errno.ENOENT
  try:
    func(*args)
  except SystemExit as exc:
    return exc.errno
  return 0


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('-V', action='store_true', help='Print version and exit.')
  parser.add_argument('-v', action='count', default=0, help='Increase the verbosity level.')
  parser.add_argument('-m', help='The name of a Craftr module to run.')
  parser.add_argument('-e', action='store_true', help='Export the build definitions to build.ninja')
  parser.add_argument('-b', action='store_true', help='Build all or the specified targets. Note that no Craftr modules are executed, if that is not required by other options.')
  parser.add_argument('-c', default=0, action='count', help='Clean the targets before building. Clean recursively on -cc')
  parser.add_argument('-d', help='The build directory. Defaults to "build". Can be out of tree.')
  parser.add_argument('-p', help='Specify the main directory (eventually to load the Craftfile from). If -d is not specified, the CWD is build directory.')
  parser.add_argument('-D', default=[], action='append',
    help='Set an option (environment variable). -D<key> will set <key> to the '
    'string "true". -D<key>= will delete the variable, if present. -D<key>=<value> '
    'will set the variable <key> to the string <value>. <key> can be prefixed with '
    'a dot, in which case it is prefixed with the current main modules name.')
  parser.add_argument('-f', nargs='+', help='The name of a function to execute.')
  parser.add_argument('-F', nargs='+', help='The name of a function to execute, AFTER the build process if any.')
  parser.add_argument('-I', default=[], action='append', help='Add a path to the Craftr extension module search path.')
  parser.add_argument('-N', nargs='...', default=[], help='Additional args to pass to ninja')
  parser.add_argument('--no-rc', action='store_true', help='Do not run Craftr startup files.')
  parser.add_argument('--rc', help='Execute the specified Craftr startup file. CAN be paired with --no-rc')
  parser.add_argument('--strace-depth', type=int, default=3, help='Depth of logging stack trace. Defaults to 3')
  parser.add_argument('--rts', action='store_true', help='If this option is specified, the Craftr runtime server will serve forever.')
  parser.add_argument('--rts-at', type=craftr.rts.parse_uri, help='Manually specify the host:port for the Craftr runtime server.')
  parser.add_argument('targets', nargs='*', default=[])
  args = parser.parse_args()

  # The verbosity level can not be read at some levels, that' why we
  # have to always pass it to the debug() function.
  debug = partial(craftr.debug, verbosity=args.v)

  if args.V:
    print('craftr {0}'.format(craftr.__version__))
    return 0

  if not args.d:
    if args.p:
      debug('Using "." as build directory (-p)')
      args.d = os.getcwd()
    else:
      args.d = 'build'
  if not args.p:
    args.p = os.getcwd()

  # Normalize the search path directories.
  args.I = path.normpath(args.I)

  if not args.m:
    cfile = path.join(args.p, 'Craftfile')
    if not path.isfile(cfile):
      error('{0!r} does not exist'.format(path.relpath(cfile)))
      return errno.ENOENT
    args.m = craftr.ext.get_module_ident(cfile)
    if not args.m:
      error('{0!r} has no or an invalid craftr_module(...) declaration'.format(
        path.relpath(cfile)))
      return errno.ENOENT

  build_dir_exists = os.path.isdir(args.d)
  if not path.exists(args.d):
    os.makedirs(args.d)
  elif not path.isdir(args.d):
    error('"{0}" is not a directory'.format(args.d))
    return errno.ENOTDIR

  try:
    ninja_ver = craftr.ninja.get_ninja_version()
  except OSError as exc:
    error('Ninja could not be found. Goto https://ninja-build.org/')
    return errno.ENOENT
  debug('Detected ninja v{0}'.format(ninja_ver))

  # Convert relative to absolute target names.
  mkabst = lambda x: ((args.m + x) if (x.startswith('.')) else x).replace(':', '.')
  args.targets = [mkabst(x) for x in args.targets]

  old_cwd = path.normpath(args.p)
  if os.getcwd() != path.normpath(args.d):
    started_from_build_dir = False
    os.chdir(args.d)
    info('Changed directory to "{0}"'.format(args.d))

  # If the build directory didn't exist from the start and it
  # is empty after Craftr exits, we can delete it again.
  @atexit.register
  def _delete_build_dir():
    os.chdir(old_cwd)
    if not build_dir_exists and not os.listdir(args.d):
      os.rmdir(args.d)

  # Delete the .craftr-rts file that indicates that the project used
  # the RTS feature. It will be re-created if the project still uses it.
  if args.e and path.exists('.craftr-rts'):
    os.remove('.craftr-rts')
    debug('Removed .craftr-rts flag file')

  # Delete the .cmd directory that eventually contains files with
  # command-line arguments in it. Only when we would re-generate
  # these files.
  if args.e and path.exists('.cmd'):
    debug('Removing build .cmd directory (command-line files)')
    shutil.rmtree('.cmd')

  # Check if we should omit the execution step. This is possile when
  # we the -b option is specified and NOT -c == 1, -e, -f or -F.
  do_run = any([args.e, args.f, args.F, args.rts])
  if not do_run and not args.b:
    # Do nothing at all? Then do the execution step.
    do_run = True

  if not do_run and path.exists('.craftr-rts'):
    info('Can not skip execution phase, RTS feature required')
    do_run = True
  elif not do_run:
    info("Skipping execution phase")

  if not args.e and path.isfile(MANIFEST):
    # If we're not exporting the Ninja build definitions again, we'll
    # read the ones cached in the Ninja manifest (if it exists).
    cached_defs = craftr.ninja.extract_defs(MANIFEST)
    if cached_defs:
      info('Prepending cached options:', ' '.join(shell.quote(x) for x in cached_defs))
    args.D = cached_defs + args.D

  session = craftr.Session(
    cwd=old_cwd,
    path=[old_cwd] + args.I,
    server_bind=args.rts_at,
    verbosity=args.v,
    strace_depth=args.strace_depth,
    export=args.e)
  with craftr.magic.enter_context(craftr.session, session):
    _abs_env(old_cwd)

    if do_run:
      # Run the environment files.
      if not args.no_rc:
        session.exec_if_exists(path.normpath('~/.craftrc'))
        session.exec_if_exists(path.join(old_cwd, '.craftrc'))
      if args.rc:
        rc_file = path.normpath(args.rc, old_cwd)
        if not session.exec_if_exists(rc_file):
          error('--rc {0!r} does not exist'.format(args.rc))
          return errno.ENOENT

      _set_env(args.D, args.m)
      _abs_env(old_cwd)

      # Load the main craftr module specified via the -m option
      # or the "Craftfile" of the original cwd.
      try:
        module = importlib.import_module('craftr.ext.' + args.m)
      except craftr.ModuleError as exc:
        error('Error in module {0!r}. Abort'.format(exc.module.project_name))
        return 1

      try:
        targets = [session.targets[x] for x in args.targets]
      except KeyError as key:
        error('Target {0} does not exist'.format(key))
        return errno.ENOENT

      if args.e:
        # Are there any targets that use the RTS feature? If so,
        # we must create a flag file so Craftr knows RTS is required
        # for subsequent invokations without the -e option.
        if session.rts_funcs:
          open('.craftr-rts', 'w').close()
          debug('Created .craftr-rts flag file')

        # Export a ninja manifest.
        with open(MANIFEST, 'w') as fp:
          craftr.ninja.export(fp, module, args.D)
    else:
      _set_env(args.D, args.m)
      _abs_env(old_cwd)

    # If the session has targets that require the RTS feature or
    # if the --rts flag was specified, start the RTS server.
    if args.rts or session.rts_funcs:
      session.start_server()

    # Pre-build function.
    if args.f:
      with craftr.magic.enter_context(craftr.module, module):
        _run_func(args.m, args.f[0], args.f[1:])

    # Perform a full or rule-based clean.
    if args.c:
      cmd = ['ninja', '-t', 'clean']
      if args.c == 1:
        # Non-recursive clean.
        cmd.append('-r')
      cmd += (t for t in args.targets)
      ret = shell.run(cmd, shell=True, check=False).returncode
      if ret != 0:
        return ret

    # Perform the build.
    if args.b:
      cmd = ['ninja'] + [t for t in args.targets] + args.N
      ret = shell.run(cmd, shell=True, check=False).returncode
      if ret != 0:
        return ret

    # Post-build function.
    if args.F:
      assert do_run
      with craftr.magic.enter_context(craftr.module, module):
        _run_func(args.m, args.F[0], args.F[1:])

    if args.rts:
      try:
        info('Craftr RTS alive at {0}. Use CTRL+C to stop.'.format(environ['CRAFTR_RTS']))
        while True:
          time.sleep(1)
      except KeyboardInterrupt:
        print(file=sys.stderr)
        info('Craftr RTS stopped. Bye bye')
    return 0


if __name__ == '__main__':
  sys.exit(main())

