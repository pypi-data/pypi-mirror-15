===========================================================================
pconfig configurables - list registered configurables (may not be complete)
===========================================================================

synopsis
========

pconfig configurables [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [typename]

positional arguments
====================

:typename:  
          if specified, only output configurables of that type; else output all configurables

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
