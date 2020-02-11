# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 22:08:49 2020
@author: Gareth V. Walkom (walkga04 at googlemail.com)

Structure:|
----------

connect():
send():
disconnect():

"""
import smtplib

# Setup an email address to email from and to
# https://automatetheboringstuff.com/chapter16/
def connect(email, password, smtp='smtp.gmail.com', gate=587):
    """
    [ADD THIS]

    Parameters
    ----------
    email : TYPE
        DESCRIPTION.
    password : TYPE
        DESCRIPTION.
    smtp : TYPE, optional
        DESCRIPTION. The default is 'smtp.gmail.com'.
    gate : TYPE, optional
        DESCRIPTION. The default is 587.

    Returns
    -------
    smtp_obj : TYPE
        DESCRIPTION.

    """

    # Connect to an SMTP server
    smtp_obj = smtplib.SMTP(smtp, gate)
    # Establish a connection to the SMTP server
    smtp_obj.ehlo()
    # Enable encryption for connection
    smtp_obj.starttls()
    # Enter login details
    smtp_obj.login(email, password)

    return smtp_obj

# Send email to given email address
def send(smtp_obj, email):
    """
    [ADD THIS]

    Parameters
    ----------
    smtp_obj : TYPE
        DESCRIPTION.
    email : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # Send mail with text to email
    smtp_obj.sendmail(email, email, 'Subject: Measurement\nMeasurement finished.')

def disconnect(smtp_obj):
    """
    [ADD THIS]

    Parameters
    ----------
    smtp_obj : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    # Close email connection
    smtp_obj.quit()
