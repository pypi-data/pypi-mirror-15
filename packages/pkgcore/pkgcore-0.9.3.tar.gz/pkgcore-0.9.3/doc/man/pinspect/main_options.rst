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

subcommands
===========

report applets

.. toctree::
    :maxdepth: 2

    pinspect pkgsets <pinspect/pkgsets>
    pinspect eapi_usage <pinspect/eapi_usage>
    pinspect license_usage <pinspect/license_usage>
    pinspect eclass_usage <pinspect/eclass_usage>
    pinspect mirror_usage <pinspect/mirror_usage>
    pinspect distfiles_usage <pinspect/distfiles_usage>
    pinspect query <pinspect/query>
    pinspect portageq <pinspect/portageq>
    pinspect profile <pinspect/profile>
    pinspect digests <pinspect/digests>
