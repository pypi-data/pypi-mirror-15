===========================================
pmaint regen - regenerate repository caches
===========================================

synopsis
========

pmaint regen [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [--disable-eclass-caching] [-t THREADS] [--force] [--rsync] [--use-local-desc] [--pkg-desc-index] [repo [repo ...]]

positional arguments
====================

:repo:  
      repo(s) to regenerate caches for

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

--disable-eclass-caching       
                               For regen operation, pkgcore internally turns on an optimization that
                                       caches eclasses into individual functions thus parsing the eclass only
                                       twice max per EBD processor. Disabling this optimization via this
                                       option results in ~2x slower regeneration. Disable it only if you
                                       suspect the optimization is somehow causing issues.

-t THREADS, --threads THREADS  
                               Number of threads to use for regeneration, defaults to using all
                               available processors.

--force                        
                               force regeneration to occur regardless of staleness checks or repo settings

--rsync                        
                               perform actions necessary for rsync repos (update metadata/timestamp.chk)

--use-local-desc               
                               update local USE flag description cache (profiles/use.local.desc)

--pkg-desc-index               
                               update package description cache (metadata/pkg_desc_index)
