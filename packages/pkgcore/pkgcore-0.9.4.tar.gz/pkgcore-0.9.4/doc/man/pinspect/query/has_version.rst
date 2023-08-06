==========================
pinspect query has_version
==========================

synopsis
========

pinspect query has_version [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [--eapi ATOM_KLS] [--use USE] [--domain DOMAIN | --domain-at-root DOMAIN] atom

description
===========

Return 0 if an atom is merged, 1 if not.

positional arguments
====================

:atom:  
      atom to inspect

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

--eapi ATOM_KLS          
                         limit all operations to just what the given EAPI supports.

--use USE                
                         override the use flags used for transititive USE deps- dev-lang/python[threads=] for example

--domain DOMAIN          
                         domain to use for this operation

--domain-at-root DOMAIN  
                         specify the domain to use via its root path
