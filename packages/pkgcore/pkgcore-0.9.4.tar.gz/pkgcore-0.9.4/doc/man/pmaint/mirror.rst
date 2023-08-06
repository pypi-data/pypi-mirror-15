================================================================================================
pmaint mirror - mirror the sources for a package in full- grab everything that could be required
================================================================================================

synopsis
========

pmaint mirror [--domain DOMAIN] [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [-f] query [query ...]

positional arguments
====================

:query:  
       query of which packages to mirror

optional arguments
==================

--domain DOMAIN  
                 domain to use for this operation

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

subcommand options
==================

-f, --ignore-failures  
                       Keep going even if a failure occurs. By default, the first failure
                       encountered stops the process.
