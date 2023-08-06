================================================================================================================================================================================================================================================
pconfig dump - Dump the entire configuration in a format similar to the ini-like
default format; however, do not rely on this to always write a loadable
config. There may be quoting issues. With a typename argument only that
type is dumped.
================================================================================================================================================================================================================================================

synopsis
========

pconfig dump [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [typename]

positional arguments
====================

:typename:  
          if specified, limit output to just config directives of this type (defaults to showing all types)

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
