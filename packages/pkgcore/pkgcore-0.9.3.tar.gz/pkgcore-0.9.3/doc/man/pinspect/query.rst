=================================================================================
pinspect query - auxiliary access to ebuild/repository info via portageq akin api
=================================================================================

synopsis
========

pinspect query [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] {best_version,env_var,get_profiles,get_repo_path,get_repos,has_version,mass_best_version} ...

optional arguments
==================

-h, --help       
                 Show this help message and exit. To get more
                 information see the related man page.

--version        
                 Show this program's version information and exit.
                 
                 When running from within a git repo or a version
                 installed from git the latest commit hash and date will
                 be shown.

--debug          
                 Enable debug checks and show verbose debug output.

-q, --quiet      
                 Suppress non-error, informational messages.

-v, --verbose    
                 Increase the verbosity of various output.

--color BOOLEAN  
                 Toggle colored output support. This can be used to forcibly
                 enable color support when piping output or other sitations
                 where stdout is not a tty.

subcommands
===========

query commands

.. toctree::
    :maxdepth: 2

    pinspect query best_version <query/best_version>
    pinspect query env_var <query/env_var>
    pinspect query get_profiles <query/get_profiles>
    pinspect query get_repo_path <query/get_repo_path>
    pinspect query get_repos <query/get_repos>
    pinspect query has_version <query/has_version>
    pinspect query mass_best_version <query/mass_best_version>
