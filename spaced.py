#! /env/python
"""
Server disk space monitor/alert
:author Steven MacDiarmid
:copyright 2018 QueryClick all rights reserved
"""
from __future__ import print_function
import datetime
import subprocess
import smtplib
from email.mime.text import MIMEText
from smtplib import SMTPAuthenticationError


def get_free_disk_space():
    # Shell command to display disk usage for / mount point
    command = "findmnt / -DoUSE%".split()
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    free_space = process.stdout.read()
    free_space = free_space.split('\n')[1][:-1]
    return 100 - int(free_space)


def log_data(free_space, disk_status):
    timestamp = datetime.datetime.now()
    update = "{:%Y-%m-%d %H:%M:%S} : FREE_DISK SPACE: {}%. STATUS: {}."
    print (update.format(timestamp, free_space, disk_status))


def send_low_disk_alert():
    print('DEBUG: Low disk space')
    
    # Configure email server and connect
    SENDER = 'testytesterqc@gmail.com'
    PASSWORD = 'queryclick'
    RECIPIENTS = 'steven@queryclick.com'
    SMTP_SERVER = 'smtp.gmail.com:465'


    # Configure message headers & body
    toaddr = RECIPIENTS

    header = 'From: %s\n' % SENDER
    header += 'To: %s\n' % RECIPIENTS
    header += 'Subject: %s\n\n' % 'WARNING: Low disk space on MARIO'
    message = """WARNING: DISK SPACE LOW"""
    message = header + message

    # Compose and attach message body
    #try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(SENDER, PASSWORD)

    server.sendmail(SENDER, toaddr, message)
    print('Email sent')
    server.quit()
    #except Exception:
    # print('Error sending email')


def main():
    REMAINING_DISK_SPACE_LIMIT = 100
    free_space = get_free_disk_space()

    if free_space > REMAINING_DISK_SPACE_LIMIT:
        log_data(free_space, 'GOOD')
    else:
        log_data(free_space, 'BAD')
        send_low_disk_alert()


if __name__ == "__main__":
    main()