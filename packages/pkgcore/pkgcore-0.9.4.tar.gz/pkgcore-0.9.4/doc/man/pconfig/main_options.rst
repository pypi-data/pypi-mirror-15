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

configuration related subcommands

.. toctree::
    :maxdepth: 2

    pconfig classes <pconfig/classes>
    pconfig describe_class <pconfig/describe_class>
    pconfig uncollapsable <pconfig/uncollapsable>
    pconfig dump <pconfig/dump>
    pconfig configurables <pconfig/configurables>
    pconfig dump-uncollapsed <pconfig/dump-uncollapsed>
    pconfig package <pconfig/package>
    pconfig world <pconfig/world>
