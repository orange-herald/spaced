#! /env/python

"""
Server disk space monitor/alert
:author Steven MacDiarmid
:copyright 2018 QueryClick all rights reserved
"""

import subprocess

def get_free_disk_space():
    # Shell command to display disk usage for / mount point
    command = "findmnt / -DoUSE%".split()
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    free_space = process.stdout.read()
    free_space = free_space.split('\n')[1][:-1]
    return free_space

#print "Free space {} %".format(free_space)

# if free_space < WARN_THRESHOLD
    # log value
    # do nothing


# if free_space >= WARN_THRESHOLD
    # send email
    # log value


def main():
    print get_free_disk_space()


if __name__ == "__main__":
    main()