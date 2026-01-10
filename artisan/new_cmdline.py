import pathlib
import sys
import argparse
import os
import shlex

def parse(cmd=None):
    supported_source_ext = {'.cpp', '.cc', '.c', '.cl', '.cu', '.h', '.hpp', '.hh' }

    argp = argparse.ArgumentParser(add_help=False)

    # Add arguments mimicking clang/g++ options
    argp.add_argument('-I', action='append', nargs=1, help="Add include directory", metavar="DIR")
    argp.add_argument('-D', action='append', nargs=1, help="Define a preprocessor macro", metavar="MACRO")
    argp.add_argument('-U', action='append', nargs=1, help="Undefine a preprocessor macro", metavar="MACRO")
    argp.add_argument('-std',  nargs=1, help="Specify the standard of C++ to use")
    argp.add_argument('-include', action='append', nargs=1, help="Include file before processing", metavar="FILE")
    # Add optional parameters -wd (work directory) and -pp (integer option)
    argp.add_argument('-wd', type=str, action='store', help="Set working directory", metavar="WORKDIR")
    # Add positional arguments for source files
    argp.add_argument('-nodefaults', action='store_true', help="Disable default behavior")


    argp.add_argument('sources', nargs='*', help="Source files to compile", metavar="FILE")


    # argp.add_argument('-D', dest = 'defines',  nargs = 1, action = 'append', help = 'Predefine name as a macro [with value]')
    # argp.add_argument('-U', dest = 'undefines',  nargs = 1, action = 'append', help = 'Pre-undefine name as a macro')
    # argp.add_argument('-I', dest = 'includes',  nargs = 1, action = 'append', help = "Path to search for unfound #include's")
    # argp.add_argument('-include', dest = 'headers',  nargs = 1, action = 'append', help = "Include headers")


    # we are keeping it simple. Sources correspond to
    # args that do not start with '-' and end with one
    # of the supported extensions (supported_source_ext)

    if cmd is None:
        cmdlst = sys.argv[1:]
    else:
        cmdlst = shlex.split(cmd)

    extra_flags = ""
    # add ARTISAN_CXXFLAGS if exists
    cxxflags = os.getenv('ARTISAN_CXXFLAGS')
    if cxxflags is not None:
        extra_flags = extra_flags + " " + cxxflags

    # add ARTISAN_CXXFLAGS_FE if exists
    cxxflags_fd = os.getenv('ARTISAN_CXXFLAGS_FE')
    if cxxflags_fd is not None:
        extra_flags = extra_flags + " " + cxxflags_fd


    cmdlst.extend(shlex.split(extra_flags))

    # specify C++ standard
    # only override if not specified
    specified_std=False
    for arg in cmdlst:
        if arg.startswith("-std="):
            specified_std = True
            break
    if not specified_std:
        cxxstd = os.getenv('ARTISAN_CXXSTD')
        if cxxstd is not None:
            cmdlst.append('-std=%s' % cxxstd)

    # parse arguments
    spec, unspec = argp.parse_known_args(cmdlst)

    print("spec=", spec)
    print("unspec=", unspec)

    exit(0)

    source_names = []
    compiler_args = []
    preproc_args = []

    for elem in unspec:
        if elem[0] != '-' and pathlib.Path(elem).suffix in supported_source_ext:
            source_names.append(elem)
        else:
            compiler_args.append(elem)


    if spec.includes is not None:
        for incl in spec.includes:
           compiler_args.extend(['-I', incl[0]])

    if spec.headers is not None:
        for s in spec.headers:
           compiler_args.extend(['-include', s[0]])

    if spec.defines is not None:
        for s in spec.defines:
           preproc_args.extend(['-D', s[0]])

    if spec.undefines is not None:
        for s in spec.undefines:
           preproc_args.extend(['-U', s[0]])

    return (source_names, compiler_args, preproc_args)


















