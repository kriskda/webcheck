import socket
import smtplib
from email.mime.text import MIMEText


class MailSender:
    
    def __init__(self, from_email, username, password, smtp):
        self.from_email = from_email
        self.username = username
        self.password = password
        self.smtp = smtp
    
    def send_message(self, to_email, subject, message):
        mime_message = self.composeMimeMessage(to_email, subject, message)
 
        self.__send_mail(to_email, mime_message)
        
    def __send_mail(self, to_email, mime_message):
        try:
            server = smtplib.SMTP(self.smtp)
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.from_email, to_email, mime_message.as_string())
            server.quit()
        except socket.gaierror:
            print "Could not send e-mail. Check server name!"			            
        except smtplib.SMTPAuthenticationError:
            server.quit()
            print "Could not send e-mail. Check user name, password and server name!"		
        except smtplib.SMTPRecipientsRefused:
            server.quit()
            print "Could not send e-mail. Check recipent e-mail adress!"	
        except smtplib.SMTPServerDisconnected:
            print "Could not send e-mail, server disconnected!"			            			    

    def composeMimeMessage(self, to_email, subject, message):
        mime_message = MIMEText(message, 'plain', 'utf-8')
        mime_message['Subject'] = subject
        mime_message['From'] = self.from_email
        mime_message['To'] = to_email
        
        return mime_message
