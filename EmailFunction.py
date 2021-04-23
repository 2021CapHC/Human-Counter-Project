# Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported
import os
import time 
from time import sleep
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

while True:
    sender_email = "seniordesignproject458cv@gmail.com"
    receiver_email = "m.iqbal7225@gmail.com"

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the sender's email address
    msg['From'] = sender_email

    # storing the receiver's email address
    msg['To'] = receiver_email

    # storing the subject
    msg['Subject'] = "Subject of the Email"

    # string to store the body of the mail
    body = "Test Email"

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # open the file to be sent
    #filename is the directory
    filename = "/home/pi/BiDirectionalCounterData_v2.0.txt"
    #name of the csv
    attachment = open("/home/pi/BiDirectionalCounterData_v2.0.txt", "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    # this part of the encodes and helps transfer it to the email
    encoders.encode_base64(p)

    #p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    #password of your email address
    s.login(sender_email, "Classof2021")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(sender_email, receiver_email, text)
    time.sleep(90)
    # terminating the session
    #s.quit()
