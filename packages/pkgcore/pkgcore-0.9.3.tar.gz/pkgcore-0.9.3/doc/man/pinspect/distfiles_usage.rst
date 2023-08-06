===========================================================================================
pinspect distfiles_usage - report detailing distfiles space usage for targeted repositories
===========================================================================================

synopsis
========

pinspect distfiles_usage [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [--no-final-summary | --no-repo-summary | --no-detail] [--sort-by-name] [--first FIRST | --last LAST] [--include-nonmirrored] [--include-restricted] [repo [repo ...]]

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

--no-repo-summary      
                       disable outputting repo summaries

--no-detail            
                       disable outputting a detail view of all repos

--sort-by-name         
                       sort output by name, rather then by frequency

--first FIRST          
                       show only the first N detail items

--last LAST            
                       show only the last N detail items

--include-nonmirrored  
                       if set, nonmirrored  distfiles will be included in the total

--include-restricted   
                       if set, fetch restricted distfiles will be included in the total
