"""
 ________  ___  ___  _____ _      ______ _   _ _   _ _____ _____ _____ _____ _   _ 
|  ___|  \/  | / _ \|_   _| |     |  ___| | | | \ | /  __ \_   _|_   _|  _  | \ | |
| |__ | .  . |/ /_\ \ | | | |     | |_  | | | |  \| | /  \/ | |   | | | | | |  \| |
|  __|| |\/| ||  _  | | | | |     |  _| | | | | . ` | |     | |   | | | | | | . ` |
| |___| |  | || | | |_| |_| |____ | |   | |_| | |\  | \__/\ | |  _| |_\ \_/ / |\  |
\____/\_|  |_/\_| |_/\___/\_____/ \_|    \___/\_| \_/\____/ \_/  \___/ \___/\_| \_/

╔═╗╔╗╔╦ ╦╦
║ ║║║║╚╦╝║
╚═╝╝╚╝ ╩ ╩ DOUBLE DOOR LEFT
                                                                                   
"""
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

#the email you want to use to send the file
sender_email = "putyouremailhere@gmail.com"
# the email that will receive the data
receiver_email = "putreceiveremailhere@gmail.com"

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
filename = "/home/pi/Desktop/FinalCodesHumanCounter/DOUBLEDOORentryLEFTData.txt"
#name of the csv
attachment = open("/home/pi/Desktop/FinalCodesHumanCounter/DOUBLEDOORentryLEFTData.txt", "rb")

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
s.login(sender_email, "yourpasswordhere")

# Converts the Multipart msg into a string
text = msg.as_string()

# sending the mail
s.sendmail(sender_email, receiver_email, text)
# terminating the session
#s.quit()
