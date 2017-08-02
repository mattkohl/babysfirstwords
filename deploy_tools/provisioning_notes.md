Provisioning a new site
=======================

## Required packages:

* nginx
* Python 3.5
* virtualenv + pip
* Git

eg, on Ubuntu 16.04:

    sudo apt-get install nginx git python3-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace USERNAME with username
* replace SITENAME with my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace USERNAME with username
* replace SITENAME with my-domain.com
* replace BFW_EMAIL_ADDRESS with site email address
* replace BFW_EMAIL_PASSWORD with site email password

## Folder structure:
Assume we have a user account at /home/username

```
/home/username
└── sites
    └── SITENAME
         ├── database
         ├── source
         ├── static
         └── virtualenv
```