==============================================================================================
pmaint copy - copy binpkgs between repositories; primarily useful for quickpkging a livefs pkg
==============================================================================================

synopsis
========

pmaint copy [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [-s SOURCE_REPO] [-i] target_repo query [query ...]

positional arguments
====================

:target_repo:  
             repository to add packages to
:query:        
             packages matching any of these restrictions will be selected for copying

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

subcommand options
==================

-s SOURCE_REPO, --source-repo SOURCE_REPO  
                                           copy strictly from the supplied repository; else it copies from wherever a match is found

-i, --ignore-existing                      
                                           if a matching pkg already exists in the target, don't update it
