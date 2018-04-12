#! /env/python

"""
Server disk space monitor/alert
:author Steven MacDiarmid
:copyright 2018 QueryClick all rights reserved
"""

import datetime
import subprocess


REMAINING_DISK_SPACE_LIMIT = 25


def get_free_disk_space():
    # Shell command to display disk usage for / mount point
    command = "findmnt / -DoUSE%".split()
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    free_space = process.stdout.read()
    free_space = free_space.split('\n')[1][:-1]
    return 100 - int(free_space)


def log_data(free_space, disk_status):
    timestamp = datetime.datetime.now()
    print "{:%Y-%m-%d %H:%M:%S} : FREE_DISK SPACE: {}%. STATUS: {}.".format(timestamp, free_space, disk_status)


def send_low_disk_alert():
    print 'Sad face!'
    


def main():
    free_space = get_free_disk_space()
    # print free_space

    if free_space > REMAINING_DISK_SPACE_LIMIT:
        log_data(free_space, 'GOOD')
    else:
        log_data(free_space, 'BAD')
        send_low_disk_alert()


if __name__ == "__main__":
    main()