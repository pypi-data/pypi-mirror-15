========================================================================
pinspect eclass_usage - report of eclass usage for targeted repositories
========================================================================

synopsis
========

pinspect eclass_usage [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [--no-final-summary] [--sort-by-name] [--first FIRST | --last LAST] [repo [repo ...]]

positional arguments
====================

:repo:  
      repo(s) to inspect

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

--no-final-summary  
                    disable outputting a summary of data across all repos

--sort-by-name      
                    sort output by name, rather then by frequency

--first FIRST       
                    show only the first N detail items

--last LAST         
                    show only the last N detail items
