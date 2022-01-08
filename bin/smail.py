#! /usr/bin/python
import smtplib, ssl

#options = {'mail_account_username': 'dso.autobpe', 'mail_account_password': 'gevdais;ia'}
#SEND_MAIL_TO = 'xanthos.papanikolaou@gmail.ntua.gr,dganastasiou@gmail.com'
#recipients_list = SEND_MAIL_TO.split(',')

message = ""
message += "Subject: autobpe-{:} {:}@{:}\n\n\n".format('foo','bar','baz')
message += 'body text\ntest email'

port =465
password='gevdais;ia'
sender_email = "autobpe.dso@gmail.com"
receiver_emails = ['xanthos@noa.gr', 'xanthos.papanikolaou@gmail.com']
server = smtplib.SMTP_SSL("smtp.gmail.com", port)
server.ehlo()
server.login(sender_email, password)
server.sendmail(sender_email, receiver_emails, message)
server.close()

#port = 465 # for SSL
#
## Create a secure SSL context
#context = ssl.create_default_context()
#with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#    #server.login(sender_email, options['mail_account_password'])
#    server.login(sender_email, "gevdais;ia")
#    server.sendmail(sender_email, recipients_list, message)

#port = 587  # For starttls
#smtp_server = "smtp.gmail.com"
#receiver_email = "xanthos.papanikolaou@gmail.com"
#password = input("Type your password and press enter:")
#message = """\
#Subject: Hi there
#
#This message is sent from Python."""
#
#context = ssl.create_default_context()
#with smtplib.SMTP(smtp_server, port) as server:
#    server.ehlo()  # Can be omitted
#    server.starttls(context=context)
#    server.ehlo()  # Can be omitted
#    server.login(sender_email, password)
#    server.sendmail(sender_email, receiver_email, message)
