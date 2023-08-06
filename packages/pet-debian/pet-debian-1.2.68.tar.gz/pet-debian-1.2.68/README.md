[![CoverageStatus](https://coveralls.io/repos/github/PET-UnB/pet/badge.svg?branch=travis)](https://coveralls.io/github/PET-UnB/pet?branch=travis)
[![BuildStatus](https://travis-ci.org/PET-UnB/pet.svg?branch=travis)](https://travis-ci.org/PET-UnB/pet.svg?branch=travis)
1111111111111111111111111111

# PET - Package Entropy Tracker

PET is a collection of scripts that gather information about your (or your group's) packages.
It allows you to see in a bird's eye view the health of hundreds of packages,
instantly realizing where work is needed.

The code is at https://anonscm.debian.org/cgit/pet/pet3.git/,
database dumps can be found at http://pet.43-1.org/~pet/db/.

Discussions go on the [pet-devel](https://lists.alioth.debian.org/mailman/listinfo/pet-devel) mailing list.

There are two ways to install Pet. With or without vagrant. Choose one and follow the next steps to install.

## Installation using Vagrant

Vagrant is a tool for building complete development environments. With an easy-to-use workflow and focus on automation, Vagrant lowers development environment setup time, increases development/production parity, and makes the "works on my machine" excuse a relic of the past. [Official Site Reference](https://www.vagrantup.com/).

Vagrant can be installed with the command: apt-get install vagrant. And all the binaries are in this page [Vagrant Download](https://www.vagrantup.com/downloads.html).

To install PET, it is necessary to clone the repository and start vagrant:

`$ git clone https://anonscm.debian.org/cgit/pet/pet3.git/`

`$ cd pet/`

Now, it is necessary to start vagrant up and access vagrants ssh. Follow this commands:
`$ vagrant up`

`$ vagrant ssh`

`$ sudo su - pet`


To start the web interface, execute:

`$ ./pet-serve`

To access it: [http://localhost:4567/pkg-perl/pet.cgi](http://localhost:8080/pkg-perl/pet.cgi)

## Installation without Vagrant
### Requirements
Install this softwares according to your operation system:
* postgresql-9.4
* postgresql-9.4-debversion
* python-argparse
* python-debian
* python-debianbts
* python-inotifyx
* python-paste
* python-psycopg2
* python-pyramid
* python-sqlalchemy
* python-subversion
* wget

### Quick Start
**As root (waiting for python-pyramid-chameleon package**, https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=785048):

`$ pip install pyramid_chameleon`

**As root (more precise: as a postgres superuser):**

`$ su postgres`

`$ createuser pet`

`Shall the new role be a superuser? (y/n) n`

`Shall the new role be allowed to create databases? (y/n) y`

`Shall the new role be allowed to create more new roles? (y/n) n`

`$ createdb -O pet pet`

`$ psql pet < /usr/share/postgresql/9.4/contrib/debversion.sql`

**As the created user:**

`$ ./pet-update -c`

`$ psql pet`

`pet=> INSERT INTO team (name, maintainer, url) VALUES ('pkg-perl', 'Debian Perl Group <pkg-perl-maintainers@lists.alioth.debian.org>', 'http://pkg-perl.alioth.debian.org/');`

`pet=> INSERT INTO repository (name, type, root, web_root, team_id) VALUES ('git','git','https://pet.alioth.debian.org/pet2-data/pkg-perl/git-pkg-perl-packages.json','http://anonscm.debian.org/gitweb/?p=pkg-perl/packages', 1);`

`pet=> INSERT INTO package (name, repository_id) VALUES ('clive', 1);`

`pet=> INSERT INTO archive (name, url, web_root) VALUES ('debian', 'http://cdn.debian.net/debian', 'http://packages.qa.debian.org/');`

`pet=> INSERT INTO suite (archive_id, name) VALUES (1, 'unstable');`

`pet=> \q`

`$ ./update-package libboolean-perl`

`$ ./update-bts`

`$ ./update-archive debian`

To start the web interface:

`$ ./pet-serve`

To access it: [http://localhost:8080/pkg-perl/pet.cgi](http://localhost:8080/pkg-perl/pet.cgi)

# Update Repository
To get the packages, it is necessary to update your local repository.
`$ update-repository x`

x is a positive integer of the repository. e.g. pass 1.
This command will return all packages.

Now, update the packages with the names printed on `$ update-repository x`. Follow this command:

`$ update-package packages_name`

After updating all packages, run:

`$ ./update-bts`
