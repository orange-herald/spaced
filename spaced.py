#! /usr/bin/python
"""
Server disk space monitor/alert
:author Steven MacDiarmid
:copyright 2018 QueryClick all rights reserved
"""
from __future__ import print_function
from email.mime.text import MIMEText
from os.path import expanduser
from sys import argv

import datetime
import smtplib
import socket
import subprocess

# Disk status codes
HEALTHY = 40
CHECK = 25
CRITICAL = 15

# Get home dir of current user to set logfile path
HOME_DIR = expanduser('~')
HOST_NAME = socket.gethostname()

if HOST_NAME == 'localhost' or HOST_NAME == 'ubuntu':



DEFAULT_EMAIL_RECIPIENT = 'droids@queryclick.com'



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


def log_and_report_disk_usage(free_space, disk_status, email_recipient):
    """
    Update log file with current disk utilisation and (optionally) send email alert.
    :param free_space as int
    :param disk_status as str
    :param email_recipient<optional> as str
    :return void
    """
    LOG_FILE = HOME_DIR + '/disk_space.log'
    timestamp = datetime.datetime.now()
    update = "{:%Y-%m-%d %H:%M:%S} : FREE DISK SPACE ON {}: {}%. STATUS: {}.\n"
    log_entry = update.format(timestamp, HOST_NAME, free_space, disk_status)

    try:
        log_file = open(LOG_FILE, 'a')
        log_file.write(log_entry)
        print('Log file updated')
        log_file.close()
    except:
        print('Error writing to log file')

    if disk_status != 'HEALTHY':
        send_low_disk_alert(log_entry, email_recipient)


def send_low_disk_alert(disk_status, email_recipient):
    """
    Send email alert if disk space below healthy level.
    :param disk_status as str
    """

    # Configure email server and connect
    SENDER = 'testytesterqc@gmail.com'
    PASSWORD = 'queryclick'
    SMTP_SERVER = 'smtp.gmail.com:587'


    # Configure message headers & body
    header = 'From: %s\n' % SENDER
    header += 'To: %s\n' % email_recipient
    header += 'Subject: WARNING: Low disk space on %s\n\n' % HOST_NAME
    message = disk_status
    message = header + message

    # Compose and attach message body
    try:
        server = smtplib.SMTP(SMTP_SERVER)
        server.starttls()
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, email_recipient, message)
        print('Email sent')
        server.quit()
    except:
        print('Error sending email')


def main():
    free_space = get_free_disk_space()
    
    # Has alternative email been provided as command-line argument?
    if len(argv) > 1:
        email_recipient = str(argv[1])
    else:
        email_recipient = DEFAULT_EMAIL_RECIPIENT
    
    if free_space > HEALTHY:
        log_and_report_disk_usage(free_space, 'HEALTHY', email_recipient)
    elif free_space < CRITICAL:
        log_and_report_disk_usage(free_space, 'CRITICAL', email_recipient)
    else:
        log_and_report_disk_usage(free_space, 'CHECK', email_recipient)


if __name__ == "__main__":
    main()
