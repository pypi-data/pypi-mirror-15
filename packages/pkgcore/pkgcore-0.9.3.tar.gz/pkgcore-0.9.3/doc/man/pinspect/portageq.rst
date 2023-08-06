===================================================================
pinspect portageq - portageq compatible interface to query commands
===================================================================

synopsis
========

pinspect portageq [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] {best_version,envvar,envvar2,get_repo_news_path,get_repo_path,get_repos,has_version,mass_best_version,match} ...

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

portageq commands

.. toctree::
    :maxdepth: 2

    pinspect portageq best_version <portageq/best_version>
    pinspect portageq envvar <portageq/envvar>
    pinspect portageq envvar2 <portageq/envvar2>
    pinspect portageq get_repo_news_path <portageq/get_repo_news_path>
    pinspect portageq get_repo_path <portageq/get_repo_path>
    pinspect portageq get_repos <portageq/get_repos>
    pinspect portageq has_version <portageq/has_version>
    pinspect portageq mass_best_version <portageq/mass_best_version>
    pinspect portageq match <portageq/match>
