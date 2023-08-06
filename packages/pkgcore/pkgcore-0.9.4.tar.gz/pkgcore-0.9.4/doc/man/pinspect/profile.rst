===========================================
pinspect profile - profile related querying
===========================================

synopsis
========

pinspect profile [-h] [--version] [--debug] [-q] [-v] [--color BOOLEAN] [-r REPO] {parent,eapi,status,deprecated,provided,system,use_expand,iuse_effective,masks,unmasks,bashrcs,keywords,accept_keywords,use,masked_use,stable_masked_use,forced_use,stable_forced_use,defaults,arch} ...

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

subcommand options
==================

-r REPO, --repo REPO  
                      target repo

subcommands
===========

profile commands

.. toctree::
    :maxdepth: 2

    pinspect profile parent <profile/parent>
    pinspect profile eapi <profile/eapi>
    pinspect profile status <profile/status>
    pinspect profile deprecated <profile/deprecated>
    pinspect profile provided <profile/provided>
    pinspect profile system <profile/system>
    pinspect profile use_expand <profile/use_expand>
    pinspect profile iuse_effective <profile/iuse_effective>
    pinspect profile masks <profile/masks>
    pinspect profile unmasks <profile/unmasks>
    pinspect profile bashrcs <profile/bashrcs>
    pinspect profile keywords <profile/keywords>
    pinspect profile accept_keywords <profile/accept_keywords>
    pinspect profile use <profile/use>
    pinspect profile masked_use <profile/masked_use>
    pinspect profile stable_masked_use <profile/stable_masked_use>
    pinspect profile forced_use <profile/forced_use>
    pinspect profile stable_forced_use <profile/stable_forced_use>
    pinspect profile defaults <profile/defaults>
    pinspect profile arch <profile/arch>
