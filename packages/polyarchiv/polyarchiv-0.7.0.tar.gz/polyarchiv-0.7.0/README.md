Polyarchiv
==========

Backup data from multiple local sources (organized in local repositories) and send them to one or more remote repositories.
Configuration is based on simple `.ini` files: 
    
  * `my-local-repo.local` defines a local repository named `my-local-repo`,
  * `my-remote-repo.remote` defines a remote repository named `my-remote-repo`.
  
Each local repository defines one or more data sources, all of them being defined in the `my-local-repo.local` file:

  * directory with files,
  * MySQL or PostgreSQL database to dump,
  * OpenLDAP database to dump.

There are several kinds of local repositories:

  * raw files,
  * local git repository: after each backup, files that have been gathered from the different sources are added and locally commited.
  
There are also several kinds of remote repositories:

  * GitRepository (requires a local git repository): after the backup, local commits are pushed to this remote git repository,
  * Rsync: after the backup, all files are synchronized to the remote repository,
  * TarArchive: after the backup, all files are archived in a single .tar.gz archive and sent to the remote repo (via ftp, scp, http, smb, or a basic cp),
  * Duplicity: after the backup, all files are encrypted and sent to the remote repository.

Each repository (either local or remote) is associated to a backup frequency. 
If a given repository has a daily backup frequency but you execute Polyarchiv twice a day, only the first backup will be executed. 

Installation
------------

The simplest way is to use `pip`:

    $ pip install polyarchiv

Some commands are available:
display the current configuration, local and remote repositories, sources and backup status

    $ polyarchiv show [-C /my/config/dir] [--verbose]

backup data. If you set a frequency, repositories that are not out-of-date are not run (unless you specified `--force`)

    $ polyarchiv backup [-C /my/config/dir] [--force]
 
display all available engines (and their options if you specified `--verbose`)

    $ polyarchiv help [--verbose]

You can also generate a Debian/Ubuntu package with: 

    sudo apt-get install python-stdeb
    python setup.py --command-packages=stdeb.command  bdist_deb

Configuration
-------------

The default configuration directory is `/etc/polyarchiv`. However, if you installed it in a virtualenv, 
then its default config dir is `$VIRTUALENV/etc/polyarchiv`. 
Otherwise, you can specify another config dir with `polyarchiv -C /my/config/dir`.

This directory should contain configuration files for local repositories 
(like `my-local.local`) as well as remote repositories (like `my-remote.remote`).

Here is an example of local repository, gathering data from three sources:

  * PostgresSQL database
  * MySQL database
  * a directory

Its name must end by `.local`. 
The `[global]` section defines options for the local repository, and other sections define the three sources:

    $ cat /etc/polyarchiv/my-local.local
    [global]
    engine=polyarchiv.locals.GitRepository
    local_path=/tmp/local
    local_tags=local
    included_remote_tags=*
    excluded_remote_tags=
    frequency=daily
    
    [source_1]
    engine=polyarchiv.sources.PostgresSQL
    host=localhost
    port=5432
    user=test
    password=testtest
    database=testdb
    destination_path=./postgres.sql
    
    [source_2]
    engine=polyarchiv.sources.MySQL
    host=localhost
    port=3306
    user=test
    password=testtest
    database=testdb
    destination_path=./mysql.sql
    
    [source_3]
    engine=polyarchiv.sources.RSync
    source_path=/tmp/source/files
    destination_path=./files

The kind of repository (either local or remote) and of each source is defined by the "engine" option.
You can define as many local repositories (each of them with one or more sources) as you want.
Remote repositories are simpler and only have a `[global]` section.
Their names must end by `.remote`.
Here is a gitlab acting as remote storage for git local repo: 

    $ cat /etc/polyarchiv/my-remote1.remote
    [global]
    engine=polyarchiv.remotes.GitRepository
    frequency=daily
    remote_tags=
    remote_url=http://gitlab.example.org/group/TestsPolyarchiv.git
    remote_branch=master
    user=mgallet
    included_local_tags=*

Maybe you also want a full backup (as an archive) uploaded monthly (the tenth day of each month) to a FTP server:

    $ cat /etc/polyarchiv/my-remote2.remote
    [global]
    engine=polyarchiv.remotes.TarArchive
    frequency=monthly:10
    remote_tags=
    remote_url=ftp://myftp.example.org/backups/project/
    remote_branch=master
    user=mgallet
    password=p@ssw0rd
    tar_format=tar.xz
    included_local_tags=*

Configuration files can be owned by different users: files that are unreadable by the current user are ignored.

Available engines
-----------------

Several engines for sources and remote or local repositories are available.
Use `polyarchiv plugins` to display them (and `polyarchiv plugins -v` to display all their configuration options). 

Associating local and remote repositories
-----------------------------------------

All remote repositories apply to all local repositories but you can change this behaviour by applying tags to repositories.
By default, a local repository has the tag `local` and include all remote repositories `included_remote_tags=*`.
A remote repository has the tag `remote` and include all local repositories `included_local_tags=*`.

If large local repositories should not be sent to a given remote repository, you can exclude the "large" tags from the remote configuration:
 
    $ cat /etc/polyarchiv/my-remote.remote
    [global]
    engine=polyarchiv.remotes.GitRepository
    excluded_local_tags=*large,huge

and add the "large" tag in the local configuration:

    $ cat /etc/polyarchiv/my-local.local
    [global]
    engine=polyarchiv.locals.GitRepository
    local_path=/tmp/local
    local_tags=local,large

Traditionnal shell expansion is used for comparing included and excluded tags. Tags can be applied to remote repositories:

    $ cat /etc/polyarchiv/my-remote.remote
    [global]
    engine=polyarchiv.remotes.GitRepository
    remote_tags=small-only

and add the "large" tag to the local configuration:

    $ cat /etc/polyarchiv/my-local.local
    [global]
    engine=polyarchiv.locals.GitRepository
    local_path=/tmp/local
    included_remote_tags=huge,large
    
Since the remote repository does not present either the `huge` tag or the `large` tag, it will not be applied.
