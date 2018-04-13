#! /usr/bin/python
"""
Server disk space monitor/alert
:author Steven MacDiarmid
:copyright 2018 QueryClick all rights reserved
"""
from __future__ import print_function
from email.mime.text import MIMEText
from os.path import expanduser

import datetime
import smtplib
import subprocess

# DISK STATUS CODES
HEALTHY = 40
CHECK = 25
CRITICAL = 15

# Get home dir of current user to set logfile path
HOME_DIR = expanduser('~')


def get_free_disk_space():
    """
    Get amount of disk space as %.
    :return free disk space as int
    """

    # Shell command to display disk usage for / mount point
    command = "findmnt / -DoUSE%".split()
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    free_space = process.stdout.read()
    free_space = free_space.split('\n')[1][:-1]             # Remove '%'
    return 100 - int(free_space)


def log_and_report_disk_usage(free_space, disk_status):
    """
    Update log file with current disk utilisation and (optionally) send email alert.
    :param free_space as int
    :disk_status as str
    :return void
    """

    LOG_FILE = HOME_DIR + '/disk_space.log'
    timestamp = datetime.datetime.now()
    update = "{:%Y-%m-%d %H:%M:%S} : FREE DISK SPACE ON MARIO: {}%. STATUS: {}.\n"
    log_entry = update.format(timestamp, free_space, disk_status)

    try:
        log_file = open(LOG_FILE, 'a')
        log_file.write(log_entry)
        print('Log file updated')
        log_file.close()
    except:
        print('Error writing to log file')

    if disk_status != 'HEALTHY':
        send_low_disk_alert(log_entry)


def send_low_disk_alert(disk_status):
    """
    Send email alert if disk space below healthy level.
    :param disk_status as str
    """

    # Configure email server and connect
    SENDER = 'testytesterqc@gmail.com'
    PASSWORD = 'queryclick'
    RECIPIENTS = 'steven@queryclick.com'
    SMTP_SERVER = 'smtp.gmail.com:587'


    # Configure message headers & body
    header = 'From: %s\n' % SENDER
    header += 'To: %s\n' % RECIPIENTS
    header += 'Subject: %s\n\n' % 'WARNING: Low disk space on MARIO'
    message = disk_status
    message = header + message

    # Compose and attach message body
    try:
        server = smtplib.SMTP(SMTP_SERVER)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECIPIENTS, message)
        print('Email sent')
        server.quit()
    except:
        print('Error sending email')


def main():
    free_space = get_free_disk_space()

    if free_space > HEALTHY:
        log_and_report_disk_usage(free_space, 'HEALTHY')
    elif free_space < CRITICAL:
        log_and_report_disk_usage(free_space, 'CRITICAL')
    else:
        log_and_report_disk_usage(free_space, 'CHECK')


if __name__ == "__main__":
    main()