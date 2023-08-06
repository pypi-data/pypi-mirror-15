==================================
pclean tmp - remove tmpdir entries
==================================

synopsis
========

pclean tmp [-p] [-x EXCLUDES] [-X EXCLUDE_FILE] [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [--add-config SECTION KEY VALUE] [--new-config SECTION KEY VALUE] [--empty-config] [--config PATH] [--domain DOMAIN] [-a] [TARGET [TARGET ...]]

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

--add-config SECTION KEY VALUE  
                                modify an existing configuration section

--new-config SECTION KEY VALUE  
                                add a new configuration section

--empty-config                  
                                do not load user/system configuration

--config PATH                   
                                override location of config files

--domain DOMAIN                 
                                domain to use for this operation

generic cleaning options
========================

TARGET                                        
                                              packages to target for cleaning

-p, --pretend                                 
                                              dry run without performing any changes

-x EXCLUDES, --exclude EXCLUDES               
                                              list of packages to exclude from removal

-X EXCLUDE_FILE, --exclude-file EXCLUDE_FILE  
                                              path to exclusion file

tmpfile options
===============

-a, --all  
           Force the entire tmpdir to be wiped. Note that this overrides any
           restrictions that have been specified.
