====================================
pinspect portageq get_repo_news_path
====================================

synopsis
========

pinspect portageq get_repo_news_path [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [--eapi ATOM_KLS] [--use USE] [root] repo_id

positional arguments
====================

:root:     
         root to inspect
:repo_id:  
         repo_id to inspect

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
