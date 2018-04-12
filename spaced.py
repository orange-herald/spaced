"""
Server disk space monitor/alert
:author Steven MacDiarmid
:copyright 2018 QueryClick all rights reserved
"""

# df -h / | tail -1 | awk '{ print $5 }'

# run disk space command

# if free_space < WARN_THRESHOLD
    # log value
    # do nothing


# if free_space >= WARN_THRESHOLD
    # send email
    # log value