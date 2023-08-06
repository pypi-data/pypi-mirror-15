===========================================================================================================
pinspect profile defaults - This is data parsed from make.defaults, containing things like
ACCEPT_KEYWORDS.
===========================================================================================================

synopsis
========

pinspect profile defaults [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] profile [variables [variables ...]]

positional arguments
====================

:profile:    
           path to the profile to inspect
:variables:  
           if not specified, all settings are displayed. If given, output is limited to just those settings if they exist

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
