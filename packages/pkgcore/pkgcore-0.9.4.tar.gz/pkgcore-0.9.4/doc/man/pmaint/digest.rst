========================================
pmaint digest - update package manifests
========================================

synopsis
========

pmaint digest [--domain DOMAIN] [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [-f] [-m] [-r REPO] [target [target ...]]

positional arguments
====================

:target:  
        Packages matching any of these restrictions will have their manifest
        entries updated; however, if no target is specified one of the
        following two cases occurs:
        
        - If a repo is specified, the entire repo is manifested.
        - If a repo isn't specified, a path restriction is created based on the
          current working directory. In other words, if `pmaint digest` is run
          within an ebuild's directory, all the ebuilds within that directory
          will be manifested. If the current working directory isn't
          within any configured repo, all repos are manifested.

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

subcommand options
==================

-f, --force           
                      Force package manifest files to be rewritten. Note that this requires
                      downloading all distfiles.

-m, --mirrors         
                      Enable checking Gentoo mirrors first for distfiles. This is disabled by
                      default because manifest generation is often performed when adding new
                      ebuilds with distfiles that aren't on Gentoo mirrors yet.

-r REPO, --repo REPO  
                      Target repository to search for matches. If no repo is specified all
                      ebuild repos are used.
