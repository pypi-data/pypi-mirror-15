==============================
pclean dist - remove distfiles
==============================

synopsis
========

pclean dist [-p] [-x EXCLUDES] [-X EXCLUDE_FILE] [-m TIME] [-s SIZE] [-I] [-f] [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [--add-config SECTION KEY VALUE] [--new-config SECTION KEY VALUE] [--empty-config] [--config PATH] [--domain DOMAIN] [-i] [TARGET [TARGET ...]]

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

file cleaning options
=====================

-m TIME, --modified TIME  
                          Don't remove files that have been modified since a given time. For
                          example, to skip files newer than a year use "1y" as an argument to this
                          option.  this option.
                          
                          Supported units are y, m, w, and d, and s representing years, months,
                          weeks, days, and seconds, respectively.

-s SIZE, --size SIZE      
                          Don't remove files bigger than a given size.  For example, to skip
                          files larger than 100 megabytes use "100M" as an argument to this
                          option.
                          
                          Supported units are B, K, M, and G representing bytes, kilobytes,
                          megabytes, and gigabytes, respectively.

repo cleaning options
=====================

-I, --installed         
                        skip files for packages that are currently installed

-f, --fetch-restricted  
                        skip fetch-restricted files

distfile options
================

-i, --ignore-failures  
                       ignore checksum parsing errors
