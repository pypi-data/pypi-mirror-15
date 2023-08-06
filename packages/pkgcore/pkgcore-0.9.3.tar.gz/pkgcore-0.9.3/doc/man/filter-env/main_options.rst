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

-i INPUT, --input INPUT  
                         Filename to read the env from (uses stdin if omitted).

Environment filtering options
=============================

-V, --var-match          
                         Invert the filtering- instead of removing a var if it matches remove all vars that do not match

-F, --func-match         
                         Invert the filtering- instead of removing a function if it matches remove all functions that do not match

-f FUNCS, --funcs FUNCS  
                         comma separated list of regexes to match function names against for filtering

-v VARS, --vars VARS     
                         comma separated list of regexes to match variable names against for filtering

--print-vars             
                         print just the global scope environment variables.

--print-funcs            
                         print just the global scope functions.
