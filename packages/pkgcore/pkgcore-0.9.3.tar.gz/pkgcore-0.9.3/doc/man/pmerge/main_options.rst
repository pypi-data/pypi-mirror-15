positional arguments
====================

:TARGET:  
        Various target arguments are supported including the following:
        
        atom
            An extended atom syntax is supported, see the related section
            in pkgcore(5).
        
        package set
            Used to define lists of packages, the syntax used for these is
            @pkgset. For example, the @system and @world package sets are
            supported.
        
        extended globbing
            Globbing package names or atoms allows for use cases such as
            ``'far*'`` (merge every package starting with 'far'),
            ``'dev-python/*::gentoo'`` (merge every package in the dev-python
            category from the gentoo repo), or even '*' (merge everything).
        
        Also, the target '-' allows targets to be read from standard input.

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

package querying options
========================

-N, --newuse  
              Include installed packages with USE flag changes in the list of viable
              targets for rebuilding.
              
              USE flag changes include flags being added, removed, enabled, or
              disabled with regards to a package. USE flag changes can occur via
              ebuild alterations, profile updates, or local configuration
              modifications.
              
              Note that this option implies -1/--oneshot.

available operations
====================

-C, --unmerge      
                   Target packages for unmerging from the system.
                   
                   WARNING: This does not ask for user confirmation for any targets so
                   it's possible to quickly break a system.

--clean            
                   Remove installed packages that aren't referenced by any target packages
                   or sets. This defaults to using the world and system sets if no targets
                   are specified.
                   
                   Use with *caution*, this option used incorrectly can render your system
                   unusable. Note that this implies --deep.

-p, --pretend      
                   Resolve package dependencies and display the results without performing
                   any merges.

--ignore-failures  
                   Skip failures during the following phases: sanity checks
                   (pkg_pretend), fetching, dep resolution, and (un)merging.

-a, --ask          
                   Perform the dependency resolution, but ask for user confirmation before
                   beginning the fetch/build/merge process. The choice defaults to yes so
                   pressing the "Enter" key will trigger acceptance.

--force            
                   Force (un)merging on the livefs (vdb), regardless of if it's frozen.

-f, --fetchonly    
                   Only perform fetching of all targets from SRC_URI based on the current
                   USE configuration.

-1, --oneshot      
                   Build and merge packages normally, but do not add any targets to the
                   world file. Note that this is forcibly enabled if a package set is
                   specified.

resolver options
================

-u, --upgrade        
                     Try to upgrade specified targets to the latest visible version. Note
                     that altered package visibility due to keywording or masking can often
                     hide the latest versions of packages, especially for stable
                     configurations.

-D, --deep           
                     Force dependency resolution across the entire dependency tree for all
                     specified targets.

--preload-vdb-state  
                     Preload the installed package database which causes the resolver to
                     work with a complete graph, thus disallowing actions that conflict with
                     installed packages. If disabled, it's possible for the requested action
                     to conflict with already installed dependencies that aren't involved in
                     the graph of the requested operation.

-i, --ignore-cycles  
                     Ignore dependency cycles if they're found to be unbreakable; for
                     example: a depends on b, and b depends on a, with neither built.

--with-bdeps         
                     Pull in build time dependencies for built packages during dependency
                     resolution, by default they're ignored.

-O, --nodeps         
                     Build and merge packages without resolving any dependencies.

-n, --noreplace      
                     Skip packages that are already installed. By default when running
                     without this option, any specified target packages will be remerged
                     regardless of if they are already installed.

-b, --buildpkg       
                     Force binary packages to be built for all merged packages.

-k, --usepkg         
                     Binary packages are preferred over ebuilds when performing dependency
                     resolution.

-K, --usepkgonly     
                     Only binary packages are considered when performing dependency
                     resolution.

-S, --source-only    
                     Only ebuilds are considered when performing dependency
                     resolution.

-e, --empty          
                     Force all targets and their dependencies to be rebuilt.

output related options
======================

--quiet-repo-display                 
                                     In the package merge list display, suppress ::repo output and instead
                                     use index numbers to indicate which repos packages come from.

-F FORMATTER, --formatter FORMATTER  
                                     Select an output formatter to use for text formatting of --pretend or
                                     --ask output, currently available formatters include the following:
                                     basic, pkgcore, portage, portage-verbose, and paludis.
                                     
                                     The basic formatter is the nearest to simple text output and is
                                     intended for scripting while the portage/portage-verbose formatter
                                     closely emulates portage output and is used by default.
