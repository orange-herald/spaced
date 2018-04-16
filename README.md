# Spaced Out
> Python script to monitor and report on available server disk space.

## Description
Linode's dashboards do not currently display the remaining disk space available on our various servers. Obviously this can outages if servers run out of space without alerting us.

This Python script can be run manually or (preferably) via Cron on a user-defined schedule to log disk space and send warning emails if necessary.

## Usage example

./scraped.py [email@example.com]

The email address is optional. If none is provided, the default address of 'droids@queryclick.com' is used.


## Release History

* 0.1
    * 16/04/18: Initial release.

## Meta

Author/maintainer: Steven MacDiarmid

steven@queryclick.com

&copy; 2018 [QueryClick](https://www.queryclick.com). All rights reserved

[https://github.com/orange-herald/](https://github.com/orange-herald/spaced)
