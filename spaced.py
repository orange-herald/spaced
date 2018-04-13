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


def get_free_disk_space():
    # Shell command to display disk usage for / mount point
    command = "findmnt / -DoUSE%".split()
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    free_space = process.stdout.read()
    free_space = free_space.split('\n')[1][:-1]
    return 100 - int(free_space)


def log_data(free_space, disk_status):
    timestamp = datetime.datetime.now()
    update = "{:%Y-%m-%d %H:%M:%S} : FREE_DISK SPACE: {}%. STATUS: {}.\n"
    log_entry = update.format(timestamp, free_space, disk_status)

    try:
        log_file = open('disk_space.log', 'a')
        log_file.write(log_entry)
        print('Log file updated')
        log_file.close()
    except:
        print('Error writing to log file')


def send_low_disk_alert():
    print('DEBUG: Low disk space')
    
    # Configure email server and connect
    SENDER = 'testytesterqc@gmail.com'
    PASSWORD = 'queryclick'
    RECIPIENTS = 'steven@queryclick.com'
    SMTP_SERVER = 'smtp.gmail.com:587'


    # Configure message headers & body
    header = 'From: %s\n' % SENDER
    header += 'To: %s\n' % RECIPIENTS
    header += 'Subject: %s\n\n' % 'WARNING: Low disk space on MARIO'
    message = """WARNING: DISK SPACE LOW"""
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
    REMAINING_DISK_SPACE_LIMIT = 100
    free_space = get_free_disk_space()

    if free_space > REMAINING_DISK_SPACE_LIMIT:
        log_data(free_space, 'GOOD')
    else:
        log_data(free_space, 'BAD')
        send_low_disk_alert()


if __name__ == "__main__":
    main()