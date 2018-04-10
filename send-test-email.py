#!/usr/bin/python

import smtplib
from env import email, password, server, port, subject, emailFrom, emailTemplate

sender = email
receivers = ['chance@sodiumhalogen.com']

message = """From: From Person <thelab@tndrivinginnovation.com>
To: To Person <chance@sodiumhalogen.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
    smtpObj = smtplib.SMTP(server, port)
    smtpObj.starttls()
    smtpObj.login(email, password)
    smtpObj.sendmail(sender, receivers, message)
    print "Successfully sent email"
except Exception:
    print "Error: unable to send email"
