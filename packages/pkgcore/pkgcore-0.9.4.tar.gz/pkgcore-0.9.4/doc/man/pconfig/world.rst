=================================================
pconfig world - inspect and modify the world file
=================================================

synopsis
========

pconfig world [--domain DOMAIN] [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [-l] [-r REMOVE] [-a ADD]

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

command modes
=============


These options are directives for what to do with the world file. You
can do multiple operations in a single invocation.  For example, you
can have `--add x11-wm/fluxbox --remove gnome-base/gnome -l` to add
fluxbox, remove gnome, and list the world file contents all in one
call.


-l, --list                  
                            List the current world file contents for this domain.

-r REMOVE, --remove REMOVE  
                            Remove an entry from the world file.  Can be specified multiple times.

-a ADD, --add ADD           
                            Add an entry to the world file.  Can be specified multiple times.
